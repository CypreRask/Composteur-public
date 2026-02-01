# 🧮 Calculs et Formules Techniques - Composteur V2

> **Document de référence** : Tous les calculs théoriques et analyses dimensionnantes

---

## 📐 1. Électronique Analogique

### 1.1 Pont Diviseur de Tension (Protection ADC)

**Schéma** :
```
Vin (0-5V) ──[R1=2.2kΩ]──┬── Vout (GPIO34)
                          │
                         [R2=4.7kΩ]
                          │
                         GND
```

**Formule** :
```
Vout = Vin × (R2 / (R1 + R2))
```

**Application** :
```
Vout = 5V × (4700 / (2200 + 4700))
     = 5V × (4700 / 6900)
     = 5V × 0.681
     = 3.405V
```

**Marge de sécurité** :
- Vmax ESP32 ADC = 3.3V (référence)
- Tolérance ESP32 = 3.6V (absolu max)
- Notre Vout max = 3.405V
- **Marge = 3.6V - 3.405V = 195mV** ✅

**Impédance de sortie** :
```
Zout = R1 // R2 = (R1 × R2) / (R1 + R2)
     = (2200 × 4700) / 6900
     = 1499Ω ≈ 1.5kΩ
```

> **Note** : L'ADC ESP32 a une impédance d'entrée > 10MΩ, donc 1.5kΩ est négligeable.

---

### 1.2 Résolution ADC et Quantification

**Caractéristiques ADC ESP32** :
- Résolution : 12 bits
- Niveaux : 2^12 = 4096 niveaux
- Tension de référence : 3.3V
- **LSB (pas de quantification)** = 3.3V / 4096 = **0.806mV**

**Avec pont diviseur** :
```
Rapport diviseur = 0.681
LSB équivalent en entrée = 0.806mV / 0.681 = 1.18mV (côté 5V)
```

**Précision sur la plage 0-5V** :
```
Résolution effective = 5V / 4096 = 1.22mV/bit
```

**Exemple MQ** : Si MQ sort 2.5V (milieu de plage)
- Valeur ADC lue = 2.5V × 0.681 = 1.703V
- Code ADC = 1.703V / 0.806mV = **2113**
- Retour calcul : 2113 × 0.806mV / 0.681 = **2.50V** ✅

---

### 1.3 MOSFET - Calcul des Résistances

#### Résistance de Gate (Rgate = 220Ω)

**Fonction** : Limiter le courant de charge/décharge de la capacité de Gate

**Calcul** :
```
Igate_max = VGPIO / Rgate
          = 3.3V / 220Ω
          = 15mA
```

**Vérification** : 15mA < 40mA (max GPIO ESP32) ✅

**Temps de commutation** (approximation) :
```
Ciss (IRLZ44N) ≈ 1.6nF
tau = Rgate × Ciss = 220 × 1.6×10^-9 = 352ns
t montée ≈ 3×tau = 1µs
```

> **Conclusion** : Commutation rapide, pertes par commutation négligeables.

#### Résistance Pull-Down (Rpd = 10kΩ)

**Fonction** : Forcer MOSFET OFF pendant boot (GPIO flottant)

**Calcul du courant** :
```
Ipd = VGPIO / Rpd
    = 3.3V / 10000Ω
    = 0.33mA
```

**Vérification** : 0.33mA négligeable vs consommation MQ (450mA) ✅

**Diviseur résistif** (état haut) :
```
Vgate = 3.3V × (Rpd / (Rgate + Rpd))
      = 3.3V × (10000 / 10220)
      = 3.23V
```

> Vgate = 3.23V > Vth (1-2V pour IRLZ44N) ✅ MOSFET bien saturé.

---

### 1.4 Pertes dans le MOSFET

**Paramètres** :
- Rds(on) IRLZ44N @ Vgs=3.3V ≈ 22mΩ (datasheet)
- Courant MQ : 450mA (3 capteurs × 150mA)

**Calcul** :
```
Pconduction = I² × Rds(on)
            = (0.45A)² × 0.022Ω
            = 0.2025 × 0.022
            = 4.45mW
```

**Chauffe** :
```
ΔT = P × RthJA (RthJA ≈ 62°C/W pour TO-220)
   = 0.00445W × 62
   = 0.28°C
```

> **Négligeable** : Le MOSFET ne chauffe pas.

---

## ⚡ 2. Calculs d'Énergie et Autonomie

### 2.1 Consommation par Phase

#### Phase Active (Mesure + Transmission)

| Composant | Tension | Courant | Puissance | Durée | Énergie |
|-----------|---------|---------|-----------|-------|---------|
| ESP32 Active | 3.3V | 80mA | 264mW | 11min | 48.4mWh |
| SCD41 | 3.3V | 15mA | 49.5mW | 11min | 9.1mWh |
| AHT20 | 3.3V | 0.5mA | 1.65mW | 11min | 0.3mWh |
| MQ (×3) | 5V | 450mA | 2.25W | 10min | 375mWh |
| NPK RS485 | 5V | 35mA | 175mW | 11min | 32.1mWh |
| **Total** | - | **~585mA** | **2.74W** | **11min** | **~465mWh** |

#### Phase Sleep

| Composant | Tension | Courant | Puissance | Durée | Énergie |
|-----------|---------|---------|-----------|-------|---------|
| ESP32 Light Sleep | 3.3V | 0.01mA | 33µW | 4h | 0.13mWh |
| NPK Veille | 5V | 5mA | 25mW | 4h | 100mWh |
| Régulateurs (quiescent) | - | ~2mA | ~10mW | 4h | 40mWh |
| **Total Sleep** | - | **~7mA** | **~35mW** | **4h** | **~140mWh** |

---

### 2.2 Calcul d'Autonomie Complète

**Énergie par cycle** (4h11min) :
```
E_cycle = E_active + E_sleep
        = 465mWh + 140mWh
        = 605mWh
```

**Capacité batterie** (exemple 10Ah LiFePO4) :
```
E_batterie = 12.8V × 10Ah = 128Wh = 128000mWh
```

**Nombre de cycles** :
```
N_cycles = E_batterie / E_cycle
         = 128000 / 605
         = 211 cycles
```

**Autonomie** :
```
T_autonomie = 211 cycles × 4.18h
            = 882 heures
            = 36.7 jours
            ≈ **37 jours sans soleil**
```

---

### 2.3 Bilan Énergétique avec Solaire

**Hypothèses hiver** (jour court, faible ensoleillement) :
- Ensoleillement effectif : 3h/jour
- Puissance panneau : 20W
- Rendement MPPT : 95%

**Énergie produite** :
```
E_produite = 20W × 3h × 0.95 = 57Wh/jour
E_consommée = 605mWh × (24h / 4.18h) = 3.47Wh/jour
```

**Bilan** :
```
E_excédent = 57Wh - 3.47Wh = 53.5Wh/jour
```

> **Conclusion** : Même en hiver, le système est largement autonome avec 20W de panneau.

---

### 2.4 Temps de Charge Batterie

**Capacité à recharger** (exemple après 10 jours sans soleil) :
```
E_consommée = 3.47Wh × 10 = 34.7Wh
Soit 27% de la capacité (128Wh)
```

**Courant de charge** (MPPT 20W, batterie 12.8V) :
```
I_charge = P_panneau / V_batterie
         = 20W / 12.8V
         = 1.56A
```

**Temps de charge** (rendement 95%) :
```
T_charge = (E_consommée / V) / (I_charge × rendement)
         = (34.7Wh / 12.8V) / (1.56A × 0.95)
         = 2.71Ah / 1.48A
         = 1.83 heures
         = **1h50 de soleil**
```

> **Conclusion** : 2 heures de soleil suffisent à recharger 10 jours de consommation.

---

## 📡 3. Communications

### 3.1 Débit UART et Temps de Transmission

**Paramètres** :
- Baudrate : 9600 bauds
- Format : 8N1 (8 bits données, 1 start, 1 stop, pas de parité) = 10 bits/caractère
- Taille trame : 36 bytes

**Calcul** :
```
T_transmission = (36 bytes × 10 bits) / 9600 bits/s
               = 360 / 9600
               = 37.5ms
```

**Avec redondance (×5)** :
```
T_total = 37.5ms × 5 + 200ms (délai entre envois)
        = 187.5ms + 800ms
        = 987.5ms ≈ **1 seconde**
```

---

### 3.2 Airtime LoRaWAN (Duty Cycle)

**Paramètres** (Europe 868MHz) :
- Spreading Factor : SF9 (vu dans tes logs TTN)
- Bandwidth : 125kHz
- Coding Rate : 4/5
- Payload : 32 bytes

**Formule** (simplifiée) :
```
T_air = T_preamble + T_payload

T_preamble = (4.25 + 8) × (2^SF / BW)
           = 12.25 × (512 / 125000)
           = 50ms

T_payload = 8 + ceil((8×32 - 4×SF + 28) / (4×SF)) × (CR + 4)
          = 8 + ceil((256 - 36 + 28) / 36) × 5.25
          = 8 + 7 × 5.25
          = 45 symboles

T_payload = 45 × (512 / 125000) = 184ms

T_air_total ≈ 50ms + 184ms = **234ms**
```

**Duty Cycle** (bande 867-868MHz : 1%) :
```
T_min_entre_transmissions = T_air / 0.01
                          = 234ms / 0.01
                          = 23.4 secondes
```

> **Conclusion** : Notre cycle de 4h respecte largement le duty cycle.

---

### 3.3 Portée LoRaWAN Estimée

**Link Budget** :
```
LB = P_tx + G_tx - L_tx + G_rx - L_rx - S_min

Avec :
- P_tx (Heltec) = +14dBm (25mW)
- G_tx = G_rx = 2dBi (antennes PCB)
- S_min (SF9) = -123dBm

LB = 14 + 2 + 2 - (-123) = 141dB
```

**Perte en espace libre** (Friis) :
```
FSPL(d) = 20×log10(d) + 20×log10(f) + 32.44

Pour f = 868MHz, distance 1km :
FSPL(1km) = 20×log10(1000) + 20×log10(868) + 32.44
          = 60 + 58.8 + 32.44
          = 151.2dB
```

**Distance max théorique** (espace libre) :
```
141dB = 20×log10(d) + 91.2
d = 10^((141-91.2)/20) = 10^2.49 = **310m**
```

**En environnement urbain** (perte -30dB) :
```
d_effective ≈ 50-100m
```

> **Observation** : Ton log montre -105 à -121dBm, donc ~50-100m avec obstacles, cohérent.

---

## 🌡️ 4. Capteurs - Calculs Physiques

### 4.1 Conversion Température (SCD41/AHT20)

**Principe** : Capteurs donnent une valeur sur 16 bits signée (×100)

**Formule générale** :
```
T(°C) = valeur_16bits / 100
```

**Exemple** :
```
Valeur brute = 2735 (0x0AAF)
Température = 2735 / 100 = 27.35°C
```

**Résolution** : 0.01°C (1/100)

---

### 4.2 Conversion MQ (ADC vers ppm - Approximation)

**Principe** : Les MQ donnent une résistance variable selon le gaz.

**Circuit** :
```
Vcc (5V) ──[RL]──┬── Vout (vers ADC)
                 │
              [Rs] (MQ)
                 │
                GND
```

**Formule** :
```
Rs = RL × (Vcc - Vout) / Vout
```

**Rapport Rs/R0** (R0 = résistance air pur) :
```
ratio = Rs / R0
```

**Concentration** (approximation polynomiale, dépend du MQ) :
```
ppm = a × (ratio)^b

Pour MQ-137 (NH3) : a ≈ 100, b ≈ -0.5 (à calibrer)
```

> **Note** : Sans calibration avec gaz étalon, on ne peut que mesurer des variations relatives.

---

## 📊 5. Statistiques et Précision

### 5.1 Erreur Relative du Système

**Sources d'erreur** :
- Référence ADC ESP32 : ±3% (interne)
- Pont diviseur (résistances 1%) : ±2%
- Capteur MQ (datasheet) : ±15%
- Capteur SCD41 : ±(40ppm + 5%) pour CO2

**Erreur totale estimée** (propagation) :
```
ΔT/T = √(3² + 2² + 15²) = √(9 + 4 + 225) = √238 ≈ ±15%
```

> **Conclusion** : Le système est précis pour tendances, pas pour mesures absolues (sauf SCD41 calibré).

---

## 🔗 Références

- **Datasheet IRLZ44N** : Rds(on), Vth, Ciss
- **Datasheet ESP32** : ADC specs, GPIO specs
- **LoRaWAN Regional Parameters** : Duty cycle, SF
- **Datasheet SCD41** : Précision CO2/temp

---

*Calculs vérifiés et cohérents avec le montage V2*
