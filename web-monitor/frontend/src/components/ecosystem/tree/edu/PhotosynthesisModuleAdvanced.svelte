<script>
    import { createEventDispatcher, onMount } from "svelte";
    import Chart from "chart.js/auto";

    const dispatch = createEventDispatcher();

    // --- CHART STATE ---
    let canvas;
    let chart;
    let timeLabel = 0;

    // --- GAME STATE ---
    let atpCount = 0;
    let o2Count = 0;
    let step = 0;

    onMount(() => {
        const ctx = canvas.getContext("2d");
        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    {
                        label: "ATP (Énergie)",
                        borderColor: "#FFD700", // Gold
                        backgroundColor: "rgba(255, 215, 0, 0.2)",
                        data: [],
                        tension: 0.4,
                        fill: true,
                    },
                    {
                        label: "O2 (Oxygène)",
                        borderColor: "#4FC3F7", // Light Blue
                        backgroundColor: "rgba(79, 195, 247, 0.2)",
                        data: [],
                        tension: 0.4,
                        fill: true,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: false,
                scales: {
                    x: { display: false },
                    y: { beginAtZero: true, max: 10 },
                },
                plugins: {
                    legend: {
                        labels: {
                            color: "white",
                            font: { family: "monospace" },
                        },
                    },
                },
            },
        });

        const interval = setInterval(() => {
            if (!chart) return;
            timeLabel++;
            chart.data.labels.push(timeLabel);
            chart.data.datasets[0].data.push(atpCount);
            chart.data.datasets[1].data.push(o2Count);

            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
                chart.data.datasets[1].data.shift();
            }

            if (atpCount > 0) atpCount -= 0.1;
            if (atpCount < 0) atpCount = 0;
            chart.update();
        }, 1000);

        return () => clearInterval(interval);
    });

    function produceATP() {
        atpCount = Math.min(atpCount + 2, 10);
    }
    function produceO2() {
        o2Count += 1;
    }

    const steps = [
        {
            title: "1. Capture (PSII) ☀️",
            text: "Le Photon frappe le PSII. Excitation !",
            action: () => (step = 1),
        },
        {
            title: "2. Hydrolyse 💧",
            text: "L'eau est cassée : O2 libéré, électrons arrachés.",
            action: () => {
                step = 2;
                produceO2();
            },
        },
        {
            title: "3. Transport (Chaine) ⚡",
            text: "L'électron saute : PQ -> Cyt b6f -> PC.",
            action: () => (step = 3),
        },
        {
            title: "4. Recharge (PSI) → NADPH 🔋",
            text: "Le PSI recharge l'électron avec un 2ème photon. L'électron réduit NADP⁺ → NADPH (pouvoir réducteur).",
            action: () => (step = 4),
        },
        {
            title: "5. Synthèse (ATP + NADPH) ⚙️",
            text: "Les protons sortent par la turbine → ATP. Avec le NADPH du PSI, le Cycle de Calvin peut assembler le CO₂ en sucre.",
            action: () => {
                step = 0;
                produceATP();
            },
        },
    ];

    function nextStep() {
        if (steps[step].action) steps[step].action();
    }
</script>

<div class="flex flex-col h-full font-pixel text-white select-none">
    <!-- HEADER -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-white/20 pb-2 bg-[#1B5E20]/90 p-2 rounded-t"
    >
        <button
            class="text-xs border border-white/30 px-2 py-1 rounded hover:bg-white/20 transition-colors"
            on:click={() => dispatch("back")}
        >
            ⬅ RETOUR
        </button>
        <span class="text-xs text-yellow-400"
            >Niveau 4 : Z-SCHEME (COMPLEXE)</span
        >
    </div>

    <div
        class="flex flex-col md:flex-row flex-grow gap-2 h-full overflow-hidden"
    >
        <!-- LEFT: VISUALIZATION (70%) -->
        <div
            class="flex-grow relative bg-[#2E7D32] border-4 border-[#1B5E20] rounded-lg overflow-hidden shadow-inner group cursor-magnify"
            on:click={nextStep}
            on:keydown={(e) => e.key === "Enter" && nextStep()}
            role="button"
            tabindex="0"
        >
            <!-- BACKGROUND PARTICLES -->
            <div class="absolute inset-0 opacity-20 pointer-events-none">
                {#each Array(10) as _, i}
                    <div
                        class="absolute w-1 h-1 bg-white/30"
                        style="left: {Math.random() *
                            100}%; top: {Math.random() * 100}%"
                    ></div>
                {/each}
            </div>

            <!-- MEMBRANE (Lipid Bilayer) -->
            <div
                class="absolute bottom-10 left-0 w-full h-14 flex justify-around items-end px-2 z-10 bg-[#FBC02D]/10"
            >
                <div
                    class="absolute inset-0 bg-[#FBC02D]/90 border-y-4 border-[#F57F17]"
                ></div>

                <!-- 1. PSII (P680) -->
                <div
                    class="w-16 h-20 relative z-20 hover:scale-105 transition-transform"
                >
                    <div
                        class="absolute bottom-0 w-full h-full bg-green-600 rounded-t-lg border-2 border-green-800"
                    ></div>
                    <span
                        class="absolute top-2 left-1 text-[8px] font-bold text-white"
                        >PSII</span
                    >
                    {#if step === 1}
                        <div
                            class="absolute -top-4 right-0 w-6 h-6 bg-yellow-400 animate-ping rounded-full"
                        ></div>
                    {/if}
                </div>

                <!-- 2. PQ (Mobile) -->
                <div
                    class="w-8 h-8 bg-yellow-700 rounded border border-white/20 z-10 flex items-center justify-center {step ===
                    2
                        ? 'animate-bounce'
                        : ''}"
                >
                    <span class="text-[6px]">PQ</span>
                </div>

                <!-- 3. Cytochrome b6f -->
                <div
                    class="w-12 h-18 bg-blue-600 rounded-lg border-2 border-blue-800 z-20 flex items-center justify-center relative"
                >
                    <span class="text-[8px] mt-4">Cyt</span>
                </div>

                <!-- 4. PC (Mobile) -->
                <div
                    class="w-6 h-6 bg-cyan-500 rounded-full border border-cyan-300 z-10 flex items-center justify-center {step ===
                    3
                        ? 'animate-spin-slow'
                        : ''}"
                >
                    <span class="text-[6px] text-black">PC</span>
                </div>

                <!-- 5. PSI (P700) -->
                <div
                    class="w-14 h-22 bg-[#8BC34A] rounded-t-lg border-2 border-[#558B2F] z-20 relative"
                >
                    <span
                        class="absolute top-2 left-1 text-[8px] font-bold text-black/50"
                        >PSI</span
                    >
                    {#if step === 4}
                        <div
                            class="absolute -top-4 w-6 h-6 bg-yellow-300 animate-ping rounded-full"
                        ></div>
                    {/if}
                </div>

                <!-- 6. ATP Synthase -->
                <div class="w-12 h-26 relative z-20 ml-2">
                    <div
                        class="absolute bottom-0 w-8 h-8 bg-pink-700 rounded-sm left-2"
                    ></div>
                    <!-- Base -->
                    <div
                        class="absolute bottom-8 w-2 h-8 bg-pink-400 left-5"
                    ></div>
                    <!-- Stalk -->
                    <div
                        class="absolute top-0 left-0 w-12 h-10 bg-pink-500 rounded-full border-2 border-pink-300 flex items-center justify-center"
                        class:animate-spin-turbine={step === 0}
                    >
                        <!-- Head -->
                        <span class="text-[8px] font-bold text-white">ATP</span>
                    </div>
                </div>
            </div>

            <!-- ACTORS -->
            <!-- SUN -->
            <div class="absolute top-2 left-2 text-4xl animate-pulse">☀️</div>

            {#if step >= 1}
                <!-- Photon Travel -->
                <div
                    class="absolute top-6 left-8 w-3 h-3 bg-yellow-200 rounded-full animate-photon"
                ></div>
            {/if}

            <div
                class="absolute bottom-4 left-8 text-xs font-bold text-blue-200"
            >
                {#if step < 2}
                    H₂O
                {:else}
                    <span class="animate-pop">O₂ + 4H+</span>
                {/if}
            </div>

            {#if step === 0 && atpCount > atpCount - 0.2}
                <!-- Visual feedback for ATP creation -->
                <div
                    class="absolute bottom-32 right-8 text-yellow-300 font-bold animate-float-up"
                >
                    ✨ ATP
                </div>
            {/if}
        </div>

        <!-- RIGHT: DATA & CONTROLS (30%) -->
        <div class="w-full md:w-1/3 flex flex-col gap-2">
            <!-- LIVE GRAPH -->
            <div class="h-40 bg-black/80 border border-green-800 rounded p-2">
                <h4
                    class="text-[10px] text-green-400 mb-1 border-b border-green-900"
                >
                    DEEP ANALYSIS
                </h4>
                <div class="h-full w-full relative">
                    <canvas bind:this={canvas}></canvas>
                </div>
            </div>

            <!-- STORY CARD -->
            <div
                class="flex-grow bg-[#3E2723] p-3 border-2 border-[#5D4037] rounded shadow-lg overflow-y-auto"
            >
                <h3
                    class="text-yellow-300 font-bold mb-1 border-b border-white/10 pb-1"
                >
                    {steps[step].title}
                </h3>
                <p class="text-xs text-gray-300 mb-4">{steps[step].text}</p>
                <button
                    class="w-full bg-[#E65100] hover:bg-[#EF6C00] text-white font-bold py-2 rounded border-b-4 border-[#BF360C] active:border-b-0 active:translate-y-1 transition-all text-xs"
                    on:click={nextStep}
                >
                    ACTION ▶
                </button>
            </div>
        </div>
    </div>
</div>

<style>
    .animate-spin-slow {
        animation: spin 3s linear infinite;
    }
    .animate-spin-turbine {
        animation: spin 0.5s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }

    @keyframes photon {
        0% {
            transform: translate(0, 0);
            opacity: 1;
        }
        100% {
            transform: translate(40px, 100px);
            opacity: 0;
        }
    }
    .animate-photon {
        animation: photon 0.5s linear forwards;
    }

    @keyframes pop {
        0% {
            transform: scale(0);
        }
        80% {
            transform: scale(1.2);
        }
        100% {
            transform: scale(1);
        }
    }
    .animate-pop {
        animation: pop 0.3s ease-out forwards;
    }

    @keyframes floatUp {
        0% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-50px);
            opacity: 0;
        }
    }
    .animate-float-up {
        animation: floatUp 1s ease-out forwards;
    }
</style>
