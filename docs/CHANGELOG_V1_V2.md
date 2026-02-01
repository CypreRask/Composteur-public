# 📝 Changelog V1 → V2 - Composteur IoT

> **Guide de migration** - Tout ce qui change entre les versions

---

## 🎯 Pourquoi une V2 ?

La V1 fonctionnait mais avait des limitations :
- Pas de capteur sol (NPK)
- Pas de CRC (risque données corrompues)
- Timing trop court (45min) pour monitoring compost
- Pins mal choisies (conflits potentiels)
- Alimentation non optimisée (AGM vs LiFePO4)

---

## 📊 Tableau comparatif complet

### Hardware - Pins

| Fonction | V1 (OBSOLÈTE) | V2 (ACTUEL) | Impact |
|----------|---------------|-------------|--------|
| **MOSFET MQ** | GPIO 27 | **GPIO 4** | 🔴 Breaking change |
| **AHT20 SDA** | GPIO 22 | **GPIO 21** | 🔴 Breaking change |
| **AHT20 SCL** | GPIO 23 | **GPIO 22** | 🔴 Breaking change |
| **SCD41** | Non présent | **GPIO 13/14** | 🟢 Ajout |
| **NPK RS485** | Non présent | **GPIO 16/17/5** | 🟢 Ajout |
| **UART TX** | GPIO 17 | **GPIO 18** | 🔴 Breaking change |
| **Wake Heltec** | Non présent | **GPIO 23** | 🟢 Ajout |
| **MUX SIG** | GPIO 34 | **GPIO 34** | 🟢 Identique |
| **MUX S0-S3** | GPIO 32/33/25/26 | **GPIO 32/33/25/26** | 🟢 Identique |

### Communication

| Aspect | V1 | V2 | Impact |
|--------|-----|-----|--------|
| **Header** | `0xAA` | **`0xBB`** | 🔴 Breaking change |
| **Taille UART** | 12 bytes | **36 bytes** | 🔴 Breaking change |
| **Taille LoRaWAN** | 12 bytes | **32 bytes** | 🔴 Breaking change |
| **CRC** | Aucun | **CRC16 Modbus** | 🟢 Fiabilité |
| **Redondance** | 1× | **5× envoi** | 🟢 Fiabilité |
| **Baudrate** | 9600 | **9600** | 🟢 Identique |

### Timing & Énergie

| Paramètre | V1 | V2 | Impact |
|-----------|-----|-----|--------|
| **Préchauffe MQ** | 2 min | **10 min** | 🟢 Stabilité capteurs |
| **Sleep** | 45 min | **4h** | 🔋 Autonomie x4 |
| **Cycle total** | ~47 min | **~4h10** | 📊 Moins de points |
| **Batterie** | AGM | **LiFePO4** | 🔋 Durée de vie |
| **Charge** | PWM | **MPPT** | ☀️ Efficacité +20% |
| **Distribution** | Directe | **Carte extension** | 🔧 Modularité |

### Données - Capteurs

| Capteur | V1 | V2 | Notes |
|---------|-----|-----|-------|
| **MQ-137 (NH3)** | ✅ | ✅ | Position Mux C0 |
| **MQ-4 (CH4)** | ✅ | ✅ | Position Mux C1 |
| **MQ-7 (CO)** | ❌ | ✅ | Position Mux C2 (nouveau) |
| **SCD41 (CO2)** | ❌ | ✅ | I2C2 - Compost interne |
| **AHT20** | ✅ | ✅ | I2C1 - Air ambiant |
| **NPK RS485** | ❌ | ✅ | Sol - N/P/K/pH/EC |

### Payload - Endianness

| Champ | V1 | V2 | Note |
|-------|-----|-----|------|
| **MQ/SCD/AHT** | Little Endian | **Little Endian** | 🟢 Identique |
| **NPK** | Non présent | **Big Endian** | ⚠️ Spécifique |

---

## 🔧 Guide de migration (pour ceux qui avaient une V1)

### Étape 1 : Câblage (Physique)

```diff
- Déconnecter GPIO27 (MOSFET)
+ Connecter GPIO4 (MOSFET)

- Déplacer AHT20 : SDA GPIO22 → SDA GPIO21
- Déplacer AHT20 : SCL GPIO23 → SCL GPIO22

+ Ajouter SCD41 sur GPIO13/14
+ Ajouter NPK sur GPIO16/17/5

- Déplacer TX UART : GPIO17 → GPIO18
+ Ajouter fil Wake : GPIO23 → RST Heltec
```

### Étape 2 : Firmware (Flash)

```bash
# Ancien code V1
v1/emetteur.ino  # Supprimer ou archiver

# Nouveau code V2
v2/emetteur/emetteur.ino     # Flash ESP32 émetteur
v2/recepteur/recepteur.ino   # Flash Heltec
```

### Étape 3 : Payload Formatter TTN

**Avant (V1)** :
```javascript
// 12 bytes, header 0xAA, pas de CRC
if (bytes[0] !== 0xAA) return { errors: [] };
```

**Après (V2)** :
```javascript
// 32 bytes, pas de header ni CRC (vérifié par récepteur)
// + Ajout helpers Big Endian pour NPK
function readUint16BE(idx) { return (bytes[idx] << 8) | bytes[idx+1]; }
// soil_n = readUint16BE(25)  // Attention : BE pas LE !
```

### Étape 4 : Backend

```python
# Ancien modèle (V1)
class CompostData:
    mq2: int      # Un seul MQ
    temp: float   # Un seul capteur temp

# Nouveau modèle (V2)
class CompostMeasure:
    mq137: int    # NH3
    mq4: int      # CH4
    mq7: int      # CO (nouveau)
    co2: int      # SCD41 (nouveau)
    temp_scd: float   # Temp compost
    temp_aht: float   # Temp air
    soil_n: int   # NPK (nouveau)
    soil_p: int   # NPK (nouveau)
    soil_k: int   # NPK (nouveau)
```

---

## ⚠️ Erreurs fréquentes lors de la migration

### 1. Oublier le pont diviseur sur GPIO34
**Symptôme** : Valeurs ADC aléatoires ou ESP32 qui reboot  
**Solution** : Vérifier R1=2.2kΩ / R2=4.7kΩ

### 2. Confondre Endianness NPK
**Symptôme** : `soil_hum: 5939.5%` au lieu de `45%`  
**Solution** : Utiliser `readUint16BE()` pas `readUint16LE()`

### 3. Mauvais pin I2C AHT20
**Symptôme** : `AHT20 Fail` au boot  
**Solution** : Vérifier SDA=21, SCL=22 (pas 22/23)

### 4. MOSFET sur GPIO27
**Symptôme** : MQ ne chauffent pas, toujours froids  
**Solution** : Déplacer sur GPIO4

### 5. Timing trop court
**Symptôme** : Valeurs MQ instables (pic aléatoires)  
**Solution** : Attendre 10min de préchauffe (pas 2min)

---

## 📦 Fichiers concernés

### À déplacer en archive
```
apport/
├── Rapport1.docx           → docs/legacy_v1/
├── Anexe technique.docx    → docs/legacy_v1/
├── Lorawan.docx            → docs/legacy_v1/
├── Prise de mesure.docx    → docs/legacy_v1/
└── 📄 Annexe Électrique_.docx → docs/legacy_v1/
```

### À utiliser (V2)
```
docs/v2/
├── WIRING_V2.md        # Pinout à jour
├── PROTOCOL_V2.md      # Format trame
├── POWER_V2.md         # Alimentation LiFePO4
└── (ce fichier)        # CHANGELOG
```

---

## ✅ Checklist migration

- [ ] Débrancher alimentation
- [ ] Déplacer MOSFET GPIO27 → GPIO4
- [ ] Déplacer AHT20 (SDA 22→21, SCL 23→22)
- [ ] Déplacer TX UART 17→18
- [ ] Ajouter SCD41 sur 13/14
- [ ] Ajouter NPK sur 16/17/5
- [ ] Ajouter fil Wake 23→RST
- [ ] Vérifier pont diviseur GPIO34
- [ ] Flasher émetteur V2
- [ ] Flasher récepteur V2
- [ ] Mettre à jour payload formatter TTN
- [ ] Tester première transmission
- [ ] Vérifier valeurs NPK (cohérentes)
- [ ] Archiver docs V1

---

## 🗓️ Historique

- **2025** : Développement V1 (prototype)
- **Janvier 2026** : Migration V2 (production)
  - Ajout capteurs sol (NPK)
  - Optimisation énergie (4h cycle)
  - Correction pins (GPIO4, 21/22)
  - Ajout CRC (fiabilité)

---

## 💡 Pourquoi ces changements ?

| Changement | Justification technique |
|------------|------------------------|
| **GPIO4** | GPIO27 parfois utilisé par LED onboard sur certains devboards |
| **I2C 21/22** | GPIO22/23 sont aussi pins UART0 (conflit potentiel) |
| **10min préchauffe** | MQ137/MQ4/MQ7 nécessitent 5-10min pour stabilité R0 |
| **4h sleep** | Compost évolue lentement, 6 points/jour suffisent |
| **CRC16** | Risque de bit error sur UART filaire (interférences) |
| **LiFePO4** | 2000+ cycles vs 300-500 pour AGM |
| **MPPT** | Rendement hivernal critique pour autonomie |

---

*Document de référence pour la migration V1→V2*
