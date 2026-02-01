export const MICRO_DATA = {
    psychro: {
        title: "Phase Psychrophile (< 20°C)",
        desc: "Le début de l'hiver ou du processus. La vie tourne au ralenti.",
        creatures: [
            {
                name: "Collembole",
                type: "insect",
                icon: "🐜",
                behavior: "jump",
                desc: "Sautille partout. Mange les champignons.",
            },
            {
                name: "Cloporte",
                type: "insect",
                icon: "🐞",
                behavior: "crawl",
                desc: "Dégrade le bois mort. Respire par des branchies !",
            },
            {
                name: "Nématode",
                type: "worm",
                icon: "〰️",
                behavior: "wiggle",
                desc: "Ver microscopique. Certains mangent les bactéries.",
            },
        ],
        color: "bg-blue-200 border-2 border-white",
        borderColor: "border-blue-800",
    },
    meso: {
        title: "Phase Mésophile (20°C - 45°C)",
        desc: "L'activité bat son plein ! Les ouvriers spécialisés sont au travail.",
        creatures: [
            {
                name: "Eisenia (Ver Rouge)",
                type: "worm",
                icon: "🪱",
                behavior: "crawl",
                desc: "Le roi du compost ! Il mange son poids par jour.",
            },
            {
                name: "Champignon (Mycélium)",
                type: "fungi",
                icon: "🕸️",
                behavior: "static",
                desc: "Réseau blanc qui digère le bois et les feuilles dures.",
            },
            {
                name: "Acarien",
                type: "insect",
                icon: "🕷️",
                behavior: "scurry",
                desc: "Régule la population de vers et décompose.",
            },
        ],
        color: "bg-green-200 border-2 border-white",
        borderColor: "border-green-800",
    },
    thermo: {
        title: "Phase Thermophile (45°C - 70°C)",
        desc: "La surchauffe ! Seules les bactéries thermorésistantes survivent.",
        creatures: [
            {
                name: "Actinobactérie",
                type: "bacteria",
                icon: "🦠",
                behavior: "pulse",
                desc: "Donne l'odeur de terre des bois. Blanchit la matière.",
            },
            {
                name: "Bacillus",
                type: "bacteria",
                icon: "💊",
                behavior: "spin",
                desc: "Bactérie en bâtonnet très résistante à la chaleur.",
            },
            {
                name: "Thermophiles",
                type: "bacteria",
                icon: "🔥",
                behavior: "shake",
                desc: "Elles génèrent cette chaleur intense !",
            },
        ],
        color: "bg-red-200 border-2 border-white",
        borderColor: "border-red-800",
    },
};

export const SORTER_ITEMS = [
    // GREENS (Nitrogen)
    { id: "apple", icon: "🍏", type: "green", name: "Trognon", info: "L'azote pur. Parfait pour activer la chauffe." },
    { id: "banana", icon: "🍌", type: "green", name: "Banane", info: "La peau se décompose vite. Riche en potassium." },
    { id: "grass", icon: "🌿", type: "green", name: "Tonte", info: "Attention, chauffe très fort ! Mélanger avec du brun." },
    { id: "lettuce", icon: "🥬", type: "green", name: "Salade", info: "Beaucoup d'eau. Attention à ne pas noyer le tas." },
    { id: "melon", icon: "🍈", type: "green", name: "Melon", info: "Riche en eau. Les vers adorent le sucre." },
    { id: "tea", icon: "🍵", type: "green", name: "Sachet Thé", info: "Ok si sachet en papier. Le thé est un bon activateur." },
    { id: "coffee", icon: "☕", type: "green", name: "Marc Café", info: "Excellent activateur ! Les vers en raffolent." },

    // BROWNS (Carbon)
    { id: "leaf", icon: "🍂", type: "brown", name: "Feuille Morte", info: "L'or brun de l'automne. Structure le compost." },
    { id: "cardboard", icon: "📦", type: "brown", name: "Carton", info: "Enlever le scotch ! Les vers se cachent dedans." },
    { id: "eggbox", icon: "🥡", type: "brown", name: "Boite Oeufs", info: "Carton moulé, très facile à digérer." },
    { id: "paper", icon: "🗞️", type: "brown", name: "Journal", info: "L'encre est ok (soja). Eviter le papier glacé." },
    { id: "wood", icon: "🪵", type: "brown", name: "Copeaux", info: "Se décompose lentement (lignine). Aère le tas." },
    { id: "tissues", icon: "🧻", type: "brown", name: "Mouchoir", info: "Cellulose pure. Disparaît en quelques jours." },

    // TRASH / TOXIC / CONTROVERSIAL
    { id: "bottle", icon: "🥤", type: "trash", name: "Plastique", info: "Jamais ! Ça fait des microplastiques." },
    { id: "battery", icon: "🔋", type: "toxic", name: "Pile", info: "POISON ! Métaux lourds qui tuent le sol." },
    { id: "bones", icon: "🍖", type: "trash", name: "Os (Viande)", info: "Attire les rats et mauvaises odeurs. (Expert seulement)" },
    { id: "can", icon: "🥫", type: "trash", name: "Conserve", info: "Métal. Recyclage, pas compost." },
    { id: "poop", icon: "💩", type: "toxic", name: "Caca chien", info: "Pathogènes dangereux. A éviter en compost domestique." },
    { id: "milk", icon: "🥛", type: "trash", name: "Laitage", info: "Graisses qui rancissent et étouffent le compost." },
    { id: "citrus", icon: "🍋", type: "green", name: "Agrumes", info: "Acide en grande quantité, mais ok si mélangé." },
];

export const QUIZ_QUESTIONS = [
    {
        question: "Quelle phase monte jusqu'à 70°C ?",
        options: [
            "Phase Mésophile",
            "Phase Thermophile",
            "Phase de Maturation",
        ],
        answer: "Phase Thermophile",
    },
    {
        question: "Quel est le ratio idéal Vert/Brun ?",
        options: ["100% Vert", "50% / 50% (Volume)", "100% Brun"],
        answer: "50% / 50% (Volume)",
    },
    {
        question: "Qui crée le Complexe Argilo-Humique ?",
        options: [
            "Les bactéries seules",
            "Le mariage Argile + Humus",
            "Les épluchures d'orange",
        ],
        answer: "Le mariage Argile + Humus",
    },
];
