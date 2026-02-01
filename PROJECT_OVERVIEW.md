# Composteur V2 - Projet IoT Full Stack

## 🌍 Vision du Projet
Ce projet vise à créer un **moniteur de compost connecté et ludique**, transformant une activité biologique lente en une expérience interactive et pédagogique.
L'objectif est de fusionner la rigueur scientifique (mesures précises, corrélations) avec une esthétique de jeu vidéo rétro ("Terraria-like") pour rendre le compostage engageant.

---

## 🏗️ Architecture Technique

### 1. Électronique (Embarqué)
- **Cœur** : ESP32 (Master) + Modules LoRa (Emetteur/Récepteur).
- **Capteurs** :
  - **Air/Gaz** : SCD41 (CO2/Temp/Hum), MICS-6814 (NO2/CO/NH3 via MQs modifiés).
  - **Sol** : Capteur NPK (Azote, Phosphore, Potassium), Humidité Sol.
- **Energie** : Gestion par batterie 12V + Panneau Solaire (à venir).
- **Communication** : LoRaWAN (TTN) ou LoRa P2P vers une passerelle locale.

### 2. Backend (Serveur)
- **Langage** : Python 3.10+.
- **API** : FastAPI.
- **Base de Données** : SQLite (via SQLModel).
- **Ingestion** : Script `ingest.py` écoutant MQTT ou Port Série.

### 3. Frontend (Interface Utilisateur)
- **Framework** : Svelte (Vite).
- **Style** : Tailwind CSS.
- **Esthétique** : **PIXEL ART OBLIGATOIRE**. Pas de design "Clean Corporate". On veut du "Jeu Indé".
- **Vues** :
  - **Biome** : Vue artistique en couches (Ciel dynamique, Surface, Sous-sol).
  - **Data** : Tableaux de bord, graphiques, matrices de corrélation.
  - **Learn** : Encyclopédie interactive du compost.

---

## 🎨 Règles de Design & Développement

### Frontend
1.  **Pixel Art First** : Tous les éléments visuels doivent respecter une grille de pixels cohérente.
2.  **Gamification** : L'interface doit réagir comme un jeu (animations, particules, tooltips ludiques).
3.  **Wows** : Chaque vue doit avoir un élément "waouh" (vers qui bougent, ciel qui change, etc.).

### Pédagogie
1.  **Vulgarisation** : Expliquer les concepts complexes (Rapport C/N, Cycle de Krebs simplifié) de manière accessible.
2.  **Données Actives** : Ne pas juste montrer un chiffre, expliquer ce qu'il signifie pour la santé du compost (ex: "Trop chaud ! Les bactéries thermophiles travaillent dur").

---

## 📅 Roadmap & Améliorations Futures

- [ ] **Data Intégration** : Connecter le Frontend au Backend réel (en cours).
- [ ] **Graphismes** : Améliorer la qualité des sprites (vers, déchets, minéraux) et ajouter plus de variété.
- [ ] **Pédagogie** : Enrichir le contenu de l'onglet "Comprendre" avec des quiz ou des guides interactifs.
- [ ] **ML/IA** : Affiner le modèle de prédiction pour qu'il soit plus pertinent avec de vraies données.
