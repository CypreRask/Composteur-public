<script>
    import { createEventDispatcher } from "svelte";
    import { fade, fly, scale } from "svelte/transition";
    const dispatch = createEventDispatcher();

    // --- STATE ---
    export let plantType = "C3";
    export let showToggle = true;

    let turgor = 50; // 0-100%
    let stomataOpen = false;

    // --- MARKERS DATA ---
    let activeMarker = null;
    const MARKERS = [
        {
            id: "guard",
            x: 25,
            y: 50,
            label: "Cellules de Garde",
            text: "Les portiers ! Elles gonflent d'eau pour courber leur paroi et ouvrir le passage.",
        },
        {
            id: "ostiole",
            x: 50,
            y: 50,
            label: "Ostiole (Trou)",
            text: "La bouche de la feuille. C'est ici que le CO2 entre pour la photosynthèse et que l'eau sort.",
        },
        {
            id: "chloro",
            x: 65,
            y: 35,
            label: "Chloroplaste",
            text: "L'usine à énergie. C'est rare d'en trouver dans la peau (épiderme), sauf ici pour ouvrir la porte !",
        },
        {
            id: "skin",
            x: 10,
            y: 10,
            label: "Épiderme",
            text: "La peau de la feuille. Elle est transparente et recouverte de cire (cuticule) pour ne pas sécher.",
        },
    ];

    // --- LOGIC ---
    function togglePlantType() {
        if (!showToggle) return;
        plantType = plantType === "C3" ? "C4" : "C3";
    }

    function toggleStomata() {
        if (turgor < 30) return;
        stomataOpen = !stomataOpen;
    }

    function enterStomata() {
        if (!stomataOpen) return;
        if (plantType === "C3") {
            dispatch("openCell");
        } else if (plantType === "C4") {
            dispatch("openC4");
        } else if (plantType === "CAM") {
            dispatch("openCAM");
        }
    }

    function waterLeaf() {
        turgor = 100;
        stomataOpen = true;
    }

    function toggleMarker(marker) {
        if (activeMarker === marker) activeMarker = null;
        else activeMarker = marker;
    }
</script>

<div
    class="w-full h-full relative font-pixel bg-[#1B5E20] overflow-hidden flex flex-col items-center justify-center select-none"
    on:click={() => (activeMarker = null)}
    on:keydown={(e) => e.key === "Escape" && (activeMarker = null)}
    role="presentation"
>
    <!-- HEADER -->
    <div
        class="absolute top-0 left-0 w-full p-2 flex justify-between items-start z-30 pointer-events-none"
    >
        <div class="flex flex-col gap-2 pointer-events-auto">
            <div
                class="bg-black/70 text-white text-xs px-3 py-1 rounded border border-green-800 shadow-md w-fit flex gap-2 items-center"
            >
                <span
                    >Niveau 1.5 : <span class="text-green-400">ÉPIDERME</span
                    ></span
                >
                <span
                    class="px-1 rounded text-[10px] {plantType === 'C3'
                        ? 'bg-green-900 text-green-200'
                        : plantType === 'C4'
                          ? 'bg-yellow-900 text-yellow-200'
                          : 'bg-purple-900 text-purple-200'}"
                >
                    {plantType === "C3"
                        ? "🍏 Pommier"
                        : plantType === "C4"
                          ? "🌽 Maïs"
                          : "🌵 Orpin"}
                </span>
            </div>

            <!-- CONTROLS -->
            <div
                class="bg-black/60 p-2 rounded border border-green-600 flex flex-col gap-2"
            >
                {#if showToggle}
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] text-gray-300">PLANTE :</span>
                        <button
                            class="px-2 py-1 text-xs rounded border-2 transition-colors {plantType ===
                            'C3'
                                ? 'bg-green-600 border-white text-white'
                                : 'bg-gray-700 border-gray-600 text-gray-400'}"
                            on:click={() => (plantType = "C3")}
                        >
                            🍏 C3
                        </button>
                        <button
                            class="px-2 py-1 text-xs rounded border-2 transition-colors {plantType ===
                            'C4'
                                ? 'bg-yellow-600 border-white text-white'
                                : 'bg-gray-700 border-gray-600 text-gray-400'}"
                            on:click={() => (plantType = "C4")}
                        >
                            🌽 C4
                        </button>
                        <button
                            class="px-2 py-1 text-xs rounded border-2 transition-colors {plantType ===
                            'CAM'
                                ? 'bg-purple-600 border-white text-white'
                                : 'bg-gray-700 border-gray-600 text-gray-400'}"
                            on:click={() => (plantType = "CAM")}
                        >
                            🌵 CAM
                        </button>
                    </div>
                {/if}

                <!-- HYDRATION -->
                <div class="flex items-center gap-2">
                    <span class="text-[10px] text-gray-300">TURGESCENCE :</span>
                    {#if turgor < 30}
                        <button
                            class="text-[10px] bg-red-500 text-white px-2 py-1 rounded animate-vibrate"
                            on:click={waterLeaf}
                        >
                            🚿 ARROSER !
                        </button>
                    {:else}
                        <span class="text-[10px] text-blue-300"
                            >💧 {turgor}% (Optimale)</span
                        >
                    {/if}
                </div>
            </div>
        </div>
    </div>

    <!-- BACKGROUND: EPIDERMAL CELLS (Pavement) -->
    <!-- SVG Pattern simulating the jigsaw puzzle cells of the epidermis -->
    <svg
        class="absolute inset-0 w-full h-full opacity-30 z-0"
        xmlns="http://www.w3.org/2000/svg"
    >
        <pattern
            id="epidermis"
            x="0"
            y="0"
            width="100"
            height="100"
            patternUnits="userSpaceOnUse"
        >
            <path
                d="M0,0 Q25,25 50,0 T100,0 V50 Q75,75 50,50 T0,50 Z"
                fill="none"
                stroke="#66BB6A"
                stroke-width="2"
            />
            <path
                d="M0,50 Q25,75 50,50 T100,50 V100 Q75,125 50,100 T0,100 Z"
                fill="none"
                stroke="#66BB6A"
                stroke-width="2"
            />
        </pattern>
        <rect width="100%" height="100%" fill="url(#epidermis)" />
        <!-- Random "nucleus" dots for background cells -->
        {#each Array(20) as _, i}
            <circle
                cx="{Math.random() * 100}%"
                cy="{Math.random() * 100}%"
                r="2"
                fill="#2E7D32"
                opacity="0.6"
            />
        {/each}
    </svg>

    <!-- HERO STOMATA (Detailed) -->
    <div
        class="relative z-10 w-[300px] h-[300px] flex items-center justify-center filter drop-shadow-xl transition-transform duration-500"
        style="transform: scale({stomataOpen ? 1.05 : 1});"
    >
        <!-- SURROUNDING TILES (Visualizing the 'Pavement' cells around the stomata) -->
        <div
            class="absolute inset-0 border-[3px] border-[#4CAF50]/50 rounded-full scale-125 opacity-40"
        ></div>
        <div
            class="absolute inset-0 border-[1px] border-[#81C784]/30 rounded-full scale-110 opacity-30"
        ></div>

        <!-- LEFT GUARD CELL -->
        <div
            class="absolute w-[100px] h-[200px] bg-[#43A047] border-[4px] border-[#1B5E20] rounded-l-full left-[50px] shadow-inner flex items-center justify-center overflow-hidden transition-all duration-700 origin-right"
            style="
                border-radius: 100% 0 0 100% / 50% 0 0 50%;
                transform: translateX({stomataOpen
                ? -15
                : 0}px) rotate({stomataOpen ? -5 : 0}deg);
             "
        >
            <!-- Thick Inner Wall (Visual) -->
            <div
                class="absolute right-0 top-0 h-full w-[10px] bg-[#1B5E20]/80"
            ></div>

            <!-- Chloroplasts (Green Dots) -->
            <div
                class="absolute top-[20%] left-[30%] w-3 h-3 bg-[#00E676] rounded-full opacity-80 shadow-sm"
            ></div>
            <div
                class="absolute top-[50%] left-[20%] w-4 h-4 bg-[#00E676] rounded-full opacity-80 shadow-sm"
            ></div>
            <div
                class="absolute bottom-[30%] left-[40%] w-3 h-3 bg-[#00E676] rounded-full opacity-80 shadow-sm"
            ></div>

            <!-- Vacuole (Big Blue Blob - Shrinks when flaccid/closed) -->
            <div
                class="absolute top-[40%] left-[10%] w-12 h-20 bg-blue-300/30 rounded-full blur-sm transition-all duration-700"
                style="opacity: {stomataOpen
                    ? 0.6
                    : 0.2}; transform: scale({stomataOpen ? 1 : 0.7});"
            ></div>

            <!-- Nucleus -->
            <div
                class="absolute top-[15%] left-[50%] w-4 h-4 bg-pink-800/60 rounded-full border border-pink-500"
            ></div>
        </div>

        <!-- RIGHT GUARD CELL -->
        <div
            class="absolute w-[100px] h-[200px] bg-[#43A047] border-[4px] border-[#1B5E20] rounded-r-full right-[50px] shadow-inner flex items-center justify-center overflow-hidden transition-all duration-700 origin-left"
            style="
                border-radius: 0 100% 100% 0 / 0 50% 50% 0;
                transform: translateX({stomataOpen
                ? 15
                : 0}px) rotate({stomataOpen ? 5 : 0}deg);
             "
        >
            <!-- Thick Inner Wall -->
            <div
                class="absolute left-0 top-0 h-full w-[10px] bg-[#1B5E20]/80"
            ></div>

            <!-- Chloroplasts -->
            <div
                class="absolute top-[30%] right-[30%] w-4 h-4 bg-[#00E676] rounded-full opacity-80 shadow-sm"
            ></div>
            <div
                class="absolute bottom-[40%] right-[20%] w-3 h-3 bg-[#00E676] rounded-full opacity-80 shadow-sm"
            ></div>

            <!-- Vacuole -->
            <div
                class="absolute top-[30%] right-[10%] w-12 h-20 bg-blue-300/30 rounded-full blur-sm transition-all duration-700"
                style="opacity: {stomataOpen
                    ? 0.6
                    : 0.2}; transform: scale({stomataOpen ? 1 : 0.7});"
            ></div>

            <!-- Nucleus -->
            <div
                class="absolute bottom-[15%] right-[50%] w-4 h-4 bg-pink-800/60 rounded-full border border-pink-500"
            ></div>
        </div>

        <!-- OSTIOLE (The Hole) -->
        <!-- Interactive Click Area -->
        <div
            class="absolute z-20 w-[40px] h-[160px] cursor-magnify group flex items-center justify-center"
            on:click={toggleStomata}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && toggleStomata}
        >
            <!-- The Void -->
            <div
                class="absolute inset-0 bg-black transition-all duration-700 rounded-[50%]"
                style="
                    transform: scaleX({stomataOpen ? 1 : 0.05});
                    opacity: {stomataOpen ? 0.9 : 0.5};
                  "
                on:click|stopPropagation={() => stomataOpen && enterStomata()}
                role="button"
                tabindex="0"
                on:keydown={(e) =>
                    e.key === "Enter" && stomataOpen && enterStomata()}
            >
                {#if stomataOpen}
                    <!-- Entrance Helper -->
                    <div
                        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[10px] text-white font-bold bg-green-700/80 px-2 py-1 rounded hover:bg-green-600 active:scale-95 transition-transform pointer-events-none"
                    >
                        ENTRER 🔍
                    </div>

                    <!-- Gas Particles -->
                    {#each Array(8) as _, i}
                        <div
                            class="absolute w-2 h-2 bg-gray-200 rounded-full animate-flow pointer-events-none"
                            style="left: {50}%; top: {100}%; animation-delay: {i *
                                0.3}s"
                        ></div>
                    {/each}
                {/if}
            </div>
        </div>
    </div>

    <!-- BIO-MARKERS OVERLAY -->
    <!-- Positioned relative to the main container -->
    {#each MARKERS as m}
        <button
            class="absolute w-6 h-6 bg-yellow-400 text-black border-2 border-white rounded-full flex items-center justify-center text-xs font-bold shadow-lg hover:scale-110 transition-transform z-30 animate-bounce-slight"
            style="left: {m.x}%; top: {m.y}%; animation-delay: {Math.random()}s"
            on:click|stopPropagation={() => toggleMarker(m)}
        >
            ?
        </button>
    {/each}

    <!-- TOOLTIP POPUP -->
    {#if activeMarker}
        <div
            class="absolute bottom-16 left-1/2 -translate-x-1/2 w-[90%] md:w-[60%] bg-black/90 border-2 border-yellow-400 p-4 rounded-xl shadow-2xl z-50 text-white"
            transition:fly={{ y: 20, duration: 200 }}
        >
            <div class="flex justify-between items-start mb-2">
                <h3 class="text-yellow-400 font-bold text-sm uppercase">
                    {activeMarker.label}
                </h3>
                <button
                    class="text-gray-400 hover:text-white"
                    on:click|stopPropagation={() => (activeMarker = null)}
                    >✖</button
                >
            </div>
            <p class="text-xs text-gray-200 leading-relaxed font-sans">
                {activeMarker.text}
            </p>
        </div>
    {/if}

    <!-- HINT TEXT -->
    <div class="absolute bottom-4 text-center pointer-events-none">
        {#if !stomataOpen}
            <p
                class="text-[10px] text-green-200 animate-pulse bg-black/40 px-2 rounded"
            >
                {#if turgor > 30}
                    👇 Cliquez au centre pour OUVRIR
                {:else}
                    ⚠️ Manque d'eau - Impossible d'ouvrir !
                {/if}
            </p>
        {:else}
            <p class="text-[10px] text-white bg-black/40 px-2 rounded">
                Échanges gazeux en cours... (CO2 ⬇️ O2 ⬆️)
            </p>
        {/if}
    </div>
</div>

<style>
    .animate-vibrate {
        animation: vibrate 0.3s linear infinite;
    }
    @keyframes vibrate {
        0% {
            transform: translate(0);
        }
        20% {
            transform: translate(-2px, 2px);
        }
        40% {
            transform: translate(-2px, -2px);
        }
        60% {
            transform: translate(2px, 2px);
        }
        80% {
            transform: translate(2px, -2px);
        }
        100% {
            transform: translate(0);
        }
    }

    .animate-flow {
        animation: flow 2s infinite linear;
    }
    @keyframes flow {
        0% {
            transform: translate(-50%, 0) scale(0.5);
            opacity: 0;
        }
        50% {
            opacity: 0.8;
        }
        100% {
            transform: translate(-50%, -100px) scale(1.5);
            opacity: 0;
        }
    }

    .animate-bounce-slight {
        animation: bounceSlight 2s infinite ease-in-out;
    }
    @keyframes bounceSlight {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-3px);
        }
    }
</style>
