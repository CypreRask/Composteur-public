<script>
    import { onMount } from "svelte";

    // STORY MODE STATE
    let step = 0;
    const steps = [
        {
            title: "1. La Rencontre Chimique 📡",
            text: "La racine ne voit pas. Elle émet des signaux (flavonoïdes) pour appeler le champignon.",
            action: "Cliquez pour émettre le signal !",
            animClass: "animate-pulse",
        },
        {
            title: "2. L'Alliance (Réseau de Hartig) 💍",
            text: "Le champignon accepte. Il tisse un manteau autour de la racine et pénètre entre les cellules.",
            action: "Cliquez pour tisser le lien !",
            animClass: "animate-grow",
        },
        {
            title: "3. Le Loyer (Carbone) 🍬",
            text: "L'arbre paie son loyer. Il envoie jusqu'à 20% de ses sucres (photosynthèse) au champignon.",
            action: "Cliquez pour payer en Sucre !",
            animClass: "animate-flow-sugar",
        },
        {
            title: "4. La Livraison (Minéraux) 💎",
            text: "En échange, le mycélium va chercher l'Azote et le Phosphore très loin dans le sol.",
            action: "Cliquez pour recevoir les Minéraux !",
            animClass: "animate-flow-mineral",
        },
    ];

    function nextStep() {
        if (step < steps.length - 1) {
            step++;
        } else {
            step = 0; // Loop or End
        }
    }
</script>

<div class="flex flex-col h-full font-pixel text-white select-none">
    <!-- Header -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-white/20 pb-2"
    >
        <h2 class="text-xl text-orange-300 drop-shadow-md">
            🍄 Symbiose Mycorhizienne
        </h2>
        <div class="text-xs bg-white/20 px-2 py-1 rounded">
            Étape {step + 1}/{steps.length}
        </div>
    </div>

    <!-- SCHEMATIC SCENE -->
    <div
        class="relative flex-grow bg-[#4E342E] border-4 border-[#3E2723] rounded-lg overflow-hidden shadow-inner mb-2 group cursor-pointer w-full text-left"
        on:click={nextStep}
        on:keydown={(e) => e.key === 'Enter' && nextStep()}
        role="button"
        tabindex="0"
        aria-label="Passer à l'étape suivante"
    >
        <svg
            width="100%"
            height="100%"
            viewBox="0 0 300 200"
            preserveAspectRatio="xMidYMid meet"
            class="block"
        >
            <defs>
                <pattern
                    id="cellWall"
                    width="4"
                    height="4"
                    patternUnits="userSpaceOnUse"
                >
                    <rect width="4" height="4" fill="#8D6E63" />
                    <rect width="3" height="3" fill="#A1887F" />
                </pattern>
            </defs>

            <!-- 1. ROOT CELLS (The Host) -->
            <g transform="translate(40, 40)">
                <!-- Cell Wall / Cortex -->
                <rect
                    x="0"
                    y="0"
                    width="80"
                    height="120"
                    rx="4"
                    fill="#A1887F"
                    stroke="#5D4037"
                    stroke-width="2"
                />
                <!-- Cytoplasm -->
                <rect
                    x="5"
                    y="5"
                    width="70"
                    height="110"
                    rx="2"
                    fill="#BCAAA4"
                    opacity="0.6"
                />
                <text
                    x="40"
                    y="110"
                    text-anchor="middle"
                    font-size="8"
                    fill="#3E2723"
                    opacity="0.8">CORTEX</text
                >
            </g>

            <!-- 2. ANIMATIONS PER STEP -->

            <!-- STEP 0: SIGNALING -->
            {#if step === 0}
                <!-- Signal Waves -->
                <circle
                    cx="120"
                    cy="100"
                    r="10"
                    stroke="yellow"
                    fill="none"
                    class="animate-ping"
                    opacity="0.8"
                />
                <circle
                    cx="120"
                    cy="100"
                    r="20"
                    stroke="yellow"
                    fill="none"
                    class="animate-ping"
                    style="animation-delay: 0.3s"
                    opacity="0.6"
                />

                <!-- Approaching Hypha -->
                <path
                    d="M280,100 Q200,100 160,100"
                    stroke="white"
                    stroke-width="4"
                    stroke-dasharray="5 5"
                    opacity="0.5"
                >
                    <animate
                        attributeName="stroke-dashoffset"
                        from="100"
                        to="0"
                        dur="2s"
                        repeatCount="indefinite"
                    />
                </path>
                <text x="200" y="90" font-size="10" fill="white" opacity="0.8"
                    >Hyphe ❓</text
                >
            {/if}

            <!-- STEP 1: COLONIZATION (Hartig Net) -->
            {#if step >= 1}
                <!-- Mantle (Wrapping) -->
                <path
                    d="M130,30 Q160,40 160,100 Q160,160 130,170"
                    stroke="white"
                    stroke-width="6"
                    fill="none"
                    opacity="0.9"
                >
                    <animate
                        attributeName="stroke-dasharray"
                        from="0 200"
                        to="200 0"
                        dur="1.5s"
                        fill="freeze"
                    />
                </path>

                <!-- Hartig Net (Penetration) -->
                <g transform="translate(40,40)" opacity="0.8">
                    <path
                        d="M80,10 H60 M80,30 H50 M80,50 H40"
                        stroke="white"
                        stroke-width="2"
                    >
                        <animate
                            attributeName="d"
                            values="M80,10 H80; M80,10 H60"
                            dur="1s"
                            fill="freeze"
                        />
                    </path>
                </g>

                <text
                    x="180"
                    y="150"
                    font-size="10"
                    fill="white"
                    font-weight="bold">Réseau de Hartig</text
                >
            {/if}

            <!-- STEP 2: SUGAR FLOW (C) -->
            {#if step === 2}
                <g>
                    <circle r="4" fill="#FFD54F">
                        <animateMotion
                            path="M80,100 L160,100 L280,80"
                            dur="1.5s"
                            repeatCount="indefinite"
                        />
                    </circle>
                    <circle r="3" fill="#FFB74D">
                        <animateMotion
                            path="M80,80 L160,80 L280,60"
                            dur="1.5s"
                            begin="0.5s"
                            repeatCount="indefinite"
                        />
                    </circle>
                    <text
                        x="150"
                        y="90"
                        font-size="10"
                        fill="#FFD54F"
                        font-weight="bold">SUCRE (C)</text
                    >
                </g>
            {/if}

            <!-- STEP 3: MINERAL FLOW (Detailed Nitrogen Cycle) -->
            {#if step === 3}
                <g>
                    <!-- 1. MINERALIZATION (Organic -> NH4+) -->
                    <g transform="translate(260, 160)">
                        <rect
                            x="-5"
                            y="-5"
                            width="10"
                            height="10"
                            fill="#5D4037"
                            class="animate-pulse"
                        >
                            <title>Matière Organique</title>
                        </rect>
                        <text
                            x="0"
                            y="15"
                            text-anchor="middle"
                            font-size="6"
                            fill="#A1887F">HUMUS</text
                        >
                    </g>

                    <!-- Arrow to NH4 -->
                    <path
                        d="M260,150 L260,130"
                        stroke="white"
                        stroke-dasharray="2 2"
                    />

                    <!-- 2. AMMONIUM (NH4+) -->
                    <polygon points="260,120 255,130 265,130" fill="#4FC3F7">
                        <animateMotion
                            path="M0,0 L-100,-20 L-180,-40"
                            dur="2s"
                            repeatCount="indefinite"
                        />
                    </polygon>

                    <!-- 3. NITRATE (NO3-) optional context -->
                    <circle
                        cx="200"
                        cy="150"
                        r="3"
                        fill="#81C784"
                        opacity="0.5"
                    >
                        <animateMotion
                            path="M0,0 L-40,-30 L-120,-50"
                            dur="2.5s"
                            begin="0.5s"
                            repeatCount="indefinite"
                        />
                    </circle>

                    <text
                        x="150"
                        y="130"
                        text-anchor="middle"
                        font-size="10"
                        fill="#4FC3F7"
                        font-weight="bold">AMMONIUM (NH₄⁺)</text
                    >
                    <text
                        x="150"
                        y="140"
                        text-anchor="middle"
                        font-size="8"
                        fill="#81C784"
                        opacity="0.8">NITRATE (NO₃⁻)</text
                    >
                </g>
            {/if}
        </svg>

        <!-- Next Button Overlay for intuitive click -->
        <div
            class="absolute bottom-4 right-4 animate-bounce text-white cursor-pointer z-20"
        >
            ▶
        </div>
    </div>

    <!-- TEXT BOX (Story) -->
    <div class="bg-[#3E2723] p-3 border-2 border-[#5D4037] relative shadow-lg">
        <h3 class="text-yellow-300 font-bold mb-1">{steps[step].title}</h3>
        <p class="text-sm text-gray-200 leading-snug min-h-[40px]">
            {steps[step].text}
        </p>
        <button
            class="mt-2 text-[#ff9100] text-xs font-bold hover:underline"
            on:click={nextStep}
        >
            {step < 3 ? "ÉTAPE SUIVANTE ▶" : "RECOMMENCER ↺"}
        </button>
    </div>
</div>
