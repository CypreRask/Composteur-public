# Plan d'Implémentation - Moteur Heuristique C/N

## Objectif
Implémenter la **Méthode d'Estimation Heuristique par Ratio** décrite dans le rapport V2.
Cette méthode remplace l'approche précédente par "Bilan de Masse" qui manquait de données sur le flux d'air.
La nouvelle méthode se concentre sur **l'Estimation de Tendance** utilisant les ratios de gaz (R1, R2, R3) et des portes logiques (Vérifications de Validité).

## Note de Conception
> [!IMPORTANT]
> Cette méthode abandonne le calcul de la masse absolue C/N (kg), scientifiquement impossible avec le matériel actuel.
> À la place, elle fournit un **Score de Probabilité (0-100)** d'être dans la "Zone Efficace", ce qui est plus robuste.

## Changements Proposés

### Backend - Nouveau Moteur
#### [NOUVEAU] [heuristic_engine.py](file:///d:/composteur/web-monitor/backend/heuristic_engine.py)
Module Python pur contenant la logique du rapport :
- `compute_indices(df)` -> Calcule R1 (NH3/CO2), R2 (CH4/CO2), EC_Norm.
- `apply_gating(df)` -> Détecte Anaérobie (Porte 2), Faible Activité (Porte 3), Maturité (Porte 1).
- `compute_score(df)` -> Formule pondérée : `0.5*ln(R1) - 0.2*ln(R2) + 0.3*EC`.
- Utilise `pandas` pour les fenêtres glissantes (EMA 24h, Tendance 72h).

### Backend - Intégration
#### [MODIFIER] [main.py](file:///d:/composteur/web-monitor/backend/main.py)
- Supprimer `physics_engine.py`.
- Sur `/api/latest` ou `/api/history`, appliquer le `heuristic_engine` aux données récupérées.
- Retourner le `score`, la `category` (Faible/Optimal/Élevé), et le flag de `reliability`.

### Frontend - Tableau de Bord
#### [MODIFIER] [DataView.svelte](file:///d:/composteur/web-monitor/frontend/src/DataView.svelte)
- Remplacer le nombre "C/N Estimé" par le nouveau **"Indice Score C/N (0-100)"**.
- Ajouter le "Feu Tricolore de Confiance" (Vert/Orange/Rouge) basé sur le flag de fiabilité.
- Afficher la "Porte" active si nécessaire (ex: "INVALIDE : Anaérobie détectée").

## Plan de Vérification

### Tests Automatisés
- **Test Unitaire `test_heuristic.py`** :
    - Script de test alimentant le moteur avec un "Historique Fictif" (CSV).
    - **Scénario A (Anaérobie)** : CH4 élevé -> Attente baisse Score + Porte Anaérobie.
    - **Scénario B (Idéal)** : CO2 élevé, NH3/CH4 faibles -> Attente Score ~50 (Optimal).
    - **Scénario C (Maturité)** : CO2 faible, EC stable -> Attente Porte Maturité.

### Vérification Manuelle
1. **Analyse Historique** : Exécution du moteur sur la base de données existante (`compost.db`) et affichage du "Score Reconstruit" pour les dernières 24h.
2. **Vérification Dashboard** : Contrôle visuel sur `http://localhost:5173` pour vérifier l'apparition du widget "Score C/N" et le changement de couleur.
