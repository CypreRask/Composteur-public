export const LEARNING_PATH = [
    // CHAPITRE 1 : LES BASES
    {
        id: "intro_1",
        type: "theory", // theory | game
        title: "Introduction",
        subtitle: "L'Or Noir",
        desc: "Découvre pourquoi composter est un super-pouvoir pour la planète.",
        content: `
# C'est quoi le Compost ?

Le compostage, c'est **transformer tes déchets de cuisine en nourriture pour la terre**.

C'est un processus **naturel** : dans la forêt, les feuilles mortes se décomposent pour nourrir les arbres. Dans ton composteur, c'est pareil, mais en accéléré !

### Pourquoi c'est génial ?
*   🗑️ **Moins de poubelle** : 30% de nos déchets sont compostables.
*   🌍 **Moins de pollution** : On évite d'incinérer des déchets qui sont à 80% de l'eau (gaspillage d'énergie !).
*   🌱 **Engrais gratuit** : Tu fabriques un terreau riche pour tes plantes.
        `,
        xp: 10,
        unlocked: true // Always unlocked start
    },
    {
        id: "game_sorter_1",
        type: "game",
        gameId: "sorter",
        config: { level: 1 }, // Level 1 = ETE (Facile)
        title: "Défi : Trieur Débutant",
        subtitle: "Niveau Été",
        desc: "Montre que tu sais reconnaître ce qui se mange (Verts) et ce qui se jette.",
        requirement: { score: 50 },
        xp: 50
    },

    // CHAPITRE 2 : EQUILIBRE
    {
        id: "theory_cn",
        type: "theory",
        title: "La Recette Magique",
        subtitle: "Verts & Bruns",
        desc: "Le secret d'un compost qui ne pue pas : l'équilibre Azote / Carbone.",
        content: `
# La Loi de l'Équilibre (C/N)

Pour que ça marche, il faut mélanger deux ingrédients clés :

### 🥬 Les Verts (Azote)
*   **C'est quoi ?** Épluchures, fruits, légumes, tonte de gazon.
*   **Effet** : C'est mou, humide, et ça pourrit vite.
*   **Rôle** : Nourrir les bactéries.

### 🍂 Les Bruns (Carbone)
*   **C'est quoi ?** Feuilles mortes, carton, boîtes d'oeufs, broyat de bois.
*   **Effet** : C'est sec, dur, et ça structure.
*   **Rôle** : Apporter de l'air et servir d'abri.

### ⚠️ La Règle d'Or
**1 part de Verts + 2 à 3 parts de Bruns = Compost Parfait** (en volume)
*   Trop de Verts ? 🤢 Ça pue et ça coule (excès d'azote, pas assez d'air).
*   Trop de Bruns ? 🌵 C'est sec et rien ne se passe (excès de carbone).
        `,
        xp: 20
    },
    {
        id: "game_sorter_2",
        type: "game",
        gameId: "sorter",
        config: { level: 2 }, // Level 2 = AUTOMNE (Difficile)
        title: "Défi : Trieur Expert",
        subtitle: "Niveau Automne",
        desc: "Attention à l'afflux de feuilles mortes ! Garde l'équilibre.",
        requirement: { score: 80 },
        xp: 100
    },

    // CHAPITRE 3 : LA VIE
    {
        id: "theory_bio",
        type: "theory",
        title: "Les Ouvriers de l'Ombre",
        subtitle: "Qui fait le boulot ?",
        desc: "Fais connaissance avec tes milliards de petits employés.",
        content: `
# Le Peuple du Compost

Ce n'est pas "magique", c'est **biologique** !

### 1. Les Bactéries 🦠
Elles sont invisibles mais sont des milliards. Elles attaquent les déchets mous et font **chauffer** le tas (jusqu'à 70°C !).

### 2. Les Champignons 🍄
Leur réseau blanc (mycélium) attaque le bois et les feuilles dures que les bactéries n'arrivent pas à manger.

### 3. La Mésa-faune 🪱
Une fois refroidi, les **Vers de compost** (Eisenia), cloportes et collemboles arrivent pour finir le travail et brasser la matière.
        `,
        xp: 30
    },
    {
        id: "game_foodweb",
        type: "game",
        gameId: "foodweb",
        title: "Défi : Festin du Sol",
        subtitle: "Chaîne Alimentaire",
        desc: "Connecte les organismes pour créer un écosystème stable.",
        requirement: { connections: 5 }, // Custom requirement handled in wrapper
        xp: 150
    },

    // CHAPITRE 4 : MASTERCLASS
    {
        id: "theory_phases",
        type: "theory",
        title: "Les 4 Saisons du Compost",
        subtitle: "Le Cycle Complet",
        desc: "Comment transformer une poubelle en terreau en 4 étapes.",
        content: `
# Le Cycle de Vie

Un compost, c'est comme une cuisson lente :

1.  **Colonisation** : Les premiers habitants s'installent.
2.  **Montée en Température (Thermophile)** : Les bactéries s'activent, ça chauffe fort ! Ça tue les maladies.
3.  **Refroidissement** : La température baisse, les champignons prennent le relais.
4.  **Maturation** : Les vers arrivent, transforment tout en humus noir (l'Or Noir).

À toi de piloter ce processus !
        `,
        xp: 50
    },
    {
        id: "game_builder",
        type: "game",
        gameId: "cyclebuilder",
        title: "Défi Ultime : Architecte",
        subtitle: "Simulation",
        desc: "Pilote un compost réel. Gère l'air, l'eau et la température jusqu'à la maturation.",
        requirement: { win: true },
        xp: 500
    },
    {
        id: "final_quiz",
        type: "game",
        gameId: "quiz",
        title: "Examen Final",
        subtitle: "Certification",
        desc: "Prouve tes connaissances pour obtenir le Diplôme de Maître Composteur.",
        requirement: { score: 4 }, // 4/5 correct
        xp: 1000
    }
];
