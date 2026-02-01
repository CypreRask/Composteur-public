# 🏗️ Architecture Globale - Composteur V2

> **Document de synthèse** - Vue d'ensemble technique complète  
> **Source de vérité** : `/docs/v2/` pour les détails spécifiques

---

## 🎯 Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              PIPELINE COMPLÈTE V2                                │
└─────────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────┐      UART 36B      ┌──────────────┐      LoRaWAN      ┌──────────┐
  │  ESP32       │ ◄────────────────► │  Heltec      │ ─────────────────►│   TTN    │
  │  ÉMETTEUR    │   9600 baud        │  RÉCEPTEUR   │    Payload 32B    │  (Cloud) │
  │  (Capteurs)  │   Wake Pulse       │  (V3)        │                   │          │
  └──────┬───────┘   GPIO23→RST       └──────────────┘                   └────┬─────┘
         │                                                                     │
         │  Capteurs :                                                          │ MQTT
         │  • SCD41 (CO2/Temp/Hum) - I2C2 GPIO 13/14                           │
         │  • AHT20 (Temp/Hum Air) - I2C1 GPIO 21/22                           │
         │  • NPK RS485 (Sol) - UART2 GPIO 16/17 + DE/RE GPIO 5                │
         │  • MQ137/4/7 (Gaz) - Mux GPIO 32/33/25/26/34 via MOSFET GPIO 4     │
         │                                                                    ▼
         │                                                           ┌──────────┐
         │         4h10min Cycle :                                   │  Python  │
         │         10min Préchauffe → Mesure → Sleep 4h              │  ingest  │
         │                                                              └────┬─────┘
         │                                                                 │
         ▼                                                                 ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                           BACKEND (web-monitor/backend/)                  │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
  │  │  FastAPI     │  │  SQLite      │  │  MQTT Client │  │  ML Model    │  │
  │  │  Port 8085   │  │  compost.db  │  │  (ingest.py) │  │  (scikit)    │  │
  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │
  └──────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼ HTTP/JSON
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         FRONTEND (web-monitor/frontend/)                  │
  │              Svelte 5 + Vite + Tailwind (Pixel Art Terraria-like)         │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## 📡 Chaîne de communication détaillée

### 1. Émetteur → Récepteur (UART)

```
Format    : [0xBB][0x20][Payload 32B][CRC16_L][CRC16_H]
Taille    : 36 bytes
Vitesse   : 9600 baud
Pins      : TX=GPIO18 (Émetteur) → RX=GPIO20 (Heltec)
Wake      : GPIO23 pulse 50ms → RST Heltec
```

**Pourquoi 36 bytes ?**
- 1 header + 1 length = framing
- 32 bytes payload = données
- 2 bytes CRC = intégrité

### 2. Récepteur → TTN (LoRaWAN)

```
Format    : [Payload 32B uniquement]
Taille    : 32 bytes
Protocole : LoRaWAN OTAA (session sauvegardée)
Fréquence : 867.9 MHz (SF9)
```

**Pourquoi 32 et pas 36 ?**
- Le récepteur vérifie le CRC localement
- Envoie uniquement le payload utile
- Économie de bandwidth + airtime LoRaWAN

### 3. TTN → Backend (MQTT)

```
Topic     : v3/{APP_ID}@ttn/devices/+/up
Format    : JSON avec decoded_payload
Parsing   : ingest.py mappe vers SQLModel
```

**⚠️ Point critique** : Le payload formatter TTN doit gérer :
- **Little Endian** pour MQ/SCD/AHT (code ESP32 LE)
- **Big Endian** pour NPK (capteur RS485 natif BE)

---

## ⚡ Architecture électrique

```
Panneau Solaire
       │
       ▼
   MPPT (charge LiFePO4)
       │
       ▼
 Batterie LiFePO4 12.8V
       │
       ▼
   Buck 8-40V → 12V stable
       │
       ▼
 Carte d'Extension
   ┌───────────────┐
   │  Régul 5V     │───► MQ (via MOSFET GPIO4)
   │  Régul 3.3V   │───► ESP32 + I2C
   └───────────────┘
```

**Consommation** :
- **Mesure** (~11min) : ~600mA (MQ chauffants actifs)
- **Sleep** (4h) : ~5mA (ESP32 light sleep + NPK veille)

---

## 🗄️ Structure de données

### Base de données (SQLite)

```sql
Table: compostmeasure
├── id (PK)
├── timestamp (UTC)
├── frame_id (compteur cycles)
├── mq137, mq4, mq7 (raw ADC 0-4095)
├── co2 (ppm), temp_scd, hum_scd (SCD41)
├── temp_aht, hum_aht (AHT20)
├── soil_hum, soil_temp, soil_ec, soil_ph (NPK)
├── soil_n, soil_p, soil_k (nutriments mg/kg)
└── rssi, snr (métriques LoRa)
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/latest` | Dernière mesure |
| `GET /api/history?limit=100` | Historique |
| `GET /api/history/stats?days=30` | Stats journalières |
| `POST /api/predict` | Prédiction ML température |
| `GET /api/weather` | Météo externe |

---

## 🔄 Cycle de vie d'une mesure

```
T+0min     : WAKE - Allumage MOSFET (MQ), démarrage préchauffe
T+0-10min  : PREHEAT - MQ chauffent (150mA × 3), SCD41 ready
T+10min    : MEASURE - Lecture tous capteurs (AHT, SCD, MQ×3, NPK RS485)
T+10min30s : BUILD - Construction trame 36 bytes + CRC16
T+10min30s : CUT - MOSFET OFF (économie)
T+10min30s : WAKE_SLAVE - Pulse GPIO23 → RST Heltec
T+10min35s : WAIT - Attente 5s boot + join LoRaWAN Heltec
T+10min40s : SEND_UART - Envoi trame ×5 (redondance) @ 9600 baud
T+11min    : SLEEP - Light sleep ESP32 pour 4h
T+4h11min  : WAKE - Redémarrage cycle
```

**Durée totale cycle** : 4h + ~11 minutes

---

## 🎨 Architecture Frontend

### Stack technique

```
Svelte 5 (runes)
    │
    ├── Vite (build)
    ├── Tailwind CSS v4 (styling)
    ├── Svelte Motion (animations)
    └── Fetch → FastAPI localhost:8085
```

### Design System

```
Style       : Pixel Art "Terraria-like"
Règles      : No rounded, no emojis, border-4, hard shadows
Palette     : #3E2723 (humus), #558B2F (vert), #795548 (terre)
Typographie : VT323 (pixel)
```

---

## 📁 Organisation des sources de vérité

| Composant | Source de vérité | Documentation |
|-----------|------------------|---------------|
| **Pinout GPIO** | `v2/emetteur/emetteur.ino` | [`docs/v2/WIRING_V2.md`](v2/WIRING_V2.md) |
| **Format trame** | `v2/recepteur/recepteur.ino` | [`docs/v2/PROTOCOL_V2.md`](v2/PROTOCOL_V2.md) |
| **Alimentation** | Montage physique réel | [`docs/v2/POWER_V2.md`](v2/POWER_V2.md) |
| **Payload TTN** | `v2/ttn-payload-formatter.js` | Inline + commentaires |
| **API Backend** | `web-monitor/backend/main.py` | FastAPI auto-docs (/docs) |
| **Modèle DB** | `web-monitor/backend/models.py` | SQLModel schema |

---

## ⚠️ Pièges et erreurs connues (V1 → V2)

| Erreur V1 | Correction V2 | Où c'est documenté |
|-----------|---------------|-------------------|
| GPIO27 MOSFET | **GPIO4** | WIRING_V2.md |
| I2C AHT20 sur 22/23 | **SDA=21, SCL=22** | WIRING_V2.md |
| Header 0xAA, 12 bytes | **0xBB, 36 bytes** | PROTOCOL_V2.md |
| Timing 2min/45min | **10min/4h** | PROTOCOL_V2.md |
| AGM + PWM | **LiFePO4 + MPPT** | POWER_V2.md |
| NPK en Little Endian | **Big Endian** | ttn-payload-formatter.js |

---

## 🔗 Liens rapides

- **Setup complet** : Voir [`../README.md`](../README.md)
- **Doc technique V2** : [`/docs/v2/`](v2/)
- **Archive V1** : [`/docs/legacy_v1/`](legacy_v1/)
- **Code source** : [`/v2/`](../v2/)

---

*Dernière mise à jour : Janvier 2026 - Passage V1→V2*
