<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let step = 0;
    let isNight = true; // Start at night (the CAM trick)

    const steps = [
        {
            title: "1. La Nuit : Ouverture 🌙",
            text: "Contrairement aux C3 et C4, la plante CAM ouvre ses stomates LA NUIT. Pas de soleil = pas d'évaporation. Le CO₂ entre sans gaspiller d'eau.",
            action: "OUVRIR LES STOMATES",
            night: true,
        },
        {
            title: "2. Stockage Acide 🧪",
            text: "La PEPcase (même enzyme que le C4 !) fixe le CO₂ en Acide Malique. Mais au lieu de l'envoyer dans une autre cellule, il est stocké dans la VACUOLE de la même cellule.",
            action: "REMPLIR LA VACUOLE",
            night: true,
        },
        {
            title: "3. Le Jour : Fermeture 🌞",
            text: "Au lever du soleil, les stomates se FERMENT. Zéro perte d'eau. La feuille devient un coffre-fort hermétique. L'énergie lumineuse est captée par les chloroplastes.",
            action: "FERMER ET ALLUMER",
            night: false,
        },
        {
            title: "4. Libération Interne 🔓",
            text: "L'Acide Malique est libéré de la vacuole → le CO₂ est relâché DANS la cellule fermée. Rubisco peut travailler avec un CO₂ concentré, sans aucune perte.",
            action: "LIBÉRER LE CO₂",
            night: false,
        },
        {
            title: "5. Résultat : Survie Extrême 🏜️",
            text: "Séparation TEMPORELLE (nuit/jour) au lieu de SPATIALE (C4). Moins efficace en croissance, mais imbattable en économie d'eau. Idéal pour les milieux arides.",
            action: "RECOMMENCER LE CYCLE",
            night: false,
        },
    ];

    function nextStep() {
        if (step < steps.length - 1) {
            step++;
        } else {
            step = 0;
        }
        isNight = steps[step].night;
    }

    // Vacuole fill level
    $: vacuoleFill = step === 0 ? 0 : step === 1 ? 100 : step === 2 ? 100 : step === 3 ? 30 : 0;
    // Stomata state
    $: stomataOpen = step <= 1;
    // CO2 visible inside
    $: co2Inside = step >= 3;
    // Sun visible
    $: sunVisible = step >= 2;
    // Malate particles moving
    $: malateMoving = step === 1;
    // Calvin cycle active
    $: calvinActive = step >= 4;
</script>

<div class="flex flex-col h-full font-pixel text-white select-none">
    <!-- Header -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-white/20 pb-2 p-2 rounded-t transition-colors duration-700"
        class:bg-indigo-900={isNight}
        class:bg-amber-600={!isNight}
    >
        <button
            class="text-xs border border-white/30 px-2 py-1 rounded hover:bg-white/20 transition-colors"
            on:click={() => dispatch("back")}
        >
            ⬅ RETOUR
        </button>
        <span class="text-xs" class:text-indigo-200={isNight} class:text-amber-200={!isNight}>
            MÉTABOLISME CAM (Crassulacées)
        </span>
        <div class="text-lg">
            {isNight ? "🌙" : "☀️"}
        </div>
    </div>

    <!-- MAIN SCENE: Single Cell with Day/Night cycle -->
    <div
        class="relative flex-grow border-4 rounded-lg overflow-hidden shadow-inner mb-2 transition-colors duration-1000"
        class:bg-indigo-950={isNight}
        class:border-indigo-800={isNight}
        class:bg-green-800={!isNight}
        class:border-green-900={!isNight}
    >
        <!-- BACKGROUND: Stars (Night) or Sun rays (Day) -->
        {#if isNight}
            <div class="absolute inset-0 overflow-hidden pointer-events-none">
                {#each Array(15) as _, i}
                    <div
                        class="absolute w-1 h-1 bg-white rounded-full animate-twinkle"
                        style="left: {10 + (i * 37) % 80}%; top: {5 + (i * 23) % 60}%; animation-delay: {i * 0.3}s"
                    ></div>
                {/each}
            </div>
        {:else}
            <div class="absolute inset-0 overflow-hidden pointer-events-none">
                <div class="absolute -top-10 -right-10 w-32 h-32 bg-yellow-300/20 rounded-full blur-xl animate-pulse-slow"></div>
            </div>
        {/if}

        <!-- THE CELL (Center) -->
        <div class="absolute inset-8 border-4 border-green-500/60 rounded-2xl bg-green-900/40 flex items-center justify-center">
            <!-- Cell Wall Label -->
            <div class="absolute -top-3 left-4 text-[8px] bg-green-700 px-2 py-0.5 rounded text-green-200">
                CELLULE CAM
            </div>

            <!-- VACUOLE (Center - The key CAM organ) -->
            <div
                class="relative w-32 h-32 rounded-full border-4 border-purple-400/80 transition-all duration-1000 flex items-center justify-center"
                style="background: rgba(147, 51, 234, {vacuoleFill / 300}); box-shadow: 0 0 {vacuoleFill / 5}px rgba(147, 51, 234, 0.5);"
            >
                <div class="text-[8px] text-purple-200 text-center font-bold">
                    VACUOLE<br/>
                    <span class="text-[10px]">
                        {#if vacuoleFill > 50}
                            🧪 Acide Malique
                        {:else if vacuoleFill > 0}
                            💨 Vidange...
                        {:else}
                            (vide)
                        {/if}
                    </span>
                </div>

                <!-- Malate fill animation -->
                {#if malateMoving}
                    {#each Array(5) as _, i}
                        <div
                            class="absolute w-2 h-2 bg-purple-400 rounded-full animate-malate-fill"
                            style="animation-delay: {i * 0.4}s; left: {30 + i * 12}%; top: -20px;"
                        ></div>
                    {/each}
                {/if}
            </div>

            <!-- CHLOROPLASTES (Around vacuole) -->
            <div class="absolute top-6 left-10 w-8 h-5 bg-green-500 rounded-full border border-green-300 flex items-center justify-center text-[6px]"
                class:animate-pulse-slow={sunVisible}
                class:opacity-40={isNight}
            >
                Chl
            </div>
            <div class="absolute bottom-8 right-8 w-8 h-5 bg-green-500 rounded-full border border-green-300 flex items-center justify-center text-[6px]"
                class:animate-pulse-slow={sunVisible}
                class:opacity-40={isNight}
            >
                Chl
            </div>
            <div class="absolute top-1/2 right-6 w-8 h-5 bg-green-500 rounded-full border border-green-300 flex items-center justify-center text-[6px]"
                class:animate-pulse-slow={sunVisible}
                class:opacity-40={isNight}
            >
                Chl
            </div>

            <!-- PEPcase (Active at night) -->
            {#if isNight}
                <div class="absolute top-4 right-12 w-10 h-10 bg-blue-700 border-2 border-blue-400 rounded flex items-center justify-center text-[7px] font-bold shadow-lg z-10">
                    PEPc
                </div>
            {/if}

            <!-- Rubisco (Active during day) -->
            {#if !isNight}
                <div class="absolute bottom-4 left-10 w-12 h-12 bg-orange-700 border-2 border-orange-400 rounded-lg flex items-center justify-center text-[7px] font-bold shadow-lg z-10">
                    Rubisco
                </div>
            {/if}

            <!-- CO2 released inside (step 3+) -->
            {#if co2Inside}
                {#each Array(4) as _, i}
                    <div
                        class="absolute w-6 h-6 bg-white/80 rounded-full flex items-center justify-center text-[6px] text-black font-bold animate-float-around z-20"
                        style="animation-delay: {i * 0.5}s; left: {20 + i * 18}%; top: {25 + (i % 2) * 40}%;"
                    >
                        CO₂
                    </div>
                {/each}
            {/if}

            <!-- Sugar output (step 4+) -->
            {#if calvinActive}
                <div class="absolute bottom-2 right-2 text-lg animate-float-up">🍬</div>
                <div class="absolute bottom-6 left-2 text-xs text-yellow-300 font-bold animate-pulse">
                    Calvin ✓
                </div>
            {/if}
        </div>

        <!-- STOMATA (Bottom of scene) -->
        <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex items-center gap-1 z-20">
            <!-- Left guard -->
            <div
                class="w-8 h-14 rounded-l-full border-2 border-green-400 transition-all duration-700"
                class:bg-green-500={stomataOpen}
                class:bg-green-800={!stomataOpen}
                style="transform: translateX({stomataOpen ? -4 : 0}px);"
            ></div>
            <!-- Gap (ostiole) -->
            <div
                class="w-4 h-12 transition-all duration-700 flex flex-col items-center justify-center"
                class:bg-black={stomataOpen}
                class:bg-green-900={!stomataOpen}
                style="transform: scaleX({stomataOpen ? 1 : 0.2});"
            >
                {#if stomataOpen}
                    <!-- CO2 entering -->
                    <div class="text-[6px] text-gray-300 animate-bounce">CO₂↓</div>
                {/if}
            </div>
            <!-- Right guard -->
            <div
                class="w-8 h-14 rounded-r-full border-2 border-green-400 transition-all duration-700"
                class:bg-green-500={stomataOpen}
                class:bg-green-800={!stomataOpen}
                style="transform: translateX({stomataOpen ? 4 : 0}px);"
            ></div>

            <!-- Label -->
            <div class="absolute -bottom-4 text-[7px] whitespace-nowrap" class:text-green-300={stomataOpen} class:text-red-300={!stomataOpen}>
                Stomate {stomataOpen ? "OUVERT" : "FERMÉ"} {stomataOpen ? "🌬️" : "🔒"}
            </div>
        </div>

        <!-- COMPARISON BADGE (C3 vs C4 vs CAM) -->
        <div class="absolute top-2 right-2 text-[7px] bg-black/70 p-1.5 rounded border border-purple-500/50 leading-tight">
            <div class="text-purple-300 font-bold mb-1">COMPARAISON :</div>
            <div class="text-gray-400">C3 : Stomates ouverts le jour</div>
            <div class="text-yellow-400">C4 : Stomates ouverts le jour</div>
            <div class="text-purple-400 font-bold">CAM : Stomates ouverts LA NUIT</div>
        </div>
    </div>

    <!-- CONTROLS / STORY -->
    <div
        class="p-3 border-2 rounded relative shadow-lg transition-colors duration-700"
        class:bg-indigo-950={isNight}
        class:border-indigo-700={isNight}
        class:bg-amber-900={!isNight}
        class:border-amber-700={!isNight}
    >
        <h3
            class="font-bold mb-1 uppercase tracking-wide border-b border-white/10 pb-1"
            class:text-purple-300={isNight}
            class:text-amber-300={!isNight}
        >
            {steps[step].title}
        </h3>
        <p
            class="text-xs text-gray-300 leading-snug min-h-[40px] mb-2 font-mono"
        >
            {steps[step].text}
        </p>

        <button
            class="w-full text-white font-bold py-2 rounded border-b-4 active:border-b-0 active:translate-y-1 transition-all text-xs"
            class:bg-indigo-600={isNight}
            class:hover:bg-indigo-500={isNight}
            class:border-indigo-800={isNight}
            class:bg-amber-600={!isNight}
            class:hover:bg-amber-500={!isNight}
            class:border-amber-800={!isNight}
            on:click={nextStep}
        >
            {step === steps.length - 1
                ? "RECOMMENCER 🔄"
                : steps[step].action + " ▶"}
        </button>
    </div>
</div>

<style>
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
    }
    .animate-twinkle {
        animation: twinkle 2s ease-in-out infinite;
    }

    @keyframes malateFill {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(60px); opacity: 0; }
    }
    .animate-malate-fill {
        animation: malateFill 1s ease-in infinite;
    }

    @keyframes floatAround {
        0% { transform: translate(0, 0) scale(1); }
        25% { transform: translate(5px, -8px) scale(1.1); }
        50% { transform: translate(-3px, 5px) scale(0.9); }
        75% { transform: translate(8px, 3px) scale(1.05); }
        100% { transform: translate(0, 0) scale(1); }
    }
    .animate-float-around {
        animation: floatAround 3s ease-in-out infinite;
    }

    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(-30px); opacity: 0; }
    }
    .animate-float-up {
        animation: floatUp 1.5s ease-out infinite;
    }

    .animate-pulse-slow {
        animation: pulse 3s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
</style>
