<script>
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";
    import { onMount, onDestroy, createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    // --- CONFIGURATION ---
    const TICK_RATE = 1000; // 1s per tick
    const STAGES = [
        {
            id: 0,
            name: "Colonisation",
            targetTemp: 20,
            minPop: 50,
            desc: "Place les premiers habitants !",
        },
        {
            id: 1,
            name: "Montée en T°",
            targetTemp: 60,
            minPop: 200,
            desc: "Nourris les bactéries pour chauffer !",
        },
        {
            id: 2,
            name: "Assainissement",
            targetTemp: 55,
            duration: 10,
            desc: "Maintiens > 50°C pour tuer les pathogènes.",
        },
        {
            id: 3,
            name: "Refroidissement",
            targetTemp: 30,
            wormPop: 20,
            desc: "Refroidis et ramène les vers.",
        },
        {
            id: 4,
            name: "Maturation",
            targetHumus: 100, // Goal
            desc: "Les vers doivent produire 100% d'Humus !",
        },
    ];

    // --- GAME STATE ---
    let gameActive = false;
    let gameOver = false;
    let victory = false;
    let feedback = "";

    // Stats
    let temp = 15; // °C
    let moisture = 50; // %
    let carbon = 50; // Relative units
    let nitrogen = 0; // Relative units
    let oxygen = 100; // %
    let humus = 0; // NEW: Victory Goal

    // Populations
    let bacteria = 0;
    let worms = 0;
    let pathogens = 10;

    // Progression
    let stage = 0;
    let ticksInStage = 0;
    let totalTicks = 0;

    let timerInterval;

    // history for graph
    let tempHistory = [];

    // --- SIMULATION LOOP ---
    function tick() {
        if (!gameActive) return;
        totalTicks++;
        ticksInStage++;

        // 0. Physics & Clamping (User Request: "Pas dépasser 100%")
        oxygen = Math.min(100, Math.max(0, oxygen));
        moisture = Math.min(100, Math.max(0, moisture));
        carbon = Math.max(0, carbon);
        nitrogen = Math.max(0, nitrogen);
        bacteria = Math.max(0, bacteria);
        worms = Math.max(0, worms);

        // 1. Carrying Capacity (Limitée par les ressources)
        // MaxPop = Min(C, N) * Scale
        const resourceLimit = (Math.min(carbon, nitrogen) + 10) * 15;
        const spaceLimit = (oxygen + moisture) * 8;
        const carryingCapacity = Math.min(resourceLimit, spaceLimit);

        // 2. Population Dynamics
        // Growth
        if (bacteria < carryingCapacity && temp > 10 && temp < 75) {
            // Sweet spot 30-60°C means fast growth
            const tempFactor = temp > 30 && temp < 60 ? 0.25 : 0.05;
            const oxyBonus = oxygen > 50 ? 1.5 : 0.8;

            // Base growth + Exponential
            bacteria += (5 + bacteria * tempFactor) * oxyBonus;
        } else if (bacteria > carryingCapacity) {
            bacteria -= bacteria * 0.05; // Gentle die-off
            if (carryingCapacity < 50 && bacteria > 50)
                feedback = "📉 Manque de ressources !";
        }

        // Critical conditions
        if (oxygen <= 5 || moisture <= 5 || temp >= 75) {
            bacteria -= bacteria * 0.2; // Fast death
            feedback = "⚠️ CONDITIONS CRITIQUES !";
        }

        // Worms (Sensitive)
        if (temp > 35) {
            worms -= worms * 0.15;
            if (worms > 5) feedback = "⚠️ TROP CHAUD POUR LES VERS !";
        } else if (temp > 10 && temp < 30 && moisture > 40 && oxygen > 30) {
            worms += worms * 0.1;
            // Worms produce Humus during maturation (Stage 3 & 4)
            if (stage >= 3 && worms > 0) {
                let production = worms * 0.005;
                humus = Math.min(100, humus + production);
                if (production > 0.1) ticksInStage = 0; // Keep active
            }
        }

        // 3. Dynamic Consumption
        if (bacteria > 0) {
            const consumptionRate = bacteria / 150; // Balanced rate

            carbon -= 0.3 * consumptionRate;
            nitrogen -= 0.15 * consumptionRate;
            oxygen -= 1.5 * consumptionRate;

            // Heat Generation
            let heatGen = 0.6 * consumptionRate;

            // C/N Ratio efficiency
            const cnRatio = carbon / (nitrogen || 1);
            if (cnRatio >= 20 && cnRatio <= 35)
                heatGen *= 1.8; // Optimal
            else if (cnRatio < 10) heatGen *= 0.5; // Sludgy

            if (oxygen < 10) heatGen *= 0.1; // Anaerobic

            temp += heatGen;
        }

        // 4. Environmental Physics
        const ambient = 15;
        // Newton's Law of Cooling (slow)
        temp -= (temp - ambient) * 0.015;

        const evap = (temp / 100) * 0.4;
        moisture -= evap;

        if (temp > 55) {
            pathogens = Math.max(0, pathogens - 5);
        }

        tempHistory = [...tempHistory, temp].slice(-50);
        checkStageProgress();
    }

    function checkStageProgress() {
        const s = STAGES[stage];
        let complete = false;

        if (stage === 0) {
            // Colonisation
            if (bacteria > s.minPop) complete = true;
        } else if (stage === 1) {
            // Heat Up
            if (temp >= s.targetTemp) complete = true;
        } else if (stage === 2) {
            // Sanitize (Hold Temp)
            if (temp < 50) {
                ticksInStage = 0; // Reset counter if temp drops
                feedback = "⚠️ Température trop basse ! Remonte > 50°C";
            }
            if (ticksInStage >= s.duration && pathogens <= 0) complete = true;
        } else if (stage === 3) {
            // Cooling
            if (temp <= s.targetTemp && worms >= s.wormPop) complete = true;
        } else if (stage === 4) {
            // Maturation (Hubus Goal)
            if (humus >= 100) complete = true;
        }

        if (complete) {
            stage++;
            ticksInStage = 0;
            if (stage >= STAGES.length) {
                // Victory
                victory = true;
                gameActive = false;
                feedback = "🏆 OR NOIR OBTENU !";
                clearInterval(timerInterval);
                dispatch("complete", { score: 100 });
            } else {
                feedback = `✨ ÉTAPE ${stage} TERMINÉE ! -> ${STAGES[stage].name}`;
            }
        }

        // Game Over Conditions
        if (oxygen <= 0 && ticksInStage > 10) {
            feedback = "🤢 ANAÉROBIE TOTALE ! Tout est mort.";
            // gameOver = true; // Optional hardcore
        }
        if (bacteria <= 0 && totalTicks > 20 && stage > 0) {
            feedback = "☠️ PLUS DE BACTERIES !";
        }
    }

    function startGame() {
        gameActive = true;
        victory = false;
        gameOver = false;
        stage = 0;
        ticksInStage = 0;
        totalTicks = 0;

        // Reset Logic
        temp = 20;
        moisture = 50;
        carbon = 50;
        nitrogen = 0; // Start with nothing to force player action
        oxygen = 100;
        bacteria = 0;
        worms = 0;
        pathogens = 10;
        tempHistory = new Array(50).fill(20);

        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(tick, TICK_RATE);
        feedback = "C'est parti ! Commence par coloniser le tas.";
    }

    onDestroy(() => {
        if (timerInterval) clearInterval(timerInterval);
    });

    // --- ACTIONS ---
    const ACTIONS = [
        {
            id: "bact",
            icon: "🦠",
            name: "Bactéries",
            desc: "+Vie, -O2 (Coût: 5% O2)",
            effect: () => {
                if (oxygen >= 5) {
                    bacteria += 50; // Kickstart
                    oxygen -= 5;
                    if (bacteria < 10) bacteria = 10;
                } else {
                    feedback = "🚫 Pas assez d'Oxygène !";
                }
            },
        },
        {
            id: "green",
            icon: "🥬",
            name: "Verts",
            desc: "+Azote, -Place",
            effect: () => {
                if (nitrogen < 100) {
                    nitrogen += 25;
                    moisture += 5;
                } else {
                    feedback = "🚫 Composter plein (Azote max) !";
                }
            },
        },
        {
            id: "brown",
            icon: "🍂",
            name: "Bruns",
            desc: "+Carbone, -Eau",
            effect: () => {
                if (carbon < 100) {
                    carbon += 25;
                    moisture -= 5;
                } else {
                    feedback = "🚫 Composter plein (Carbone max) !";
                }
            },
        },
        {
            id: "water",
            icon: "💧",
            name: "Arroser",
            desc: "+Eau, -Temp",
            effect: () => {
                if (moisture < 100) {
                    moisture += 20;
                    temp -= 1; // Mild cooling
                    oxygen -= 5;
                } else {
                    feedback = "🚫 Inondation !";
                }
            },
        },
        {
            id: "turn",
            icon: "🔄",
            name: "Retourner",
            desc: "+Oxygène, -10°C (Refroidit)",
            effect: () => {
                oxygen = 100;
                // Active Cooling: Break the heat core!
                // If it's hot, it cools down a LOT.
                if (temp > 40) temp -= 10;
                else temp -= 2;

                feedback = "🌬️ Aération ! La température chute.";
            },
        },
        {
            id: "worm",
            icon: "🪱",
            name: "Vers",
            desc: "Accélère la fin (Si <35°C)",
            effect: () => {
                if (temp < 35 && moisture > 20) {
                    worms += 10;
                    feedback = "🪱 Les vers accélèrent la maturation !";
                } else {
                    feedback =
                        "🚫 Conditions mortelles pour les vers (Temp/Sec) !";
                }
            },
        },
    ];

    function doAction(act) {
        if (!gameActive) return;
        act.effect();
        // Visual feedback could go here
    }

    // --- HELPERS ---
    $: cnDisplay = (carbon / (nitrogen || 0.1)).toFixed(1);
</script>

<div class="h-full relative font-pixel">
    <RetroWindow title="Architecte du Sol" mode="inline" width="w-full">
        {#if !gameActive && !victory}
            <!-- LOBBY -->
            <div
                class="flex flex-col items-center justify-center h-full p-8 space-y-6"
            >
                <div class="text-6xl animate-pulse">🏗️</div>
                <h2 class="text-3xl font-bold text-[#C0CA33] text-center">
                    Architecte du Sol
                </h2>
                <p class="text-sm text-center text-gray-300 max-w-md">
                    Incarne l'esprit du compost. <br />
                    Guidez le processus de la matière brute à l'humus fertile. Gère
                    la température, l'air et la vie.
                </p>

                <div
                    class="grid grid-cols-2 gap-4 text-xs text-gray-400 border border-gray-600 p-4 rounded bg-black/20"
                >
                    <div class="flex flex-col items-center">
                        <span>PHASE 1</span>
                        <strong class="text-blue-400">Colonisation</strong>
                    </div>
                    <div class="flex flex-col items-center">
                        <span>PHASE 2</span>
                        <strong class="text-red-400"
                            >Chauffe (Thermophile)</strong
                        >
                    </div>
                    <div class="flex flex-col items-center">
                        <span>PHASE 3</span>
                        <strong class="text-orange-400">Refroidissement</strong>
                    </div>
                    <div class="flex flex-col items-center">
                        <span>PHASE 4</span>
                        <strong class="text-green-400">Maturation</strong>
                    </div>
                </div>

                <button
                    class="px-8 py-3 bg-[#558B2F] text-white font-bold border-b-4 border-[#2E3B20] hover:bg-[#689F38] active:border-b-0 active:translate-y-1 transition-all"
                    on:click={startGame}
                >
                    COMMENCER LA SIMULATION
                </button>
            </div>
        {:else if victory}
            <!-- WIN SCREEN -->
            <div
                class="flex flex-col items-center justify-center h-full p-8 space-y-6"
            >
                <div class="text-8xl">🏆</div>
                <h2 class="text-4xl text-yellow-400 font-bold">
                    CYCLE COMPLET !
                </h2>
                <p class="text-center">Tu as créé un humus parfait.</p>
                <button
                    class="px-6 py-2 bg-gray-600 text-white rounded"
                    on:click={() => (victory = false)}>Retour</button
                >
            </div>
        {:else}
            <!-- GAMEPLAY UI -->
            <div class="flex flex-col h-full p-2 gap-2">
                <!-- TOP BAR: PROGRESS & FEEDBACK -->
                <div
                    class="flex justify-between items-center bg-black/40 p-2 rounded border border-gray-700"
                >
                    <div class="flex flex-col">
                        <span class="text-[10px] text-gray-400"
                            >PHASE {stage + 1}/4</span
                        >
                        <strong class="text-[#C0CA33]"
                            >{STAGES[stage].name}</strong
                        >
                    </div>
                    <div
                        class="text-xs text-center text-yellow-100 px-4 animate-pulse"
                    >
                        {feedback}
                    </div>
                    <div class="text-right">
                        <span class="text-[10px] text-gray-400">TEMPS</span>
                        <div class="font-mono">{totalTicks}h</div>
                    </div>
                </div>

                <!-- MAIN DISPLAY: PILE & STATS -->
                <div
                    class="flex-1 flex flex-col lg:flex-row gap-2 min-h-0 overflow-y-auto lg:overflow-hidden"
                >
                    <!-- LEFT: VISUAL PILE -->
                    <div
                        class="lg:flex-1 h-48 lg:h-auto shrink-0 bg-[#2E3B20] border-2 border-[#558B2F] relative overflow-hidden rounded shadow-inner"
                    >
                        <!-- SKY -->
                        <div
                            class="absolute inset-0 bg-gradient-to-b from-[#84bbf0] to-transparent h-1/3 opacity-20"
                        ></div>

                        <!-- PILE LAYERS (DYNAMIC) -->
                        <div
                            class="absolute bottom-0 w-full bg-[#3E2723] transition-all duration-1000 ease-in-out flex items-end justify-center"
                            style="height: {20 + (carbon + nitrogen) / 4}%"
                        >
                            <!-- Texture -->
                            <div
                                class="w-full h-full opacity-50 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iMiIgaGVpZ2h0PSIyIiBmaWxsPSIjNTQzRDI1Ii8+PC9zdmc+')]"
                            ></div>

                            <!-- Particles: Bacteria -->
                            {#if bacteria > 0}
                                <div
                                    class="absolute inset-0 z-10 opacity-50 animate-pulse bg-green-900/20"
                                ></div>
                            {/if}

                            <!-- Particles: Heat -->
                            {#if temp > 40}
                                <div
                                    class="absolute -top-4 w-full flex justify-center space-x-4 opacity-50"
                                >
                                    <span class="animate-bounce text-red-400"
                                        >🔥</span
                                    >
                                    <span
                                        class="animate-bounce delay-100 text-red-400"
                                        >♨️</span
                                    >
                                    <span
                                        class="animate-bounce delay-200 text-red-400"
                                        >🔥</span
                                    >
                                </div>
                            {/if}

                            <!-- Worms -->
                            {#if worms > 0}
                                <div
                                    class="absolute bottom-2 w-full text-center text-xl animate-bounce-step"
                                >
                                    🪱
                                </div>
                            {/if}
                        </div>
                    </div>

                    <!-- RIGHT: GAUGES -->
                    <div
                        class="w-full lg:w-1/3 flex flex-row lg:flex-col gap-2 shrink-0 overflow-x-auto lg:overflow-visible pr-1"
                    >
                        <!-- Temperature -->
                        <div
                            class="bg-black/50 p-2 rounded border-l-4 border-red-500"
                        >
                            <div
                                class="flex justify-between text-[10px] text-gray-300"
                            >
                                <span>TEMP</span>
                                <span>{temp.toFixed(1)}°C</span>
                            </div>
                            <div
                                class="w-full bg-gray-700 h-1.5 mt-1 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-gradient-to-r from-blue-500 via-green-500 to-red-500 transition-all duration-500"
                                    style="width: {(temp / 80) * 100}%"
                                ></div>
                            </div>
                            <!-- Target Marker -->
                            <div
                                class="text-[8px] text-gray-500 text-right mt-0.5"
                            >
                                Cible: {STAGES[stage].targetTemp || "-"}°C
                            </div>
                        </div>

                        <!-- Moisture -->
                        <div
                            class="bg-black/50 p-2 rounded border-l-4 border-blue-500"
                        >
                            <div
                                class="flex justify-between text-[10px] text-gray-300"
                            >
                                <span>EAU</span>
                                <span>{moisture.toFixed(0)}%</span>
                            </div>
                            <div
                                class="w-full bg-gray-700 h-1.5 mt-1 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-blue-400 transition-all duration-500"
                                    style="width: {moisture}%"
                                ></div>
                            </div>
                        </div>

                        <!-- Oxygen -->
                        <div
                            class="bg-black/50 p-2 rounded border-l-4 border-cyan-500"
                        >
                            <div
                                class="flex justify-between text-[10px] text-gray-300"
                            >
                                <span>AIR (O2)</span>
                                <span>{oxygen.toFixed(0)}%</span>
                            </div>
                            <div
                                class="w-full bg-gray-700 h-1.5 mt-1 rounded-full overflow-hidden"
                            >
                                <div
                                    class="h-full bg-cyan-400 transition-all duration-500"
                                    style="width: {oxygen}%"
                                ></div>
                            </div>
                        </div>

                        <!-- Biome -->
                        <div
                            class="bg-black/50 p-2 rounded border-l-4 border-green-500 text-[10px]"
                        >
                            <div class="flex justify-between mb-1">
                                <span>🦠 BACT</span>
                                <span class="text-green-300"
                                    >{bacteria.toFixed(0)}</span
                                >
                            </div>
                            <div class="flex justify-between">
                                <span>🪱 VERS</span>
                                <span class="text-pink-300"
                                    >{worms.toFixed(0)}</span
                                >
                            </div>
                            {#if stage >= 3}
                                <div class="mt-2 border-t border-gray-600 pt-1">
                                    <div
                                        class="flex justify-between text-[#8D6E63]"
                                    >
                                        <span>HUMUS</span>
                                        <span>{humus.toFixed(0)}%</span>
                                    </div>
                                    <div
                                        class="w-full bg-gray-700 h-2 mt-1 rounded-full overflow-hidden"
                                    >
                                        <div
                                            class="h-full bg-[#3E2723] transition-all duration-500"
                                            style="width: {humus}%"
                                        ></div>
                                    </div>
                                </div>
                            {/if}
                        </div>
                    </div>
                </div>

                <!-- BOTTOM: ACTIONS DECK -->
                <div
                    class="min-h-[6rem] bg-[#3E2723] rounded p-2 grid grid-cols-3 lg:flex gap-2 items-center border-t-4 border-[#5D4037]"
                >
                    {#each ACTIONS as action}
                        <button
                            class="w-full lg:w-20 h-16 lg:h-full bg-[#5D4037] border-2 border-[#8D6E63] rounded hover:bg-[#6D4C41] active:translate-y-1 transition-all flex flex-col items-center justify-center p-1 group relative"
                            on:click={() => doAction(action)}
                        >
                            <div
                                class="text-2xl group-hover:scale-110 transition-transform"
                            >
                                {action.icon}
                            </div>
                            <div
                                class="text-[9px] font-bold text-[#FFCCBC] mt-1 text-center leading-tight"
                            >
                                {action.name}
                            </div>

                            <!-- Tooltip -->
                            <div
                                class="hidden group-hover:block absolute bottom-full mb-2 bg-black/90 text-white text-[10px] p-2 rounded w-32 z-50 pointer-events-none"
                            >
                                {action.desc}
                            </div>
                        </button>
                    {/each}
                </div>
            </div>
        {/if}
    </RetroWindow>
</div>

<style>
    /* Reuse global animations or define specific ones */
    .animate-bounce-step {
        animation: bounce-step 1s steps(4) infinite;
    }

    @keyframes bounce-step {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-3px);
        }
    }
</style>
