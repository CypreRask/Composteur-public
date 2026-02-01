# 🔌 Guide de Câblage - Composteur V2

Ce guide détaille les connexions à réaliser pour la nouvelle version du composteur sur l'**ESP32 Émetteur**.

## 🧠 ESP32 Emetteur - Pinout

| Pin ESP32 | Fonction | Connecté à... | Détails |
| :--- | :--- | :--- | :--- |
| **GND** | Masse | Tous les GND | Relier toutes les masses ensemble ! |
| **3V3** | Power 3.3V | AHT20, SCD41, NPK (VCC), Mux (VCC) | Attention, le NPK a besoin de 5V-30V sur son alim principale (Vin), pas 3.3V ! |
| **21** | I2C1 SDA | **AHT20** (SDA) | Bus I2C Principal (`Wire`) |
| **22** | I2C1 SCL | **AHT20** (SCL) | Bus I2C Principal (`Wire`) |
| **13** | I2C2 SDA | **SCD41** (SDA) | Bus I2C Secondaire (`Wire1`) |
| **14** | I2C2 SCL | **SCD41** (SCL) | Bus I2C Secondaire (`Wire1`) |
| **34** | Analog Input | **Multiplexeur** (SIG) | Sortie du signal analogique des gaz |
| **32** | Digital Out | **Multiplexeur** (S0) | Sélection canal |
| **33** | Digital Out | **Multiplexeur** (S1) | Sélection canal |
| **25** | Digital Out | **Multiplexeur** (S2) | Sélection canal |
| **26** | Digital Out | **Multiplexeur** (S3) | Sélection canal |
| **16** | UART RX | **Module RS485** (RO) | Réception NPK (RO = Receiver Output) |
| **17** | UART TX | **Module RS485** (DI) | Envoi NPK (DI = Driver Input) |
| **5** | Digital Out | **Module RS485** (DE + RE) | Contrôle Flux (Relier DE et RE ensemble) |
| **4** | Digital Out | **MOSFET Gate** | Pilotage alimentation des capteurs Gaz (Active HIGH) |
| **18** | UART TX | **ESP32 Récepteur** (RX) | Envoi des données vers le récepteur |
| **19** | UART RX | **ESP32 Récepteur** (TX) | (Optionnel) Retour du récepteur |
| **23** | GPO | **ESP32 Récepteur** (RST) | **Wake-Up Slave** (Fil de contrôle "WAKE") |

---

## 🧩 Détail des modules

### 1. Circuit de Puissance (MOSFET & Diviseur)
**A. Le MOSFET (Interrupteur MQs)**
*   **But** : Couper les capteurs gaz quand on ne lit pas (économie d'énergie + évite surchauffe).
*   **Type** : MOSFET Canal N (ex: IRLZ44N).
*   **Câblage** :
    *   **Source (S)** -> GND de l'ESP32.
    *   **Drain (D)** -> GND des Capteurs MQs. *Note : Le VCC des MQs reste branché au 5V permanent.*
    *   **Gate (G)** -> Pin **4** de l'ESP32 (via une résistance 100-200Ω).
    *   **Résistance Pull-Down** : Ajoute une résistance 10kΩ entre Gate et GND (Source) pour forcer l'état bas si l'ESP reboot.

**B. Pont Diviseur (Protection ADC)**
*   **But** : Réduire le signal 0-5V du Multiplexeur pour ne pas griller l'entrée 3.3V de l'ESP32.
*   **Emplacement** : Entre la sortie `SIG` du Multiplexeur et le Pin **34**.
*   **Composants** : R1 (Haut) et R2 (Bas).
*   **Valeurs suggérées** :
    *   R1 = 2.2kΩ (Entre SIG Mux et Pin 34)
    *   R2 = 4.7kΩ (Entre Pin 34 et GND)
    *   *Formule* : Vout = Vin * R2 / (R1 + R2) => 5V * 4.7 / 6.9 ~= 3.4V (C'est safe).

### 2. Multiplexeur (CD74HC4067 ou similaire)
*   **VCC** -> 3.3V
*   **GND** -> GND
*   **EN** (Enable) -> **GND** (Pour qu'il soit toujours activé)
*   **SIG** -> Pin 34 (ESP32)
*   **S0** -> Pin 32
*   **S1** -> Pin 33
*   **S2** -> Pin 25
*   **S3** -> Pin 26
*   **Entrées Capteurs Gaz** :
    *   **C0** -> MQ137 (NH3) Analog
    *   **C1** -> MQ4 (CH4) Analog
    *   **C2** -> MQ7 (CO) Analog

### 2. Capteurs I2C (Double Bus)
**Bus 1 : AHT20 (Temp/Hum)**
*   **VCC** -> 3.3V
*   **GND** -> GND
*   **SDA** -> Pin **21**
*   **SCL** -> Pin **22**

**Bus 2 : SCD41 (CO2)**
*   **VCC** -> 3.3V
*   **GND** -> GND
*   **SDA** -> Pin **13** (Revenu sur 13 !)
*   **SCL** -> Pin **14**
*   *Raison* : Plus de place sur le bornier principal. Utilise `Wire1` dans le code.

### 3. Module RS485 (Max485) pour NPK
*   **VCC** -> 5V (Le module RS485 aime mieux le 5V, attention aux niveaux logiques, mais souvent ça passe sur ESP32 si le module a son régulateur, sinon 3.3V).
*   **GND** -> GND
*   **RO** -> Pin 16 (ESP32)
*   **DI** -> Pin 17 (ESP32)
*   **DE** & **RE** -> Pin 5 (ESP32) (Relier les deux pins ensemble)
*   **Bornier A/B** -> Vers le capteur NPK (Fil A sur A, Fil B sur B).
*   *Alimentation NPK* : Le capteur NPK lui-même doit surement être alimenté en 12V ou 5V externe (pas par l'ESP32 !).

### 4. Liaison vers Récepteur
*   **ESP32 Emetteur (Pin 18)** -> vers **ESP32 Récepteur (RX - Pin 20)**
*   **GND** -> **GND** (Les masses doivent être communes entre les deux ESP !)
*   **WAKE / RST** : Relier le Pin **23** de l'Emetteur au Pin **RST** du Récepteur.
    *   *Sur la Heltec V3* : C'est le **Pin N°7** du connecteur de droite (Header J2), en comptant depuis le bas (juste au-dessus des pins TX/RX).
    *   *Note* : Cela permet à l'Emetteur de réveiller le Récepteur (qui dort profondément) uniquement quand une mesure est prête.
