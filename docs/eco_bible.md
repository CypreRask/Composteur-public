# 🌿 L'Écosystème Numérique - Documentation de Référence

Ce document sert de "Bible" pour la représentation biologique et environnementale du projet. Il définit ce qui habite chaque zone, comment c'est représenté (Pixel Art), et les cycles qui les relient.

---

## 🏡 LE COMPOSTEUR (CompostCabin)

C'est le cœur du réacteur. Un milieu artificiel dense et chaud.

### 🍰 Les Strates (Couches)

| Strate | Nom Scientifique | État | Visuel (Pixel Art) | Temps Moyen |
| :--- | :--- | :--- | :--- | :--- |
| **1. Surface** | **Litière (Mésophile)** | Frais | Déchets identifiables (Pommes, Feuilles). Texture aérée. | 1-2 semaines |
| **2. Cœur** | **Thermophile** | Actif | Masse pulsante marron/rouge. Vapeur si > 50°C. Texture dense. | 2-4 semaines |
| **3. Fond** | **Maturation** | Stable | Terreau noir (Humus). Texture riche et grumeleuse (C.A.H). | 3-6 mois |

### 🐛 Bestiaire du Composteur

| Nom | Zone | Rôle | Représentation Visuelle | Condition Apparition |
| :--- | :--- | :--- | :--- | :--- |
| **Bactéries** | Cœur (Chaud) | Chauffage (Fermentation) | Particules vibrantes, nuages colorés. | Temp > 20°C |
| **Actinobactéries** | Cœur (Fin de chauffe) | "Blanchiment" | Filaments blancs (souvent confondu avec champi). | Temp > 40°C |
| **Vers Épigés** | Surface | Mangeurs de litière | Vers rouges, petits, très vifs. | Temp < 30°C (Fuit le chaud) |
| **Cloportes** | Surface | Découpeurs (Bois) | Petits blindés gris. | Humidité élevée |
| **Soldats Noirs** | Surface | Voraces | Larves blanches segmentées (Asticots). | Présence viandes/fruits sucrés |

---

## 🌍 LE SOL (Underground)

Le milieu naturel sous le composteur. Un écosystème plus lent et structuré.

### 🏗️ Structure Géologique

| Élément | Description | Visuel |
| :--- | :--- | :--- |
| **Argile** | Particules fines minérales | Disques/Particules Bleues. |
| **Sables/Limos** | Structure drainante | Particules Jaunes/Beiges. |
| **C.A.H** | Le "Frigo" du sol | Complexe **Argile (Bleu) - Calcium (Jaune) - Humus (Marron)**. |

### 🐜 Bestiaire du Sol

| Nom | Type | Rôle | Visuel & Animation |
| :--- | :--- | :--- | :--- |
| **Lombric Anécique** | Ver Vertical | Laboureur | ✅ Gros, Sombre, Rugueux. Animation : Verticale "Stop & Go". |
| **Lombric Endogé** | Ver Horizontal | Aérateur | ✅ Fin, Rose pâle. Animation : Horizontale + Vibration. |
| **Collembole** | Sauteur | Nettoyeur | ✅ Pixel Blanc. Animation : Sauts brusques. |
| **Taupe/Rongeur** | Mammifère | Bioturbation | Sprite Blocky (Mulot/Campagnol) qui passe. |
| **Mycélium** | Champignon | Réseau | Toile blanche fine connectant les plantes. |

---

## 🔄 LES CYCLES (Flux)

Les règles invisibles qui régissent la simulation.

### 1. Cycle de l'Azote (N)
*   **Source** : Déchets Verts (Épluchures) + Urine (si on est courageux).
*   **Flux** : La décomposition libère de l'**Ammonium (NH4+)**.
*   **Danger** : Si pas d'air (Anaérobie) -> **Ammoniac (NH3)** (Ça pue ! 🤢).
*   **Transformation** : Transformé en **Nitrates (NO3-)** pour les plantes.

### 2. Cycle du Carbone (C)
*   **Source** : Déchets Bruns (Carton, Feuilles mortes, Bois).
*   **Flux** : C'est le "Carburant" des bactéries pour chauffer.
*   **Résultat** : Une partie part en **CO2** (Respiration du tas), le reste devient de l'**Humus** stable (Stockage Carbone).

### 3. Cycle de l'Eau (H2O)
*   **Entrée** : Pluie (Sol) ou Arrosage/Déchets humides (Compost).
*   **Sortie** : Évaporation (Vapeur) ou Lessivage (Fond).
*   **Visuel** : Le sol s'assombrit, le C.A.H gonfle, les plantes verdissent.
