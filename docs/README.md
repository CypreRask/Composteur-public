# 📚 Documentation Composteur V2

Bienvenue dans la documentation du projet Composteur IoT.

---

## 🗺️ Guide de navigation

### 🎯 Pour commencer

| Si vous cherchez... | Allez voir... |
|---------------------|---------------|
| Vue d'ensemble du projet | [`../README.md`](../README.md) |
| Architecture complète (schémas) | [`ARCHITECTURE.md`](ARCHITECTURE.md) |
| Différences V1 vs V2 | [`CHANGELOG_V1_V2.md`](CHANGELOG_V1_V2.md) |

### 🔧 Documentation technique V2 (Active)

**⚠️ Source de vérité pour le montage actuel**

| Document | Contenu | Public |
|----------|---------|--------|
| [`v2/WIRING_V2.md`](v2/WIRING_V2.md) | Pinout GPIO complet, tableau connexions | Électronicien |
| [`v2/PROTOCOL_V2.md`](v2/PROTOCOL_V2.md) | Format trame UART (36B) / LoRaWAN (32B), CRC | Développeur firmware |
| [`v2/POWER_V2.md`](v2/POWER_V2.md) | Chaîne d'alimentation LiFePO4/MPPT | Électronicien |
| [`v2/CALCULS_TECHNIQUES.md`](v2/CALCULS_TECHNIQUES.md) | **Formules, calculs dimensionnants, analyses** | Ingénieur |

### 🎨 Frontend & Design

| Document | Contenu | Public |
|----------|---------|--------|
| [`design_system.md`](design_system.md) | Règles pixel art (couleurs, pas d'emojis...) | Designer/UI |
| [`monitor.md`](monitor.md) | Architecture web monitor | Développeur web |
| [`tree_design.md`](tree_design.md) | Modules pédagogiques biologie | Contenu éducatif |
| [`eco_bible.md`](eco_bible.md) | Écosystème compost (bestiaire, cycles) | Contenu éducatif |

### ⚠️ Archive V1 (Obsolète)

**NE PAS UTILISER pour un nouveau montage**

[`legacy_v1/README.md`](legacy_v1/README.md) - Explication et liste des docs V1 (GPIO27, header 0xAA, 12 bytes...)

---

## 🔄 Workflow documentation

```
Problème montage
       │
       ▼
┌──────────────┐
│ Pin correct ? │──Non──► Consulter WIRING_V2.md
│ (GPIO4,21/22) │
└──────────────┘
       │ Oui
       ▼
┌──────────────┐
│ Trame OK ?    │──Non──► Consulter PROTOCOL_V2.md
│ (0xBB,36B,CRC)│
└──────────────┘
       │ Oui
       ▼
┌──────────────┐
│ Alim OK ?     │──Non──► Consulter POWER_V2.md
│ (LiFePO4/MPPT)│
└──────────────┘
       │ Oui
       ▼
   Ça marche !
```

---

## 📋 Résumé des changements V2

```diff
+ GPIO4 (MOSFET)      - GPIO27 (obsolète)
+ GPIO21/22 (AHT20)   - GPIO22/23 (obsolète)
+ GPIO18 (UART TX)    - GPIO17 (obsolète, conflit NPK)
+ GPIO16/17/5 (NPK)   - Nouveau
+ GPIO13/14 (SCD41)   - Nouveau
+ GPIO23 (Wake)       - Nouveau
+ Header 0xBB         - 0xAA (obsolète)
+ 36 bytes (UART)     - 12 bytes (obsolète)
+ CRC16               - Aucun (obsolète)
+ 10min/4h cycle      - 2min/45min (obsolète)
+ LiFePO4 + MPPT      - AGM + PWM (obsolète)
```

---

## 🆘 Support

En cas de doute entre deux documents :
1. **La source de vérité est le code** (`v2/emetteur/emetteur.ino`)
2. **Ensuite les docs `/docs/v2/`**
3. **Jamais les `.docx` de `/docs/legacy_v1/` (V1)**

---

*Structure mise à jour : Janvier 2026*
