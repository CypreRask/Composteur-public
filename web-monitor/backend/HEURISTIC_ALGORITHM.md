# Algorithme du Moteur Heuristique C/N

## Objectif
Ce document décrit la **Méthode d'Estimation Heuristique par Ratio** implémentée dans le système V2.
Cette méthode remplace l'approche par "Bilan de Masse" (qui manquait de données de flux d'air) par une **Estimation de Tendance** basée sur les ratios de gaz (R1, R2, R3) et des portes logiques.

## Principe de Fonctionnement
> [!NOTE]
> Cette méthode ne calcule pas la masse absolue C/N (kg). Elle fournit un **Score de Probabilité (0-100)** d'être dans la "Zone Efficace", ce qui est plus robuste avec des capteurs low-cost.

## Architecture du Moteur

### 1. Calcul des Indices (`heuristic_engine.py`)
Le module analyse les données historiques et calcule :
- **R1 (Ratio Activité)** : $NH_3 / CO_2$. Indique si la dégradation est équilibrée.
- **R2 (Ratio Anaérobie)** : $CH_4 / CO_2$. Indique la présence de poches anoxiques.
- **EC_Norm** : Conductivité normalisée pour estimer la maturité.

### 2. Logique de "Gating" (Portes)
Le système applique des règles strictes pour détecter les états critiques :
- **Porte 2 (Anaérobie)** : Si $CH_4$ > Seuil, le score chute drastiquement.
- **Porte 3 (Faible Activité)** : Si $CO_2$ est bas malgré une température correcte.
- **Porte 1 (Maturité)** : Si $CO_2$ baisse et EC se stabilise (détection de fin de cycle).

### 3. Calcul du Score Final
Si aucune porte critique n'est activée, le score est calculé par une formule pondérée :
$$ Score = 50 + \alpha \cdot \ln(R1) - \beta \cdot \ln(R2) + \gamma \cdot EC $$
Le résultat est lissé sur 24h (Moyenne Exponentielle) pour éviter le bruit capteur.

## Intégration Système

### Backend
- Le fichier `main.py` appelle `heuristic_engine` à chaque requête `/api/latest`.
- Il retourne :
    - `score` : 0 à 100.
    - `category` : "Faible", "Optimal", "Élevé".
    - `reliability` : Indicateur de confiance (basé sur la quantité de données).

### Frontend
- Le Tableau de Bord affiche ce score sous forme d'une jauge "C/N Index".
- Un code couleur (Vert/Orange/Rouge) indique immédiatement l'état de santé du compost.
- Les messages d'alerte (ex: "Hyperthermie") sont générés directement par ce moteur.
