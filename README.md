# 🌱 SmartCompost

**Un écosystème connecté pour visualiser la vie invisible du sol.**

> 🚧 **En Développement** : Ce projet est un prototype fonctionnel en cours d'amélioration, une v1 avait déjà été déployé et une v2 avec plus de capteurs et un meilleur boitier est en cours de réalisation.
⚠️ Warning :  Les algorithmes de calcul (notamment le rapport C/N et les conversions de gaz) sont actuellement des ébauches théoriques. Les vérifications mathématiques et les calibrations physiques (capteurs MQ) n'ont pas encore été faites! 
Ce projet surveille la santé d'un composteur (Température, Humidité, NPK) et propose une expérience gamifiée pour comprendre les processus biologiques de décomposition.

## 📂 Structure du Projet

- **`/web-monitor`** : L'application principale (Svelte + Backend Python/FastAPI).
  - **Dashboard** : Visualisation temps réel des données capteurs.
  - **Moteur Heuristique** : Analyse prédictive de la santé du compost (Jumeau Numérique).
  - **Jeux Éducatifs** : Modules interactifs (Cycle de vie, Chaîne alimentaire).
- **`/firmware`** : Code embarqué pour les capteurs ESP32/LoRaWAN (Arduino/C++).
- **`/docs`** : documentation technique et spécifications.

## 🚀 Installation Rapide

1.  Aller dans le dossier `web-monitor`.
2.  Backend : `pip install -r backend/requirements.txt`
3.  Frontend : `cd frontend && npm install`
4.  Lancer : Exécuter `START_APP.bat` (Windows) pour démarrer tous les services.

## 🎮 Fonctionnalités

- **Monitoring Temps Réel** : Suivi via MQTT/TheThingsNetwork (Température, Humidité, Gaz).
- **Jeux "Serious Games"** :
  - *Le Trieur Fou* : Apprendre à équilibrer Carbone/Azote.
  - *Festin du Sol* : Reconstituer la chaîne trophique du sol.
  - *Architecte du Sol* : Gérer les cycles de bactéries et champignons.
- **Mode Labo & Sciences** :
  - Visualisation microscopique des interactions (C4/C3, Cycle de l'Azote).
  - Compréhension du **Complexe Argilo-Humique** (CAH).
  - Symbiose Arbre-Champignons (Mycorhizes).
  > Le compost est utilisé comme un "cheval de Troie" pédagogique pour comprendre l'intégration globale des écosystèmes.

## 📸 Galerie

### Interface & Monitoring
| Vue Surface | Tableau de Bord |
|:---:|:---:|
| ![Vue Surface](assets/interface.png) | ![Tableau de Bord](assets/dashboard.png) |
| *L'arbre reflète la santé du système* | *Analyse précise des données* |

### Hardware & Installation (Prototype V1)
| Boîtier de Mesure (V1) | Test Terrain (Solaire) |
|:---:|:---:|
| ![Boitier](assets/case.jpg) | ![Câblage](assets/wiring.jpg) |
| *Câblage initial pour collecte de données* | *Déploiement "Test électrique outdoor|

## 🛠️ Stack Technique

- **Frontend** : Svelte, Vite, TailwindCSS (Pixel Art UI).
- **Backend** : Python (FastAPI), SQLite, Pandas.
- **Hardware** : ESP32, LoRaWAN, Capteurs NPK & Gaz.

---
*Projet réalisé pour la Mission Éco-Responsable.*
