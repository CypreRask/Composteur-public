# 🌳 SmartTree : L'Encyclopédie Interactive (Bio Végétale)

> **Objectif** : Transformer l'arbre en un cours de biologie végétale complet et interactif. Du pixel art macroscopique jusqu'au schéma moléculaire animé.

---

## 🍃 MODULE 1 : LA FEUILLE (L'Usine Photochimique)

### 1. Niveau Macro : L'Échange
*   **Visuel** : Coupe transversale de feuille.
*   **Mécanique** :
    *   **Stomates** : Gardiens de la porte. Ils s'ouvrent/ferment selon l'hydratation (Turgescence).
    *   **Flux** : Entrée CO2 / Sortie O2 + H2O (Transpiration).

### 2. Niveau Nano : Le Chloroplaste (Mode "Story") 🎓
*Le joueur avance étape par étape (Click-to-Next) pour comprendre les schémas complexes.*

#### Schéma A : La Chaîne Photosynthétique (Membrane Thylakoïde)
*Simplification Pixel Art du schéma "Membrane".*
1.  **L'Attaque Solaire** :
    *   *Action* : Joueur clique sur le Soleil.
    *   *Visuel* : Photon ⚡ frappe **PS2** (Vert).
2.  **L'Eau Sacrifiée (Photolyse)** :
    *   *Action* : Zoom sur PS2.
    *   *Visuel* : Molécule H2O se brise. **O2** s'envole (On respire !), **H+** reste, **e-** (électron) part dans la chaîne.
3.  **Le Voyage de l'Électron** :
    *   *Visuel* : L'électron saute : PS2 -> PQ -> Cyt -> PC -> PS1.
    *   *Effet* : A chaque saut, il pompe des H+ vers l'intérieur (Gonflage de batterie).
4.  **La Turbine (ATP Synthase)** :
    *   *Visuel* : Les H+ sortent par la turbine (gros moteur rotatif).
    *   *Résultat* : Création d'ATP (L'énergie pure).

#### Schéma B : Le "Z-Scheme" (Échelle d'Énergie)
*Visualisation graphique de l'énergie de l'électron (Axe Y = Énergie).*
*   **État Bas** : Électron dans l'eau (Fatigué).
*   **Flash 1 (PS2)** : L'électron grippe tout en haut du graphique (Boosté !).
*   **Descente** : Il perd de l'énergie en travaillant (Chaîne de transport).
*   **Flash 2 (PS1)** : Re-boost solaire pour le sprint final vers le NADPH (Transporteur final).

### 3. Les Adaptations Métaboliques (C3 / C4 / CAM)
*Selecteur Interactif pour comparer :*
*   **C3 (Classique - ex: Pommier)** : Tout se fait au même endroit. Risque de "Photorespiration" si chaud (la plante suffoque).
*   **C4 (Tropical - ex: Maïs)** : Séparation spatiale. La capture du CO2 est faite dans une cellule à part. Plus efficace sous forte chaleur.
*   **CAM (Aride - ex: Cactus)** : Séparation temporelle. Ouvre les stomates la nuit (stocke le CO2), ferme le jour (photosynthèse).

---

## 🪵 MODULE 2 : LE TRONC (La Pompe & L'Autoroute)

### 1. Le Transport (Xylème vs Phloème)
*   **Le Xylème (Sève Brute ⬆️)** :
    *   *Moteur* : La **Théorie de la Tension-Cohésion**.
    *   *Visuel* : Les molécules d'eau se "tiennent la main" (liens hydrogène). L'évaporation en haut tire toute la chaîne vers le haut (comme une corde).
    *   *Cavitation* : Si trop chaud/sec, la chaîne casse (bulle d'air) -> Embolie de l'arbre.
*   **Le Phloème (Sève Élaborée ⬇️)** :
    *   *Contenu* : Eau chargée de sucres (sirop).
    *   *Moteur* : Pression osmotique. Distribution vers les puits (racines, fruits).

### 2. La Croissance (Dendrochronologie)
*   **Le Cambium** : La couche de cellules souches.
*   **Cernes** :
    *   *Printemps* : Gros vaisseaux (clair) pour boire vite.
    *   *Été/Automne* : Petits vaisseaux (foncé) pour la structure.
    *   *Lecture* : On peut lire l'histoire climatique de l'arbre.

---

## 🪱 MODULE 3 : LES RACINES (L'Interface Sol)

### 1. La Nutrition Minérale
*   **C.E.C (Capacité d'Échange Cationique)** :
    *   Le sol (Argile/Humus) est chargé négativement (-). Il retient les nutriments positifs (K+, Ca², Mg²+).
    *   *L'Échange* : La racine relâche des ions H+ (Acide) pour "décrocher" les nutriments et les boire.
    *   *Jeu* : "Équilibre le pH pour manger".

### 2. La Symbiose (Le Super-Pouvoir)
*   **Mycorhizes (Champignons)** :
    *   Extension du réseau. La plante donne 20% de son sucre en échange d'eau/phosphore inaccessibles.
*   **Nodosités (Bactéries)** :
    *   *Si Légumineuse* : Les bactéries *Rhizobium* squattent les racines.
    *   *Alchimie* : Elles cassent l'Azote de l'air (N2, inerte) pour en faire de l'Ammoniac (NH3, engrais).

---

## 🗺️ PROJET D'IMPLÉMENTATION

### Phase 1 : Structure Graphique
*   Créer le "Navire Arbre" : Un sprite géant cliquable.

### Phase 2 : Les Modales "Cours"
*   Développer des vues schématiques animées (non-réalistes, pédagogiques) pour chaque processus.
*   Utiliser des particules pour les molécules (H2O, CO2, e-).

### Phase 3 : Gamification
*   **Quiz Bio** : "Quelle plante survit le mieux au désert (CAM) ?"
*   **Gestion** : "Attention, embolie gazeuse imminente ! Arrose !"
