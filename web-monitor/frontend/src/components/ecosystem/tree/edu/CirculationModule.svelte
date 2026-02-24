<script>
    import { onMount } from "svelte";

    // STORY MODE STATE
    let step = 0;
    const steps = [
        {
            title: "1. L'Aspiration (Xylème) 💧",
            text: "La transpiration des feuilles crée une succion. L'eau monte comme une corde tendue (Cohésion).",
            action: "Cliquez pour tirer la colonne d'eau !",
            animClass: "animate-flow-up",
        },
        {
            title: "2. Le Chargement (Source) 🍬",
            text: "Dans les feuilles, le sucre (photosynthèse) est pompé activement dans les tubes du Phloème.",
            action: "Cliquez pour charger le sucre !",
            animClass: "animate-load-sugar",
        },
        {
            title: "3. Le Courant de Masse 🌊",
            text: "Le sucre concentre attire l'eau par osmose. Cette pression hydrostatique pousse la seve elaboree vers le bas dans le Phloeme.",
            action: "Cliquez pour déclencher le flux !",
            animClass: "animate-flow-down",
        },
        {
            title: "4. La Réserve (Rayons) 📦",
            text: "En descendant, le sucre est stocké horizontalement dans les rayons ligneux (Aubier).",
            action: "Cliquez pour stocker l'amidon !",
            animClass: "animate-store-starch",
        },
    ];

    function nextStep() {
        if (step < steps.length - 1) {
            step++;
        } else {
            step = 0; // Loop
        }
    }
</script>

<div class="flex flex-col h-full font-pixel text-white select-none">
    <!-- Header -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-white/20 pb-2"
    >
        <h2 class="text-xl text-yellow-300 drop-shadow-md">
            🪵 Circulation : Sève
        </h2>
        <div class="text-xs bg-white/20 px-2 py-1 rounded">
            Étape {step + 1}/{steps.length}
        </div>
    </div>

    <!-- SCHEMATIC SCENE -->
    <div
        class="relative flex-grow bg-[#5D4037] border-4 border-[#3E2723] rounded-lg overflow-hidden shadow-inner mb-2 group cursor-magnify w-full text-left"
        on:click={nextStep}
        on:keydown={(e) => e.key === "Enter" && nextStep()}
        role="button"
        tabindex="0"
        aria-label="Passer à l'étape suivante"
    >
        <!-- Background: Wood Grain -->
        <div
            class="absolute inset-0 opacity-20 pointer-events-none"
            style="background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, #3E2723 10px, #3E2723 12px);"
        ></div>

        <svg
            width="100%"
            height="100%"
            viewBox="0 0 300 200"
            preserveAspectRatio="none"
            class="block relative z-10"
        >
            <!-- 1. XYLEM (LEFT) - Blue Pipe -->
            <rect
                x="50"
                y="10"
                width="60"
                height="180"
                fill="#29B6F6"
                fill-opacity="0.2"
                stroke="#29B6F6"
                stroke-width="2"
                stroke-opacity="0.5"
            />
            <text
                x="80"
                y="185"
                text-anchor="middle"
                font-size="8"
                fill="#29B6F6"
                opacity="0.8">XYLÈME (EAU)</text
            >

            <!-- 2. PHLOEM (RIGHT) - Orange Pipe -->
            <rect
                x="190"
                y="10"
                width="60"
                height="180"
                fill="#FFA726"
                fill-opacity="0.2"
                stroke="#FFA726"
                stroke-width="2"
                stroke-opacity="0.5"
            />
            <!-- Sieve Plates -->
            {#each [50, 90, 130] as y}
                <line
                    x1="190"
                    y1={y}
                    x2="250"
                    y2={y}
                    stroke="#FFA726"
                    stroke-width="1"
                    stroke-dasharray="2 2"
                />
            {/each}
            <text
                x="220"
                y="185"
                text-anchor="middle"
                font-size="8"
                fill="#FFA726"
                opacity="0.8">PHLOÈME (SUCRE)</text
            >

            <!-- 3. RAY CELLS (Horizontal Storage) -->
            <rect
                x="110"
                y="80"
                width="80"
                height="40"
                rx="5"
                fill="#8D6E63"
                stroke="#3E2723"
                opacity="0.8"
            />
            <text
                x="150"
                y="105"
                text-anchor="middle"
                font-size="8"
                fill="#EFEBE9"
                opacity="0.8">RAYON (STOCK)</text
            >

            <!-- ANIMATIONS -->

            <!-- STEP 0: TRANSPIRATION PULL (Water going UP in Xylem) -->
            {#if step === 0 || step === 2}
                <g>
                    {#each [0, 40, 80, 120, 160] as y, i}
                        <circle cx="80" cy={y + 10} r="4" fill="#E1F5FE">
                            <animate
                                attributeName="cy"
                                from={200}
                                to={0}
                                dur="2s"
                                begin="{i * 0.4}s"
                                repeatCount="indefinite"
                            />
                        </circle>
                    {/each}
                    <!-- Rope Effect visualization -->
                    <line
                        x1="80"
                        y1="0"
                        x2="80"
                        y2="200"
                        stroke="#81D4FA"
                        stroke-width="1"
                        stroke-dasharray="4 4"
                        opacity="0.5"
                    >
                        <animate
                            attributeName="stroke-dashoffset"
                            from="200"
                            to="0"
                            dur="2s"
                            repeatCount="indefinite"
                        />
                    </line>
                </g>
            {/if}

            <!-- STEP 1: LOADING (Sugar appearing in Phloem Top) -->
            {#if step === 1}
                <g>
                    <!-- Pulse effect at source -->
                    <circle
                        cx="270"
                        cy="30"
                        r="10"
                        stroke="#FFD54F"
                        fill="none"
                        class="animate-ping"
                    />

                    <!-- Sugar Cubes entering -->
                    <rect
                        x="270"
                        y="26"
                        width="8"
                        height="8"
                        fill="#FFD54F"
                        stroke="#E65100"
                    >
                        <animate
                            attributeName="x"
                            from="270"
                            to="216"
                            dur="0.6s"
                            fill="freeze"
                            calcMode="spline"
                            keyTimes="0;1"
                            keySplines="0.4, 0, 0.2, 1"
                        />
                    </rect>

                    <!-- Pile up high density -->
                    <rect
                        x="216"
                        y="26"
                        width="8"
                        height="8"
                        fill="#FFB74D"
                        stroke="#E65100"
                    >
                        <animate
                            attributeName="opacity"
                            values="0.5; 1; 0.5"
                            dur="1s"
                            repeatCount="indefinite"
                        />
                    </rect>
                    <rect
                        x="220"
                        y="20"
                        width="8"
                        height="8"
                        fill="#FFA726"
                        stroke="#E65100"
                        opacity="0.8"
                    >
                        <animate
                            attributeName="opacity"
                            values="0.5; 1; 0.5"
                            dur="1s"
                            begin="0.3s"
                            repeatCount="indefinite"
                        />
                    </rect>
                    <text
                        x="220"
                        y="55"
                        text-anchor="middle"
                        font-size="8"
                        fill="#FFD54F"
                        font-weight="bold"
                        class="animate-bounce">CHARGE ACTIVE!</text
                    >
                </g>
            {/if}

            <!-- STEP 2: PRESSURE FLOW (Osmosis + Flow) -->
            {#if step === 2}
                <g>
                    <!-- Osmosis Arrow (Water Crossing Over) -->
                    <path
                        d="M110,40 L190,40"
                        stroke="#4FC3F7"
                        stroke-width="4"
                        stroke-dasharray="4 2"
                    >
                        <animate
                            attributeName="stroke-dashoffset"
                            from="20"
                            to="0"
                            dur="0.5s"
                            repeatCount="indefinite"
                        />
                    </path>
                    <text
                        x="150"
                        y="35"
                        text-anchor="middle"
                        font-size="6"
                        fill="#4FC3F7"
                        font-weight="bold">OSMOSE</text
                    >

                    <!-- Mass Flow Down (Mixed Cluster) -->
                    {#each [0, 40, 80] as offset, i}
                        <g>
                            <!-- Sugar Cube -->
                            <rect
                                x="214"
                                y="20"
                                width="8"
                                height="8"
                                fill="#FFD54F"
                                stroke="#E65100"
                            >
                                <animate
                                    attributeName="y"
                                    from="20"
                                    to="200"
                                    dur="2s"
                                    begin="{i * 0.6}s"
                                    repeatCount="indefinite"
                                />
                            </rect>
                            <!-- Water Cube attached (Pressure) -->
                            <rect
                                x="226"
                                y="20"
                                width="6"
                                height="6"
                                fill="#4FC3F7"
                                opacity="0.8"
                            >
                                <animate
                                    attributeName="y"
                                    from="20"
                                    to="200"
                                    dur="2s"
                                    begin="{i * 0.6}s"
                                    repeatCount="indefinite"
                                />
                            </rect>
                        </g>
                    {/each}
                </g>
            {/if}

            <!-- STEP 3: STORAGE (Unloading) -->
            {#if step === 3}
                <g>
                    <text
                        x="150"
                        y="120"
                        text-anchor="middle"
                        font-size="8"
                        fill="white">AMIDON</text
                    >
                </g>
            {/if}

            <defs>
                <marker
                    id="arrow"
                    markerWidth="10"
                    markerHeight="10"
                    refX="0"
                    refY="3"
                    orient="auto"
                    markerUnits="strokeWidth"
                >
                    <path d="M0,0 L0,6 L9,3 z" fill="#4FC3F7" />
                </marker>
            </defs>
        </svg>

        <!-- Next Pulse -->
        <div
            class="absolute bottom-4 right-4 animate-bounce text-white cursor-magnify z-20"
        >
            ▶
        </div>
    </div>

    <!-- TEXT BOX -->
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
