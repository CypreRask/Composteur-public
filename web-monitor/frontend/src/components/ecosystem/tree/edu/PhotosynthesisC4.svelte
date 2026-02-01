<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    // Steps of the C4 Story
    let step = 0;

    const steps = [
        {
            title: "1. Capture Avancée (Mésophylle) 🛡️",
            text: "Contrairement à l'arbre, la capture du CO2 se fait ici, dans une cellule 'bouclier' externe.",
            action: "Cliquez sur le CO2 pour le capturer !",
        },
        {
            title: "2. La Transformation C4 📦",
            text: "Le CO2 est transformé en Malate (une molécule à 4 carbones), un 'colis' stable et transportable.",
            action: "Cliquez pour emballer le Carbone !",
        },
        {
            title: "3. Le Transport Actif 🚚",
            text: "Le colis C4 est pompé vers la cellule centrale (Gaine). C'est ce transport qui consomme de l'énergie.",
            action: "Cliquez pour envoyer le colis !",
        },
        {
            title: "4. La Livraison (Rubisco) 🏭",
            text: "Dans la Gaine (bunker hermétique), le CO2 est relâché devant Rubisco. Concentration x10 !",
            action: "Cliquez pour libérer le CO2 concentré !",
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
        <h2 class="text-xl text-green-400 drop-shadow-md">
            🧪 Photosynthèse C4
        </h2>
        <div class="text-xs bg-white/20 px-2 py-1 rounded">
            Étape {step + 1}/{steps.length}
        </div>
    </div>

    <!-- MAIN SCENE (Split Screen Cell View) -->
    <div
        class="relative flex-grow bg-[#2E7D32] border-4 border-[#1B5E20] rounded-lg overflow-hidden shadow-inner mb-4 flex"
    >
        <defs>
            <pattern
                id="grid"
                width="10"
                height="10"
                patternUnits="userSpaceOnUse"
            >
                <path
                    d="M 10 0 L 0 0 0 10"
                    fill="none"
                    stroke="black"
                    stroke-opacity="0.1"
                />
            </pattern>
        </defs>

        <!-- LEFT CELL: MESOPHYLL (The Collector) -->
        <div
            class="w-1/2 h-full border-r-4 border-[#1B5E20] relative bg-[#4CAF50] bg-opacity-20 flex flex-col items-center p-2"
        >
            <div
                class="text-[10px] text-green-300 font-bold mb-2 uppercase tracking-widest bg-black/50 px-2 rounded"
            >
                Mésophylle
            </div>

            <!-- ENZYME PEPc -->
            <div
                class="absolute top-1/3 left-1/4 w-12 h-12 bg-green-600 rounded-sm border-2 border-green-400 flex items-center justify-center"
            >
                <span class="text-[8px]">PEPc</span>
            </div>

            <!-- CO2 Particle -->
            {#if step === 0}
                <div
                    class="absolute top-10 left-10 w-6 h-6 bg-gray-300 border border-black animate-bounce cursor-pointer flex items-center justify-center text-[8px] text-black font-bold z-50"
                    on:click={nextStep}
                    on:keydown={(e) => e.key === 'Enter' && nextStep()}
                    role="button"
                    tabindex="0"
                >
                    CO2
                </div>
            {/if}
        </div>

        <!-- RIGHT CELL: BUNDLE SHEATH (The Bunker) -->
        <div
            class="w-1/2 h-full relative bg-[#F9A825] bg-opacity-20 flex flex-col items-center p-2"
        >
            <div
                class="text-[10px] text-yellow-300 font-bold mb-2 uppercase tracking-widest bg-black/50 px-2 rounded"
            >
                Gaine
            </div>

            <!-- RUBISCO (Protected) -->
            <div
                class="absolute bottom-1/3 right-1/4 w-16 h-16 bg-yellow-700 rounded-sm border-4 border-yellow-500 flex items-center justify-center shadow-lg"
            >
                <div class="text-[8px] text-center leading-tight">
                    RUBISCO<br /><span class="text-[6px] opacity-70"
                        >(Protégée)</span
                    >
                </div>
            </div>
        </div>

        <!-- ANIMATIONS & INTERACTION LAYERS -->

        <!-- Step 1->2: CO2 merging with PEP -->
        {#if step >= 1}
            <!-- The C4 Molecule (Malate) -->
            <div
                class="absolute w-8 h-8 bg-blue-500 border-2 border-white flex items-center justify-center text-[8px] font-bold z-50 transition-all duration-1000"
                style="top: 40%; left: {step === 1
                    ? '20%'
                    : step === 2
                      ? '60%'
                      : '75%'}; transform: {step === 3
                    ? 'scale(0)'
                    : 'scale(1)'}"
                class:cursor-pointer={step === 1 || step === 2}
                on:click={() => (step === 1 || step === 2) && nextStep()}
                on:keydown={(e) => (step === 1 || step === 2) && e.key === 'Enter' && nextStep()}
                role="button"
                tabindex="0"
            >
                C4
            </div>
        {/if}

        {#if step === 3}
            <!-- Released CO2 in Bunker -->
            <div
                class="absolute bottom-1/3 right-1/4 w-6 h-6 bg-gray-200 border border-black animate-ping flex items-center justify-center text-[8px] text-black font-bold z-50 pointer-events-none"
            >
                CO2
            </div>
            <!-- Sugar produced -->
            <div
                class="absolute bottom-10 right-10 w-4 h-4 bg-yellow-300 animate-spin-slow"
            ></div>
        {/if}
    </div>

    <!-- TEXT BOX (Shared Style) -->
    <div class="bg-[#3E2723] p-3 border-2 border-[#5D4037] relative shadow-lg">
        <h3 class="text-green-300 font-bold mb-1 uppercase tracking-wide">
            {steps[step].title}
        </h3>
        <p class="text-sm text-gray-200 leading-snug min-h-[40px]">
            {steps[step].text}
        </p>

        <div class="mt-2 flex justify-end items-center">
            <button
                class="bg-[#ff9100] text-black font-bold px-4 py-1 border-b-4 border-[#e65100] active:border-b-0 active:translate-y-1 hover:bg-[#ffab40] transition-colors rounded text-xs"
                on:click={() => nextStep()}
            >
                {step === steps.length - 1
                    ? "RECHARGER LA POMPE 🔄"
                    : "CONTINUER ▶"}
            </button>
        </div>
    </div>
</div>

<style>
    @keyframes spinSlow {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    .animate-spin-slow {
        animation: spinSlow 4s linear infinite;
    }
</style>
