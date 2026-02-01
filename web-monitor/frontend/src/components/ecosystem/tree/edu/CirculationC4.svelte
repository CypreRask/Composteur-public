<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    // Steps
    let step = 0;

    const steps = [
        {
            title: "1. L'Anatomie en Couronne (Kranz) 👑",
            text: "Coupe transversale d'une feuille C4. Regardez cette structure en anneaux concentriques.",
            action: "Cliquez pour voir la coupe !",
        },
        {
            title: "2. Le Blindage (Gaine) 🛡️",
            text: "Les vaisseaux (Xylème/Phloème) sont entourés d'une gaine hermétique. Rien ne fuit !",
            action: "Cliquez pour construire le blindage !",
        },
        {
            title: "3. Haute Pression 💥",
            text: "Grâce à ce blindage, la sève circule à haute pression sans évaporation excessive.",
            action: "Cliquez pour mettre sous pression !",
        },
        {
            title: "4. Efficience de l'Eau 💧",
            text: "Résultat : La plante C4 boit 2x moins d'eau que l'arbre pour la même croissance.",
            action: "Terminer la leçon",
        },
    ];

    function nextStep() {
        if (step < steps.length - 1) {
            step++;
        } else {
            step = 0; // Loop relative or end
        }
    }
</script>

<div class="flex flex-col h-full font-pixel text-white select-none">
    <!-- Header -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-white/20 pb-2"
    >
        <h2 class="text-xl text-blue-400 drop-shadow-md">
            🩸 Circulation C4 (Kranz)
        </h2>
        <div class="text-xs bg-white/20 px-2 py-1 rounded">
            Étape {step + 1}/{steps.length}
        </div>
    </div>

    <!-- MAIN SCENE (Cross Section View) -->
    <div
        class="relative flex-grow bg-[#263238] border-4 border-[#37474F] rounded-lg overflow-hidden shadow-inner mb-4 flex justify-center items-center"
    >
        <!-- KRANZ ANATOMY (Concentric Squares) -->
        <div class="relative w-64 h-64 flex items-center justify-center">
            <!-- LAYER 3: MESOPHYLL (Outer Ring) -->
            {#if step >= 0}
                <div
                    class="absolute w-64 h-64 bg-[#2E7D32] border-4 border-[#1B5E20] flex flex-wrap content-start p-1 transition-all duration-1000 origin-center"
                    style="transform: {step === 0 ? 'scale(0.8)' : 'scale(1)'}"
                >
                    <span
                        class="absolute top-1 left-1 text-[10px] text-white bg-black/50 px-1"
                        >MÉSOPHYLLE</span
                    >
                    <!-- Cellular Texture -->
                    {#each Array(40) as _, i}
                        <div
                            class="w-4 h-4 bg-[#43A047] border border-[#2E7D32] opacity-50"
                        ></div>
                    {/each}

                    {#if step === 0}
                        <div
                            class="absolute inset-0 flex items-center justify-center z-50 cursor-pointer"
                            on:click={nextStep}
                            on:keydown={(e) => e.key === 'Enter' && nextStep()}
                            role="button"
                            tabindex="0"
                        >
                            <div
                                class="w-16 h-16 border-4 border-white animate-ping rounded-full"
                            ></div>
                        </div>
                    {/if}
                </div>
            {/if}

            <!-- LAYER 2: BUNDLE SHEATH (Inner Ring) -->
            {#if step >= 1}
                <div
                    class="absolute w-40 h-40 bg-[#F9A825] border-4 border-[#F57F17] shadow-xl flex items-center justify-center z-10 transition-all duration-500 animate-zoom-in"
                >
                    <span
                        class="absolute top-1 right-1 text-[10px] text-black bg-white/50 px-1 font-bold"
                        >GAINE</span
                    >

                    {#if step === 1}
                        <div
                            class="absolute inset-0 flex items-center justify-center z-50 cursor-pointer"
                            on:click={nextStep}
                            on:keydown={(e) => e.key === 'Enter' && nextStep()}
                            role="button"
                            tabindex="0"
                        >
                            <div
                                class="text-xs font-bold text-black bg-white px-2 py-1 rounded animate-bounce"
                            >
                                CONSTRUIRE 🛡️
                            </div>
                        </div>
                    {/if}
                </div>
            {/if}

            <!-- LAYER 1: VASCULAR BUNDLE (Center) -->
            {#if step >= 2}
                <div
                    class="absolute w-24 h-24 bg-[#ECEFF1] border-4 border-gray-400 z-20 overflow-hidden flex flex-col"
                >
                    <!-- XYLEM (Water) -->
                    <div
                        class="w-full h-1/2 bg-blue-500 relative overflow-hidden"
                    >
                        <span
                            class="absolute top-0 left-1 text-[8px] text-white"
                            >XYLÈME (EAU)</span
                        >
                        <!-- Rushing Water Animation -->
                        <div
                            class="absolute inset-0 flex flex-col gap-1 animate-flow-fast opacity-50"
                        >
                            <div class="w-full h-1 bg-white"></div>
                            <div class="w-full h-1 bg-white"></div>
                            <div class="w-full h-1 bg-white"></div>
                            <div class="w-full h-1 bg-white"></div>
                        </div>
                    </div>

                    <!-- PHLOEM (Sugar) -->
                    <div
                        class="w-full h-1/2 bg-orange-500 relative overflow-hidden"
                    >
                        <span
                            class="absolute bottom-0 left-1 text-[8px] text-white"
                            >PHLOÈME (SUCRE)</span
                        >
                        <div
                            class="absolute inset-0 flex flex-col gap-2 animate-flow-slow"
                        >
                            <div
                                class="w-4 h-4 bg-yellow-300 rounded-full ml-8"
                            ></div>
                            <div
                                class="w-4 h-4 bg-yellow-300 rounded-full ml-2"
                            ></div>
                        </div>
                    </div>

                    {#if step === 2}
                        <div
                            class="absolute inset-0 flex items-center justify-center z-50 cursor-pointer"
                            on:click={nextStep}
                            on:keydown={(e) => e.key === 'Enter' && nextStep()}
                            role="button"
                            tabindex="0"
                        >
                            <span class="text-2xl">⚡</span>
                        </div>
                    {/if}
                </div>
            {/if}

            <!-- Step 3: Water Efficiency Overlay -->
            {#if step === 3}
                <div
                    class="absolute -right-16 top-0 w-24 bg-blue-900/90 border border-blue-500 p-2 text-[8px] rounded z-50 animate-fade-in"
                >
                    <div class="font-bold text-blue-300 mb-1">EFFICIENCE</div>
                    <div class="flex items-center gap-1 mb-1">
                        <div class="w-10 h-2 bg-blue-500 rounded"></div>
                         C4
                    </div>
                    <div class="flex items-center gap-1 opacity-50">
                        <div class="w-20 h-2 bg-blue-500 rounded"></div>
                         C3
                    </div>
                </div>
            {/if}
        </div>
    </div>

    <!-- TEXT BOX -->
    <div class="bg-[#3E2723] p-3 border-2 border-[#5D4037] relative shadow-lg">
        <h3 class="text-blue-300 font-bold mb-1 uppercase tracking-wide">
            {steps[step].title}
        </h3>
        <p class="text-sm text-gray-200 leading-snug min-h-[40px]">
            {steps[step].text}
        </p>
        <div class="mt-2 flex justify-end items-center">
            <button
                class="bg-[#ff9100] text-black font-bold px-4 py-1 border-b-4 border-[#e65100] rounded text-xs active:translate-y-1"
                on:click={() => nextStep()}
            >
                {step === steps.length - 1 ? "REVOIR" : "SUIVANT ▶"}
            </button>
        </div>
    </div>
</div>

<style>
    @keyframes zoomIn {
        from {
            transform: scale(0);
        }
        to {
            transform: scale(1);
        }
    }
    .animate-zoom-in {
        animation: zoomIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    @keyframes flowFast {
        from {
            transform: translateY(-10px);
        }
        to {
            transform: translateY(10px);
        }
    }
    .animate-flow-fast {
        animation: flowFast 0.2s linear infinite;
    }

    @keyframes flowSlow {
        from {
            transform: translateY(-20px);
        }
        to {
            transform: translateY(20px);
        }
    }
    .animate-flow-slow {
        animation: flowSlow 1s linear infinite;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateX(10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out forwards;
    }
</style>
