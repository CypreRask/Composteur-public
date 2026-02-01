# 📡 Protocole de Communication V2

> **SOURCE DE VÉRITÉ** : `v2/emetteur/emetteur.ino` + `v2/recepteur/recepteur.ino`

---

## 🔄 Vue d'ensemble

```
┌─────────────┐    UART 36B    ┌─────────────┐    LoRaWAN 32B    ┌─────┐
│ ESP32       │ ─────────────→ │ Heltec      │ ────────────────→ │ TTN │
│ Émetteur    │   9600 baud    │ Récepteur   │    (payload)      │     │
└─────────────┘                └─────────────┘                   └─────┘
```

**Deux formats différents** :
- **UART** (émetteur → récepteur) : **36 bytes** (header + len + payload + CRC)
- **LoRaWAN** (récepteur → TTN) : **32 bytes** (payload uniquement)

---

## 📦 Format UART (36 bytes)

Utilisé entre l'émetteur et le récepteur Heltec.

```
┌────────┬────────┬──────────────────────────────┬────────┬────────┐
│ Header │ Length │          Payload             │ CRC_L  │ CRC_H  │
│ 0xBB   │  0x20  │         32 bytes             │ 1 byte │ 1 byte │
│ 1 byte │ 1 byte │                              │        │        │
└────────┴────────┴──────────────────────────────┴────────┴────────┘

Total : 36 bytes
```

### Structure détaillée

| Offset | Taille | Champ | Description |
|--------|--------|-------|-------------|
| 0 | 1 | Header | `0xBB` (fixe) |
| 1 | 1 | Length | `0x20` = 32 (taille payload) |
| 2-33 | 32 | Payload | Voir tableau ci-dessous |
| 34 | 1 | CRC16_L | CRC16 little-endian (octet faible) |
| 35 | 1 | CRC16_H | CRC16 little-endian (octet fort) |

### Payload (32 bytes)

**⚠️ ENDIANNESS MIXTE** :
- MQ/SCD/AHT : **Little Endian**
- NPK : **Big Endian** (capteur RS485 natif)

| Offset | Champ | Type | Facteur | Endian |
|--------|-------|------|---------|--------|
| 0 | frameCounter | uint8 | 1 | - |
| 1-2 | mq137 | uint16 | raw ADC | LE |
| 3-4 | mq4 | uint16 | raw ADC | LE |
| 5-6 | mq7 | uint16 | raw ADC | LE |
| 7-8 | scd_co2 | uint16 | ppm | LE |
| 9-10 | scd_temp | int16 | ÷100 (°C) | LE |
| 11-12 | scd_hum | uint16 | ÷100 (%) | LE |
| 13-14 | aht_temp | int16 | ÷100 (°C) | LE |
| 15-16 | aht_hum | uint16 | ÷100 (%) | LE |
| 17-18 | **soil_hum** | uint16 | ÷10 (%) | **BE** ⚠️ |
| 19-20 | **soil_temp** | int16 | ÷10 (°C) | **BE** ⚠️ |
| 21-22 | **soil_ec** | uint16 | µS/cm | **BE** ⚠️ |
| 23-24 | **soil_ph** | uint16 | ÷10 | **BE** ⚠️ |
| 25-26 | **soil_n** | uint16 | mg/kg | **BE** ⚠️ |
| 27-28 | **soil_p** | uint16 | mg/kg | **BE** ⚠️ |
| 29-30 | **soil_k** | uint16 | mg/kg | **BE** ⚠️ |
| 31 | padding | uint8 | - | - |

---

## 📡 Format LoRaWAN (32 bytes)

Le récepteur vérifie le CRC sur la trame UART, puis envoie **uniquement le payload** (32 bytes) sur LoRaWAN.

**Pourquoi 32 et pas 36 ?**
- Le header (0xBB) et length (0x20) sont implicites
- Le CRC est vérifié par le récepteur, inutile de l'envoyer
- Économie de bandwidth LoRaWAN

```
┌──────────────────────────────────────────────────────────────┐
│                         Payload                              │
│                        32 bytes                              │
│           (même structure que ci-dessus)                     │
└──────────────────────────────────────────────────────────────┘
```

---

## 🔐 CRC16

**Algorithme** : Modbus/IBM (CRC-16)

```cpp
uint16_t calculateCRC16(uint8_t *data, size_t len) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < len; i++) {
    crc ^= data[i];
    for (int j = 0; j < 8; j++) {
      if ((crc & 0x0001) != 0) {
        crc >>= 1;
        crc ^= 0xA001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}
```

**Important** : Le CRC est calculé sur les **32 bytes de payload uniquement**, pas sur le header.

---

## ⏱️ Timing du cycle

```
┌──────────────────────────────────────────────────────────────────┐
│  T+0          T+10min           T+11min                T+4h10min  │
│   │              │                 │                       │      │
│   ▼              ▼                 ▼                       ▼      │
│ ┌──────┐    ┌────────┐      ┌──────────┐            ┌──────────┐ │
│ │WAKE  │    │MEASURE │      │ SEND     │            │ SLEEP    │ │
│ │Start │───→│Read all│─────→│UART→Heltec│───────────→│4h cycle │ │
│ │heat  │    │sensors │      │LoRaWAN   │            │          │ │
│ └──────┘    └────────┘      └──────────┘            └──────────┘ │
│                                                                      │
│ Preheat: 10 min                                                      │
│ UART window: ~5s après réveil Heltec                                │
│ Sleep: 4h (4 * 60 * 60 * 1e6 µs)                                    │
└──────────────────────────────────────────────────────────────────┘
```

**Note** : Le temps total de cycle est **4h + 10min** (pas 4h pile).

---

## 📋 Différences V1 → V2

| Aspect | V1 (OBSOLÈTE) | V2 (ACTUEL) |
|--------|---------------|-------------|
| **Header** | `0xAA` | `0xBB` |
| **Taille** | 12 bytes | 36 bytes UART / 32 bytes LoRaWAN |
| **Timing** | 2min preheat, 45min sleep | **10min preheat, 4h sleep** |
| **CRC** | Aucun | **CRC16 Modbus** |
| **NPK** | Non présent | **Ajouté en BE** |

---

## 🔗 Fichiers associés

- **Formatter TTN** : `v2/ttn-payload-formatter.js`
- **Code émetteur** : `v2/emetteur/emetteur.ino`
- **Code récepteur** : `v2/recepteur/recepteur.ino`
