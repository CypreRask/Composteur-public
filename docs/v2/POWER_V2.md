# ⚡ Alimentation Électrique V2

> **Architecture** : Panneau solaire → MPPT → Batterie LiFePO4 → Buck → Carte d'extension

---

## 🔋 Chaîne d'alimentation complète

```
Panneau     MPPT        Batterie      Buck        Carte        Modules
Solaire    (régulateur)  LiFePO4    (8-40V→12V)  Extension   (5V/3.3V)
   │           │           │           │            │            │
   ▼           ▼           ▼           ▼            ▼            ▼
┌─────┐    ┌──────┐    ┌──────┐    ┌─────┐     ┌────────┐    ┌────────┐
│ 12V │───→│ Gestion│───→│ 12V  │───→│ 12V │────→│ 5V/3.3V│───→│ Capteurs│
│     │    │ charge │    │stable│    │stable│    │ régulé │    │ (I2C)  │
└─────┘    └──────┘    └──────┘    └─────┘     └────────┘    └────────┘
   │                                                  │
   │                                                  ▼
   │                                             ┌────────┐
   │                                             │ MOSFET │───→ MQ (chauffe)
   │                                             │ GPIO4  │     5V coupable
   │                                             └────────┘
   │
   └───────────────────────────────────────────────────────────────→
                                    (Alim directe NPK 5V-12V)
```

---

## 🔧 Composants détaillés

### 1. Batterie : LiFePO4 (remplace AGM V1)

| Caractéristique | Valeur |
|-----------------|--------|
| **Type** | LiFePO4 (Lithium Fer Phosphate) |
| **Tension** | 12.8V nominale (3.2V × 4 cellules) |
| **Avantages** | +2000 cycles, pas d'effet mémoire, stable |
| **VS V1** | Remplace l'AGM (plomb) moins durable |

**⚠️ Contradiction V1 corrigée** : Les annexes V1 mentionnaient AGM → maintenant LiFePO4.

### 2. Régulateur MPPT (remplace PWM V1)

| Caractéristique | Valeur |
|-----------------|--------|
| **Type** | MPPT (Maximum Power Point Tracking) |
| **Entrée** | Panneau solaire (18-24V typiquement) |
| **Sortie** | Charge batterie LiFePO4 (14.4V max) |
| **VS V1** | Remplace PWM (moins efficace) |

**Pourquoi MPPT ? Calcul du Rendement**

Formule de puissance panneau solaire :
```
P = Vmp × Imp (tension et courant au point de puissance max)
```

**Comparaison MPPT vs PWM** :

| Condition | PWM | MPPT | Gain |
|-----------|-----|------|------|
| Plein soleil | 85% | 98% | +13% |
| Hiver/faible luminosité | 60% | 95% | **+35%** |
| Batterie déchargée | 70% | 97% | +27% |

**Calcul du gain hivernal** (cas critique) :
```
Panneau 20W :
- Avec PWM : 20W × 60% = 12W utiles
- Avec MPPT : 20W × 95% = 19W utiles
- Gain : 19W - 12W = +7W (+58%)
```

**Point de fonctionnement** :
- Vpanneau (Voc) ≈ 22V
- Vbatterie = 12.8V
- PWM : force Vpanneau = 12.8V (perte de 40% de la puissance)
- MPPT : maintient Vpanneau à Vmp (≈18V), convertit avec rendement 95%

> **Conclusion** : En hiver, MPPT récupère jusqu'à 2× plus d'énergie que PWM.

### 3. Buck Post-MPPT (stabilisation 12V)

```
Entrée : 8-40V (sortie MPPT/batterie)
Sortie : 12V stable
Usage  : Alimentation carte d'extension
```

**⚠️ Précision** : Ce n'est PAS un 12V→5V comme en V1. C'est un buck qui prend la tension variable batterie/panneau et sort du 12V stable.

### 4. Carte d'Extension (distribution)

| Entrée | Sorties |
|--------|---------|
| 12V (buck) | 5V régulé (capteurs) |
| | 3.3V régulé (ESP32, I2C) |
| | MOSFET 5V (MQ coupables) |

**Rôle** : Point central de distribution avec régulateurs propres.

---

## ⚡ Consommation détaillée

### Mode Mesure (actif ~11 minutes)

| Composant | Consommation | Gestion |
|-----------|--------------|---------|
| ESP32 Active | ~80mA @ 3.3V | - |
| SCD41 | ~15mA @ 3.3V | Toujours on |
| AHT20 | ~0.5mA @ 3.3V | Toujours on |
| MQ137/4/7 (chauffe) | ~150mA × 3 = 450mA @ 5V | **MOSFET GPIO4** |
| NPK RS485 | ~20-50mA @ 5V | Veille <5mA |
| **Total** | **~600-700mA** | - |

### Mode Sleep (4h)

| Composant | Consommation |
|-----------|--------------|
| ESP32 Light Sleep | ~10µA |
| NPK Veille | <5mA |
| **Total** | **~5mA** |

### Calcul Autonomie Détaillé

#### Bilan Énergétique par Cycle

**Phase Active** (~11 min) :
```
P_active = P_ESP32 + P_SCD41 + P_AHT20 + P_MQ + P_NPK
         = (3.3V × 0.08A) + (3.3V × 0.015A) + (3.3V × 0.0005A) + (5V × 0.45A) + (5V × 0.035A)
         = 0.264W + 0.0495W + 0.00165W + 2.25W + 0.175W
         = 2.74W

E_active = P_active × t_active
         = 2.74W × (11/60)h
         = 0.502Wh = 502mWh
```

**Phase Sleep** (4h) :
```
P_sleep = P_ESP32_sleep + P_NPK_veille + P_regulateurs
        = (3.3V × 0.00001A) + (5V × 0.005A) + 0.01W
        = 0.033mW + 25mW + 10mW
        = 35mW

E_sleep = 35mW × 4h = 140mWh
```

**Total par cycle** (4h11min) :
```
E_cycle = E_active + E_sleep
        = 502mWh + 140mWh
        = 642mWh

I_moyen = E_cycle / V_batterie / T_cycle
        = 642mWh / 12.8V / 4.18h
        = 12mA (moyenne sur cycle)
```

#### Autonomie sans Solaire

**Capacité batterie** (exemple 10Ah LiFePO4) :
```
E_batterie = 12.8V × 10Ah = 128Wh = 128000mWh
Autonomie = E_batterie / E_cycle
          = 128000 / 642
          = 199 cycles
          = 199 × 4.18h
          = 831 heures
          = **34.6 jours** (≈ 5 semaines)
```

**Autonomie avec différentes capacités** :

| Capacité | Énergie | Autonomie | Cycles |
|----------|---------|-----------|--------|
| 5Ah | 64Wh | **17 jours** | 100 |
| 10Ah | 128Wh | **35 jours** | 200 |
| 20Ah | 256Wh | **70 jours** | 400 |
| 50Ah | 640Wh | **175 jours** | 1000 |

---

## 🔌 Alimentation spécifique par module

### Capteurs I2C (AHT20, SCD41)
- **Tension** : 3.3V (via carte extension)
- **Source** : Régulateur 3.3V intégré
- **Filtrage** : Condensateur 100nF près de chaque capteur

### Capteurs MQ (137, 4, 7)
- **Tension** : 5V (chauffe filament)
- **Contrôle** : MOSFET GPIO4 (coupable)
- **Consommation** : ~150mA chacun en chauffe
- **⚠️ Danger** : Ne jamais laisser chauffer sans surveillance (risque incendie)

### Capteur NPK RS485
- **Tension module** : 5V (logique)
- **Tension capteur** : 5V-12V externe (pas via ESP32)
- **Interface** : Module MAX485

### ESP32
- **Tension** : 3.3V via régulateur carte extension
- **Alimentation** : Via pin 5V ou USB (selon mode prog)

---

## ⚠️ Sécurités électriques

### Protection MOSFET (GPIO4)
```
GPIO4 ───[220Ω]───┬── Gate
                  │
                 [10kΩ]
                  │
                 GND
```
- **220Ω** : Limite courant GPIO (protection)
- **10kΩ** : Pull-down (sûreté si reboot)

### Protection ADC (GPIO34)
Pont diviseur 2.2kΩ/4.7kΩ pour ramener 0-5V → 0-3.4V

### Protection RS485
- Bornier A/B avec vis
- Pas de masse commune obligatoire (différentiel)

---

## 🔄 Différences V1 → V2

| Aspect | V1 (OBSOLÈTE) | V2 (ACTUEL) |
|--------|---------------|-------------|
| **Batterie** | AGM plomb | **LiFePO4** |
| **Régulateur charge** | PWM | **MPPT** |
| **Conversion** | 12V → 5V DC-DC externe | **Buck 8-40V → 12V** + carte extension |
| **Distribution** | Directe filaire | **Carte d'extension centrale** |

---

## 📋 Checklist installation

- [ ] Batterie LiFePO4 chargée à 100%
- [ ] MPPT configuré pour LiFePO4 (14.4V max)
- [ ] Buck sort du 12V stable
- [ ] Carte extension alimentée en 12V
- [ ] Tous les GND sont communs (émetteur-récepteur-capteurs)
- [ ] MOSFET commandé par GPIO4 (pas 27 !)
- [ ] Pont diviseur présent sur SIG (GPIO34)

---

## 🔗 Fichiers associés

- **Pinout** : `docs/v2/WIRING_V2.md`
- **Code source** : `v2/emetteur/emetteur.ino`
- **Archives V1** : `docs/legacy_v1/` (AGM/PWM obsolètes)
