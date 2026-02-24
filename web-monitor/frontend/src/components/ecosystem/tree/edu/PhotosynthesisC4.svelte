<script>
    import { createEventDispatcher } from "svelte";
    import { fade, scale } from "svelte/transition";
    const dispatch = createEventDispatcher();

    // Steps of the C4 Story
    let step = 0;

    const steps = [
        {
            title: "1. Capture Mésophylle 🛡️",
            text: "Ici, on ne rigole pas avec l'Oxygène. La PEPcase fixe le bicarbonate (HCO₃⁻) ultra-vite, bien plus rapide que Rubisco !",
            action: "CLIQUEZ SUR LE CO2",
        },
        {
            title: "2. Transformation C4 📦",
            text: "Le CO2 est fixé en Oxaloacétate (4C), puis converti en Malate. Un colis sécurisé à 4 carbones.",
            action: "EMBALLER LE CARBONE",
        },
        {
            title: "3. Transport Actif 🚚",
            text: "Le colis est expédié vers le bunker central (Gaine). Ça coûte de l'énergie, mais c'est sûr.",
            action: "ENVOYER LE COLIS",
        },
        {
            title: "4. Livraison Rubisco 🏭",
            text: "Dans la Gaine, le CO2 est relâché. Rubisco est saturée de CO2 : Rendement maximal !",
            action: "LIBÉRER ET SUCRER",
        },
    ];

    function nextStep() {
        if (step < steps.length - 1) {
            step++;
        } else {
            step = 0; // Loop or maybe finish?
        }
    }
</script>

<div class="flex flex-col h-full font-pixel text-white select-none">
    <!-- Header -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-white/20 pb-2 bg-[#F57F17]/90 p-2 rounded-t"
    >
        <button
            class="text-xs border border-white/30 px-2 py-1 rounded hover:bg-white/20 transition-colors"
            on:click={() => dispatch("back")}
        >
            ⬅ RETOUR
        </button>
        <span class="text-xs text-yellow-200">ANATOMIE DE KRANZ (C4)</span>
    </div>

    <!-- MAIN SCENE (Split Screen Cell View) -->
    <div
        class="relative flex-grow bg-[#2E7D32] border-4 border-[#1B5E20] rounded-lg overflow-hidden shadow-inner flex mb-2"
    >
        <!-- LEFT CELL: MESOPHYLL (The Collector) -->
        <div
            class="w-1/2 h-full border-r-4 border-[#1B5E20] relative bg-[#4CAF50] hover:bg-[#66BB6A] transition-colors flex flex-col items-center p-2 isolate"
        >
            <!-- Background Pattern -->
            <div
                class="absolute inset-0 opacity-10"
                style="background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, #000 10px, #000 11px);"
            ></div>

            <div
                class="text-[10px] text-green-100 font-bold mb-2 bg-black/40 px-2 rounded z-10"
            >
                MÉSOPHYLLE (Extérieur)
            </div>

            <!-- ENZYME PEPc -->
            <div
                class="absolute top-1/3 left-1/4 w-14 h-14 bg-green-700 rounded-lg border-2 border-green-400 flex items-center justify-center shadow-md z-20"
            >
                <span class="text-[8px] font-bold">PEPc</span>
            </div>

            <!-- CO2 Particle -->
            {#if step === 0}
                <button
                    class="absolute top-16 left-10 w-8 h-8 bg-gray-200 border-2 border-white animate-bounce flex items-center justify-center text-[10px] text-black font-bold z-50 rounded-full shadow-xl hover:scale-110 transition-transform cursor-magnify"
                    on:click={nextStep}
                >
                    CO2
                </button>
            {/if}
        </div>

        <!-- RIGHT CELL: BUNDLE SHEATH (The Bunker) -->
        <div
            class="w-1/2 h-full relative bg-[#F9A825] hover:bg-[#FBC02D] transition-colors flex flex-col items-center p-2 isolate"
        >
            <!-- Background Pattern -->
            <div
                class="absolute inset-0 opacity-10"
                style="background-image: radial-gradient(#000 1px, transparent 1px); background-size: 10px 10px;"
            ></div>

            <div
                class="text-[10px] text-yellow-100 font-bold mb-2 bg-black/40 px-2 rounded z-10"
            >
                GAINE (Bunker)
            </div>

            <!-- RUBISCO (Protected) -->
            <div
                class="absolute bottom-1/3 right-1/4 w-20 h-20 bg-[#EF6C00] rounded-xl border-4 border-[#E65100] flex items-center justify-center shadow-lg z-20"
            >
                <div
                    class="text-[8px] text-center leading-tight font-bold text-white shadow-black drop-shadow-md"
                >
                    RUBISCO<br /><span class="text-[6px] opacity-80"
                        >(VIP Only)</span
                    >
                </div>
            </div>
        </div>

        <!-- ANIMATIONS LAYER -->
        {#if step >= 1}
            <!-- The C4 Molecule (Malate) -->
            <button
                class="absolute w-10 h-10 bg-blue-600 border-2 border-white rounded-lg flex items-center justify-center text-[8px] font-bold z-50 transition-all duration-1000 shadow-[0_0_15px_rgba(33,150,243,0.8)] cursor-magnify"
                style="
                    top: 40%; 
                    left: {step === 1 ? '20%' : step === 2 ? '60%' : '75%'}; 
                    transform: {step === 3 ? 'scale(0)' : 'scale(1)'};
                "
                disabled={step !== 1 && step !== 2}
                on:click={() => (step === 1 || step === 2) && nextStep()}
            >
                📦 C4
            </button>
        {/if}

        {#if step === 3}
            <!-- Released CO2 in Bunker -->
            <div
                class="absolute bottom-1/3 right-1/4 w-8 h-8 bg-white/90 border border-black animate-ping flex items-center justify-center text-[8px] text-black font-bold z-50 pointer-events-none rounded-full"
            >
                CO2
            </div>
            <!-- Sugar particles -->
            <div class="absolute bottom-10 right-10 text-xl animate-float-up">
                🍬
            </div>
        {/if}
    </div>

    <!-- CONTROLS / STORY -->
    <div
        class="bg-[#3E2723] p-3 border-2 border-[#5D4037] rounded relative shadow-lg"
    >
        <h3
            class="text-yellow-400 font-bold mb-1 uppercase tracking-wide border-b border-white/10 pb-1"
        >
            {steps[step].title}
        </h3>
        <p
            class="text-xs text-gray-300 leading-snug min-h-[40px] mb-2 font-mono"
        >
            {steps[step].text}
        </p>

        <button
            class="w-full bg-[#E65100] hover:bg-[#EF6C00] text-white font-bold py-2 rounded border-b-4 border-[#BF360C] active:border-b-0 active:translate-y-1 transition-all text-xs"
            on:click={nextStep}
        >
            {step === steps.length - 1
                ? "RECHARGER LE CYCLE 🔄"
                : steps[step].action + " ▶"}
        </button>
    </div>
</div>

<style>
    @keyframes floatUp {
        0% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-30px);
            opacity: 0;
        }
    }
    .animate-float-up {
        animation: floatUp 1.5s ease-out infinite;
    }
</style>
