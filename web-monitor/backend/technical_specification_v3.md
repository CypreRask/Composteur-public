# Spécification d'Architecture : Jumeau Numérique Hybride pour Compostage Prédictif (V3)

**Projet :** Smart Compost Monitor
**Date :** 1 Février 2026
**Statut :** Cadre Conceptuel
**Référence :** Recherche Interne "V3-Hybrid"

---

## 1. Résumé Exécutif
Ce document définit l'architecture "V3" pour le Système d'Intelligence du Compost. Dépassant les simples heuristiques (V2), la V3 implémente un **Jumeau Numérique Hybride Mécaniste-Stochastique**. Son objectif principal n'est pas de "fitter" les données historiques, mais d'estimer **l'État Biologique Latent** du tas pour prédire les événements critiques (Anaérobie, Crash d'Activité) avec un horizon de 72h à 120h.

## 2. Topologie des Capteurs : Causes vs Symptômes
Une intuition critique de la V3 est la classification hiérarchique des entrées. Pour éviter les "biais d'apprentissage", nous distinguons les *moteurs* du système de ses *manifestations*.

### 2.1 Moteurs Principaux (Les "Causes") [Haute Fiabilité]
Ces capteurs mesurent les conditions limites physiques qui dictent la possibilité biologique.
*   **Température ($T$) :** Proxy direct du Taux Métabolique (Respiration/Dégradation du $C_{rapide}$).
*   **Humidité ($W$) :** Clé du Transport d'Oxygène (Coefficient de diffusion $D_{O2} \propto f(W)$). L'excès mène au bouchage des pores (Anaérobie).
*   **pH :** Détermine l'équilibre chimique de l'Ammoniac ($NH_3 \leftrightarrow NH_4^+$). pH haut + T haute = Risque de Volatilisation.
*   **EC (Conductivité) :** Proxy de la Minéralisation (Salinité) et de l'Humification. Une EC élevée peut agir comme inhibiteur.

### 2.2 Signatures Gazeuses (Les "Symptômes") [Basse Fiabilité / Haute Latence]
Les capteurs de gaz mesurent le *résultat* de l'activité biologique, modifié par les délais de transport.
*   **CO₂ :** Respiration Aérobie (Retardé par diffusion).
*   **CH₄ :** La signature primaire des **Bascules Anaérobies** (Méthanogenèse). Dépend fortement de la fraction de "poches anoxiques".
*   **NH₃ :** Saturation en Azote ou déséquilibre C/N.
*   **CO :** Artefact/Signal trace, pondéré faiblement.

**Stratégie :** Le modèle doit efficacement "inverser" la fonction de transport : $Observation(t) = Transport(Etat(t-\delta)) + Bruit$.

## 3. Architecture du Jumeau Numérique

### 3.1 Vecteur d'État Latent ($\vec{x}_t$)
Le Jumeau Numérique estime des variables qui ne peuvent pas être mesurées directement mais définissent la trajectoire future du système :

*   $A(t)$ : **Activité Microbienne Effective** (Fraction de biomasse active).
*   $C_{rapide}(t)$ : Stock de **Carbone Bio-disponible** (Sucres/Cellulose).
*   $N_{dispo}(t)$ : Stock d'**Azote Minéralisé** ($NH_4^+/NO_3^-$).
*   $W_{eff}(t)$ : **Saturation Effective** (Occupation des pores).
*   $K_{O2}(t)$ : **Capacité d'Aération** (Porosité/Percolation estimée).
*   $AnaFrac(t)$ : **Fraction Anoxique** (0.0 à 1.0).

### 3.2 Le Modèle Hybride
Le Jumeau opère en "Shadow Mode", mettant à jour son état $\vec{x}_t$ à chaque pas de temps.

#### A. Cœur Mécaniste (La Physique)
Définit l'évolution de $\vec{x}_t$ :
$$ \frac{dA}{dt} = \mu(T, W, pH) \cdot \frac{C_{rapide}}{K_c + C_{rapide}} - Decheance $$
$$ \text{AnaFrac} = f(W_{eff}, K_{O2}) \quad (\text{si Demande } O_2 > \text{Offre } O_2) $$

#### B. Couche d'Observation (Le Modèle Capteur)
Mappe l'état vers les mesures attendues (Problème Inverse) :
$$ CO_{2,mesure}(t) = \text{Diffuse}(A(t) \cdot \text{AerobicFrac}) + \epsilon_{derive} $$

### 3.3 Prédiction Probabiliste (L'Ensemble)
Au lieu d'une courbe unique, le système V3 projette un **Ensemble de N=50 trajectoires** dans le futur (J+5), échantillonnant les incertitudes sur :
1.  Météo (Pluie/Temp).
2.  Intervention (Limites utilisateur).
3.  Erreur Modèle (Bruit de processus).

**Sortie :** Probabilité de Danger $P(E|t_{maintenant})$
*   "Probabilité d'Anaérobie > 50% dans 48h"
*   "Probabilité de Crash d'Activité > 80% dans 72h"

## 4. Stratégie d'Implémentation

### 4.1 Entraînement Synthétique ("Sim-to-Real")
Pour entraîner les composants ML (Correction Résiduelle & Fonction de Hasard), nous générons un dataset synthétique massif via **Domain Randomization** :
*   Simuler la dérive capteur (Offset/Gain walk).
*   Simuler les délais membranaires (1h - 48h).
*   Simuler l'hétérogénéité (Poches anaérobies localisées).
*   Simuler les "Événements Externes" (Retournement, Ajout Verts, Pluie).

Le modèle ML apprend à mapper *l'historique capteur bruité et retardé* vers des *probabilités d'état latent propres*.

### 4.2 Le Moteur "What-If"
En accédant à l'État Latent, le système peut simuler des contrefactuels :
*   *Action :* "Ajouter 5kg Matière Sèche (Bruns)" $\rightarrow$ $W_{eff} \downarrow, K_{O2} \uparrow$.
*   *Prédiction :* $P(Anaérobie)$ chute de 85% à 12%.
*   *Recommandation :* "Ajouter des Bruns pour prévenir le crash imminent."

## 5. Roadmap de Déploiement

### Phase 1 : Alerte Robuste (Actuel V2+)
*   Modèle : Règles Heuristiques + Détection de Tendance (Moteur V2).
*   Sortie : État Actuel + Tendance Naïve (Linéaire).

### Phase 2 : Jumeau Ombre (V3 Alpha)
*   Modèle : Estimateur d'État Mécaniste tournant en temps réel.
*   Sortie : Variables Latentes affichées (estimation stock $C_{rapide}$), Projection 5 jours.

### Phase 3 : Résidus Neuronaux (V3 Beta)
*   Modèle : Deep Learning entraîné sur Données Synthétiques corrige le Noyau Mécaniste.
*   Sortie : Maintenance Prédictive, Détection de Panne Capteur ("Désaccord CO2 implique défaillance capteur").

## 6. Conclusion
L'Architecture V3 représente un changement de paradigme du "Monitoring" vers la "Gestion". En distinguant les moteurs des symptômes et en modélisant l'état biologique caché, le système passe d'un observateur passif à un système expert actif et prédictif, capable de guider l'utilisateur à travers le processus de compostage avec une prévoyance scientifiquement fondée.
