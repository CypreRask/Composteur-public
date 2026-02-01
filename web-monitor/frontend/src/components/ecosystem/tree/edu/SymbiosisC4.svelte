<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    // Steps of the C4 Symbiosis Story
    let step = 0;

    const steps = [
        {
            title: "1. Le Contact Intime (Endo) 🤝",
            text: "Contrairement à l'arbre, ici le champignon NE reste PAS dehors. Il perce la paroi de la racine !",
            action: "Cliquez pour percer la paroi !",
        },
        {
            title: "2. L'Arbuscule (L'Arbre Intérieur) 🌳",
            text: "Le champignon se divise à l'infini DANS la cellule pour former un 'petit arbre' (Arbuscule).",
            action: "Cliquez pour déployer l'arbuscule !",
        },
        {
            title: "3. L'Échange Direct ⚡",
            text: "La surface de contact est immense ! Le sucre (jaune) sort de la plante, l'eau/azote (bleu) entre.",
            action: "Cliquez pour lancer les échanges !",
        },
        {
            title: "4. La Glomaline (Colle) 🏗️",
            text: "Ces champignons produisent de la 'Super-Glu' pour le sol, stockant massivement du carbone.",
            action: "Cliquez pour solidifier le sol !",
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
        <h2 class="text-xl text-cyan-400 drop-shadow-md">
            🍄 Endomycorhize (C4)
        </h2>
        <div class="text-xs bg-white/20 px-2 py-1 rounded">
            Étape {step + 1}/{steps.length}
        </div>
    </div>

    <!-- MAIN SCENE (Zoom on Single Root Cell) -->
    <div
        class="relative flex-grow bg-[#3E2723] border-4 border-[#5D4037] rounded-lg overflow-hidden shadow-inner mb-4 flex justify-center items-center"
    >
        <!-- Background Soil Texture -->
        <div
            class="absolute inset-0 opacity-20 pointer-events-none"
            style="background-image: radial-gradient(#5D4037 1px, transparent 1px); background-size: 10px 10px;"
        ></div>

        <!-- THE ROOT CELL (Huge Box) -->
        <div
            class="w-64 h-64 border-8 border-[#8D6E63] bg-[#A1887F] relative shadow-2xl"
        >
            <span
                class="absolute top-2 right-2 text-[8px] text-[#3E2723] opacity-70"
                >CELLULE RACINAIRE</span
            >

            <!-- Cytoplasm -->
            <div class="absolute inset-0 bg-[#BCAAA4] opacity-50"></div>

            <!-- STEP 0: Hyphae approaching from outside -->
            <div
                class="absolute -left-20 top-1/2 -translate-y-1/2 w-24 h-4 bg-cyan-400 border-y border-cyan-600 transition-all duration-1000"
                style="transform: {step >= 1
                    ? 'translateX(20px)'
                    : 'translateX(0)'}"
            >
                <!-- Hyphae Tip -->
                <div class="absolute right-0 top-0 w-4 h-4 bg-cyan-300"></div>

                {#if step === 0}
                    <div
                        class="absolute -right-8 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full border-2 border-cyan-400 animate-ping opacity-50 cursor-pointer z-50"
                        on:click={nextStep}
                        on:keydown={(e) => e.key === 'Enter' && nextStep()}
                        role="button"
                        tabindex="0"
                    ></div>
                {/if}
            </div>

            <!-- STEP 1 & 2: Penetration & Arbuscule Formation -->
            {#if step >= 1}
                <!-- The Penetration Point (Breaking the wall) -->
                <div
                    class="absolute left-[-4px] top-1/2 -translate-y-1/2 w-4 h-8 bg-cyan-500 z-10"
                ></div>

                <!-- The Trunk inside -->
                <div
                    class="absolute left-0 top-1/2 -translate-y-1/2 h-2 bg-cyan-400 transition-all duration-1000"
                    style="width: {step >= 2 ? '40px' : '10px'}"
                ></div>

                <!-- THE ARBUSCULE (Fractal Tree) -->
                {#if step >= 2}
                    <g class="absolute left-10 top-1/2 -translate-y-1/2">
                        <!-- Upper Branch -->
                        <div
                            class="absolute bottom-0 left-0 w-1 h-12 bg-cyan-400 origin-bottom -rotate-45 animate-grow-branch"
                        ></div>
                        <div
                            class="absolute bottom-8 left-6 w-1 h-8 bg-cyan-400 origin-bottom -rotate-45 animate-grow-branch delay-100"
                        ></div>

                        <!-- Lower Branch -->
                        <div
                            class="absolute top-0 left-0 w-1 h-12 bg-cyan-400 origin-top rotate-45 animate-grow-branch"
                        ></div>
                        <div
                            class="absolute top-8 left-6 w-1 h-8 bg-cyan-400 origin-top rotate-45 animate-grow-branch delay-100"
                        ></div>

                        <!-- Center Branch -->
                        <div
                            class="absolute top-0 left-0 w-24 h-1 bg-cyan-400 animate-grow-width"
                        ></div>

                        <!-- Fine details (Pixels) appearing -->
                        <div
                            class="absolute left-16 top-[-20px] w-8 h-8 border border-cyan-300 opacity-50 animate-pulse delay-200"
                        ></div>
                        <div
                            class="absolute left-12 bottom-[-30px] w-6 h-6 border border-cyan-300 opacity-50 animate-pulse delay-300"
                        ></div>

                        {#if step === 2}
                            <div
                                class="absolute left-20 top-0 w-8 h-8 rounded-full border-2 border-yellow-400 animate-bounce cursor-pointer z-50 flex items-center justify-center text-[8px]"
                                on:click={nextStep}
                                on:keydown={(e) => e.key === 'Enter' && nextStep()}
                                role="button"
                                tabindex="0"
                            >
                                🔁
                            </div>
                        {/if}
                    </g>
                {/if}
            {/if}

            <!-- STEP 3: Exchange Particles -->
            {#if step >= 3}
                <!-- Sugar (Yellow) Out -->
                <div
                    class="absolute left-1/2 top-10 w-2 h-2 bg-yellow-400 animate-rain"
                ></div>
                <div
                    class="absolute left-3/4 top-20 w-2 h-2 bg-yellow-400 animate-rain delay-100"
                ></div>

                <!-- Water (Blue) In -->
                <div
                    class="absolute left-1/4 bottom-10 w-2 h-2 bg-blue-400 animate-rise"
                ></div>
                <div
                    class="absolute left-10 bottom-20 w-2 h-2 bg-blue-400 animate-rise delay-100"
                ></div>

                <!-- Glomaline Glue Effect -->
                {#if step === 4}
                    <div
                        class="absolute inset-0 bg-green-900/30 animate-pulse border-4 border-green-500"
                    ></div>
                    <div
                        class="absolute bottom-2 right-2 text-green-300 text-xs font-bold"
                    >
                        SOL STRUCTURÉ (GLOMALINE)
                    </div>
                {/if}

                {#if step === 3}
                    <div
                        class="absolute right-4 bottom-4 w-8 h-8 bg-green-600 border border-white animate-bounce cursor-pointer z-50 flex items-center justify-center text-xs"
                        on:click={nextStep}
                        on:keydown={(e) => e.key === 'Enter' && nextStep()}
                        role="button"
                        tabindex="0"
                    >
                        🏗️
                    </div>
                {/if}
            {/if}
        </div>
    </div>

    <!-- TEXT BOX -->
    <div class="bg-[#3E2723] p-3 border-2 border-[#5D4037] relative shadow-lg">
        <h3 class="text-cyan-300 font-bold mb-1 uppercase tracking-wide">
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
                {step === steps.length - 1 ? "REVOIR" : "CONTINUER ▶"}
            </button>
        </div>
    </div>
</div>

<style>
    @keyframes growBranch {
        from {
            transform: scaleY(0);
        }
        to {
            transform: scaleY(1);
        }
    }
    .animate-grow-branch {
        animation: growBranch 1s ease-out forwards;
    }

    @keyframes growWidth {
        from {
            width: 0;
        }
        to {
            width: 96px;
        } /* w-24 */
    }
    .animate-grow-width {
        animation: growWidth 1s ease-out forwards;
    }

    @keyframes rain {
        0% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(100px);
            opacity: 0;
        }
    }
    .animate-rain {
        animation: rain 1.5s infinite linear;
    }

    @keyframes rise {
        0% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px);
            opacity: 0;
        }
    }
    .animate-rise {
        animation: rise 1.5s infinite linear;
    }
</style>
