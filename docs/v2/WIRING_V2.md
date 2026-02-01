# 🔌 Pinout Officiel V2 - ESP32 Émetteur

> **SOURCE DE VÉRITÉ** : `v2/emetteur/emetteur.ino`  
> **Version** : V2 (remplace V1 obsolète avec GPIO27 MOSFET et I2C 22/23)

---

## 📍 Tableau complet des connexions

| Pin ESP32 | Fonction | Connecté à | Détails |
|-----------|----------|------------|---------|
| **GND** | Masse | Tous les GND | Commun impératif |
| **3V3** | Alim 3.3V | AHT20, SCD41, Mux | Capacité limitée, pas pour les MQ |
| **4** | **MOSFET Gate** | Gate du MOSFET N | ⚠️ **V2** : Anciennement GPIO27 en V1 |
| **21** | **I2C1 SDA** | AHT20 (SDA) | ⚠️ **V2** : Anciennement GPIO22 en V1 |
| **22** | **I2C1 SCL** | AHT20 (SCL) | ⚠️ **V2** : Anciennement GPIO23 en V1 |
| **13** | **I2C2 SDA** | SCD41 (SDA) | Bus secondaire (Wire1) |
| **14** | **I2C2 SCL** | SCD41 (SCL) | Bus secondaire (Wire1) |
| **34** | **Analog In** | Mux SIG | Entrée ADC (avec pont diviseur !) |
| **32** | Digital Out | Mux S0 | Sélection canal 0 |
| **33** | Digital Out | Mux S1 | Sélection canal 1 |
| **25** | Digital Out | Mux S2 | Sélection canal 2 |
| **26** | Digital Out | Mux S3 | Sélection canal 3 |
| **16** | **UART2 RX** | Module RS485 (RO) | Réception NPK |
| **17** | **UART2 TX** | Module RS485 (DI) | Émission NPK |
| **5** | **Digital Out** | Module RS485 (DE+RE) | Contrôle flux RS485 |
| **18** | **UART1 TX** | Récepteur Heltec (RX) | ⚠️ **V2** : GPIO18 (ancien GPIO17 utilisé par NPK) |
| **19** | UART1 RX | Récepteur Heltec (TX) | Optionnel (retour) |
| **23** | **Wake Signal** | Récepteur Heltec (RST) | Pulse reset pour réveiller |

---

## 🔗 Câblage Inter-cartes (Lien UART)

### ESP32 Émetteur → Heltec Récepteur

| Signal | Émetteur | → | Récepteur | Note |
|--------|----------|---|-----------|------|
| **TX** | GPIO **18** | → | GPIO **20** (RX) | Câble principal |
| **RX** | GPIO **19** | ← | GPIO **19** (TX) | Optionnel |
| **Wake** | GPIO **23** | → | Pin **RST** | Pulse 50ms |
| **GND** | GND | ↔ | GND | Commun obligatoire |

**Configuration UART** : 9600 baud, 8N1

---

## ⚡ Circuits de Puissance

### 1. MOSFET (Contrôle MQ)

```
GPIO 4 ───[220Ω]───┬── Gate (MOSFET N)
                   │
                  [10kΩ]
                   │
                  GND

MOSFET Drain ────┬─── GND des capteurs MQ
                 │
MOSFET Source ───┴─── GND ESP32
```

**Composants** :
- MOSFET Canal N (ex: IRLZ44N)
- Rgate = 220Ω (protection GPIO)
- Rpulldown = 10kΩ (état bas sûr au boot)

#### Calcul des Résistances

**1. Résistance de Gate (Rgate = 220Ω)**

Fonction : Limiter le courant de charge de la capacité de Gate du MOSFET.

```
Igate_max = V_GPIO / Rgate
          = 3.3V / 220Ω
          = 15mA < 40mA (max GPIO) ✅
```

Temps de commutation (Ciss ≈ 1.6nF pour IRLZ44N) :
```
tau = Rgate × Ciss = 220 × 1.6×10^-9 = 352ns
t_montée ≈ 3×tau ≈ 1µs
```

> Commutation quasi-instantanée, pertes par commutation négligeables.

**2. Résistance Pull-Down (Rpd = 10kΩ)**

Fonction : Forcer MOSFET OFF pendant boot (GPIO flottant).

```
I_pull-down = 3.3V / 10kΩ = 0.33mA (négligeable)
```

Tension Gate à l'état haut (diviseur résistif) :
```
Vgate = 3.3V × (Rpd / (Rgate + Rpd))
      = 3.3V × (10000 / 10220)
      = 3.23V > Vth (1-2V) ✅
```

**3. Pertes dans le MOSFET**

Avec Rds(on) = 22mΩ (IRLZ44N @ Vgs=3.3V) et I = 450mA (3 MQ) :
```
P = I² × Rds(on) = 0.45² × 0.022 = 4.5mW
```

Chauffe : ΔT = 4.5mW × 62°C/W = 0.28°C (négligeable)

**⚠️ ERREUR V1 CORRIGÉE** : La résistance 220Ω est entre GPIO et Gate, PAS dans la ligne de chauffe (risque de surchauffe des MQ).

### 2. Pont Diviseur (Protection ADC)

Entre `SIG` du mux et `GPIO 34` :

```
SIG (0-5V) ───[R1=2.2kΩ]───┬─── GPIO 34 (Vout)
                           │
                          [R2=4.7kΩ]
                           │
                          GND
```

#### Calcul Théorique

**Formule du pont diviseur** :
```
Vout = Vin × (R2 / (R1 + R2))
```

**Application numérique** (Vin = 5V) :
```
Vout = 5V × (4700Ω / (2200Ω + 4700Ω))
     = 5V × (4700 / 6900)
     = 5V × 0.681
     = 3.405V
```

**Marge de sécurité** :
- Vmax absolu ESP32 = 3.6V
- Notre Vout max = 3.405V
- **Marge = 195mV** ✅

**Impédance de sortie** (pour calcul de chargement ADC) :
```
Zout = (R1 × R2) / (R1 + R2)
     = (2200 × 4700) / 6900
     = 1499Ω ≈ 1.5kΩ
```

> L'impédance d'entrée de l'ADC ESP32 > 10MΩ, donc erreur de chargement négligeable (<0.01%).

**Résolution effective** :
```
Rapport = 0.681
Plage entrée effective = 0-5V
Plage ADC = 0-3.3V
Résolution = 5V / 4096 = 1.22mV/bit (côté capteur)
```

---

## 🔌 Modules détaillés

### Multiplexeur CD74HC4067

| Pin Mux | Connexion |
|---------|-----------|
| VCC | 3.3V |
| GND | GND |
| EN | GND (toujours actif) |
| SIG | Pont diviseur → GPIO 34 |
| S0-S3 | GPIO 32,33,25,26 |
| C0 | MQ137 (NH3) |
| C1 | MQ4 (CH4) |
| C2 | MQ7 (CO) |

### Module RS485 (Max485)

| Pin Module | Connexion |
|------------|-----------|
| VCC | 5V |
| GND | GND |
| RO | GPIO 16 (RX) |
| DI | GPIO 17 (TX) |
| DE + RE | GPIO 5 (liés ensemble) |
| A/B | Vers capteur NPK |

**Note** : Le capteur NPK lui-même nécessite une alimentation 5V-12V externe.

---

## ⚠️ Différences V1 → V2

| Élément | V1 (OBSOLÈTE) | V2 (ACTUEL) |
|---------|---------------|-------------|
| MOSFET MQ | GPIO 27 | **GPIO 4** |
| AHT20 SDA | GPIO 22 | **GPIO 21** |
| AHT20 SCL | GPIO 23 | **GPIO 22** |
| UART TX vers Heltec | GPIO 17 | **GPIO 18** (17 pris par NPK) |
| NPK RS485 | - | **GPIO 16/17/5** |
| SCD41 | - | **GPIO 13/14** |
| Wake Heltec | - | **GPIO 23** |

---

## 🔗 Fichiers sources

- **Code source** : `v2/emetteur/emetteur.ino`
- **Doc associée** : `v2/WIRING.md` (ce fichier)
- **Archives V1** : `docs/legacy_v1/` (ne pas utiliser)
