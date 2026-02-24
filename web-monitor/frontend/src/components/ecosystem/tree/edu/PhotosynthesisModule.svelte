<script>
    import { createEventDispatcher, onMount } from "svelte";
    const dispatch = createEventDispatcher();

    // Steps of the Story Mode
    let step = 0;

    // PROPS (Real World Data)
    export let weather = null;

    // LAB MODE STATE
    let labMode = false;
    let plantType = "C3"; // C3, C4, CAM
    let stomataOpen = 50; // 0-100%
    let isNight = false; // For CAM

    // INTERNAL WEATHER STATE (Synced with Prop OR Manual Lab Override)
    let labWeather = "sunny";

    // REACTIVE: Sync Real Weather to Visuals (NORMAL MODE ONLY)
    $: if (!labMode) {
        if (weather && weather.weather && weather.weather.length > 0) {
            const main = weather.weather[0].main;
            if (main === "Rain" || main === "Drizzle") labWeather = "rain";
            else if (main === "Clouds") labWeather = "cloudy";
            else labWeather = "sunny";
        } else {
            labWeather = "sunny"; // Default
        }
    }

    const steps = [
        {
            title: "1. L'Attaque Solaire ☀️",
            text: "Le Photon frappe le Photosystème II (PS2). L'antenne collecte l'énergie.",
            action: "Clique sur le Soleil pour lancer le Photon !",
        },
        {
            title: "2. Le Sacrifice de l'Eau 💧",
            text: "L'énergie casse une molécule d'eau (H2O). On libère de l'Oxygène (O2) et des électrons.",
            action: "Clique sur PS2 pour casser l'eau !",
        },
        {
            title: "3. La Chaîne de Transport ⚡",
            text: "L'électron survolté saute de protéine en protéine (PSII → PSI). Il pompe des H+ au passage.",
            action: "Clique sur l'électron pour le faire voyager !",
        },
        {
            title: "4. Le Double Produit ⚙️",
            text: "Les H+ sortent par l'ATP Synthase → ATP. Et au PSI, l'électron réduit le NADP⁺ → NADPH. Ces deux molécules alimentent le Cycle de Calvin.",
            action: "Clique sur la turbine pour produire de l'énergie !",
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
        <div class="flex items-center gap-2">
            <h2 class="text-xl text-yellow-400 drop-shadow-md">
                🌿 La Photosynthèse
            </h2>
        </div>
        <div class="text-xs bg-white/20 px-2 py-1 rounded">
            Étape {step + 1}/{steps.length}
        </div>
    </div>

    <!-- MAIN SCENE (Schematic) -->
    <div
        class="relative flex-grow bg-[#1B5E20] border-4 border-[#2E7D32] rounded-lg overflow-hidden shadow-inner mb-4 flex flex-col"
    >
        <!-- VISUALIZATION AREA -->
        <div class="relative flex-grow w-full h-full">
            <!-- BACKGROUND DETAILS -->
            <div class="absolute inset-0 opacity-20 pointer-events-none">
                {#each Array(10) as _, i}
                    <div
                        class="absolute w-1 h-1 bg-white/30"
                        style="left: {Math.random() *
                            100}%; top: {Math.random() * 100}%"
                    ></div>
                {/each}
            </div>

            <!-- C3 STANDARD VIEW (The existing MEMBRANE code) -->
            <!-- MEMBRANE (Lipid Bilayer) -->
            <div
                class="absolute bottom-10 left-0 w-full h-14 flex justify-around items-end px-4 z-10"
            >
                <!-- Bilayer Texture Background -->
                <div
                    class="absolute inset-0 bg-[#FBC02D]/90 border-y-4 border-[#F57F17] flex flex-col justify-between py-1 px-1"
                >
                    <div
                        class="w-full h-1 border-b border-dashed border-[#F9A825]/50 opacity-50"
                    ></div>
                    <div
                        class="w-full h-1 border-t border-dashed border-[#F9A825]/50 opacity-50"
                    ></div>
                </div>

                <!-- PROTEIN: PS2 (Photosystem II) -->
                <div
                    class="w-20 h-24 relative cursor-magnify hover:scale-105 active:scale-95 transition-transform group z-20"
                    on:click={() => step === 1 && nextStep()}
                    on:keydown={(e) =>
                        step === 1 && e.key === "Enter" && nextStep()}
                    role="button"
                    tabindex="0"
                >
                    <div
                        class="absolute bottom-0 left-0 w-10 h-20 bg-green-600 rounded-t-[15px] border-2 border-green-800"
                    ></div>
                    <div
                        class="absolute bottom-0 right-0 w-10 h-20 bg-green-500 rounded-t-[15px] border-2 border-green-700"
                    ></div>
                    <div
                        class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-8 h-4 bg-gray-400 rounded-full border border-gray-600"
                    ></div>
                    <div
                        class="absolute top-2 left-2 w-3 h-3 bg-green-300 rounded-full opacity-80"
                    ></div>
                    <div
                        class="absolute top-2 right-2 w-3 h-3 bg-green-300 rounded-full opacity-80"
                    ></div>
                    <span
                        class="absolute top-8 left-1/2 -translate-x-1/2 text-[10px] font-bold text-white drop-shadow-md"
                        >PSII</span
                    >
                    {#if step === 1}
                        <div
                            class="absolute -top-4 right-0 w-8 h-8 bg-yellow-400 animate-ping rounded-full z-30"
                        ></div>
                    {/if}
                </div>

                <!-- PROTEIN: Plastoquinone -->
                <div
                    class="w-8 h-8 bg-yellow-700 rounded border border-white/20 flex items-center justify-center absolute bottom-16 left-[28%] z-10 opacity-80"
                >
                    <span class="text-[8px]">PQ</span>
                </div>

                <!-- PROTEIN: Cytochrome b6f -->
                <div
                    class="w-16 h-22 bg-blue-600 rounded-[10px] border-2 border-blue-800 relative flex items-center justify-center z-20"
                >
                    <div
                        class="w-full h-2 bg-blue-400 absolute top-4 opacity-50"
                    ></div>
                    <div
                        class="w-full h-2 bg-blue-400 absolute bottom-4 opacity-50"
                    ></div>
                    <span class="text-[10px] font-bold text-white">Cyt</span>
                    <span class="text-[8px] text-blue-200 absolute bottom-2"
                        >b6f</span
                    >
                </div>

                <!-- PROTEIN: Plastocyanin -->
                <div
                    class="w-6 h-6 bg-cyan-500 rounded-full border border-cyan-300 flex items-center justify-center absolute bottom-20 left-[55%] z-10 opacity-80 animate-pulse"
                >
                    <span class="text-[6px] text-black font-bold">PC</span>
                </div>

                <!-- PROTEIN: PS1 -->
                <div
                    class="w-16 h-24 bg-green-400 rounded-t-[20px] border-2 border-green-600 relative flex items-center justify-center z-20"
                >
                    <span class="text-[10px] font-bold text-black/50">PSI</span>
                    <div
                        class="absolute top-4 w-4 h-4 bg-yellow-600 rounded-full border border-yellow-800"
                    ></div>
                </div>

                <!-- PROTEIN: ATP Synthase -->
                <div
                    class="w-14 h-28 relative cursor-magnify group z-20 ml-2"
                    on:click={() => step === 3 && nextStep()}
                    on:keydown={(e) =>
                        step === 3 && e.key === "Enter" && nextStep()}
                    role="button"
                    tabindex="0"
                >
                    <div
                        class="absolute bottom-2 left-1/2 -translate-x-1/2 w-10 h-10 bg-pink-700 rounded-sm border-2 border-pink-900"
                    ></div>
                    <div
                        class="absolute bottom-10 left-1/2 -translate-x-1/2 w-3 h-10 bg-pink-400 border border-pink-600"
                    ></div>
                    <div
                        class="absolute top-0 left-1/2 -translate-x-1/2 w-14 h-12 bg-pink-500 rounded-full border-2 border-pink-300 flex items-center justify-center shadow-md transition-transform"
                        class:animate-spin-slow={step === 3}
                    >
                        <div
                            class="w-12 h-12 border-4 border-dashed border-white/30 rounded-full"
                        ></div>
                        <span
                            class="absolute text-[10px] font-bold text-white drop-shadow-md"
                            >ATP</span
                        >
                    </div>
                </div>
            </div>

            <!-- ACTORS (Standard C3) -->
            <!-- SUN -->
            <div
                class="absolute top-4 left-4 text-5xl cursor-magnify hover:scale-110 transition-transform z-30 {step ===
                0
                    ? 'animate-bounce drop-shadow-[0_0_10px_orange]'
                    : 'opacity-50 grayscale'}"
                on:click={() => step === 0 && nextStep()}
                on:keydown={(e) =>
                    step === 0 && e.key === "Enter" && nextStep()}
                role="button"
                tabindex="0"
            >
                ☀️
            </div>

            <!-- PHOTON -->
            {#if step >= 1}
                <div
                    class="absolute top-8 left-12 w-4 h-4 bg-yellow-300 border border-white rounded-full animate-photon-travel z-20 shadow-[0_0_8px_yellow]"
                ></div>
            {/if}

            <!-- WATER MOLECULE -->
            <div
                class="absolute bottom-4 left-14 text-sm flex gap-1 z-20 font-bold"
            >
                {#if step < 2}
                    <span class="text-blue-200">H₂O</span>
                {:else}
                    <span class="text-blue-300 animate-proton-pop absolute"
                        >H+</span
                    >
                    <span class="text-white animate-oxygen-escape absolute ml-4"
                        >O₂</span
                    >
                {/if}
            </div>

            <!-- ELECTRON -->
            {#if step >= 2}
                <div
                    class="absolute w-4 h-4 bg-yellow-200 border-2 border-white rounded-full shadow-[0_0_10px_yellow] z-40 transition-all duration-[2000ms]"
                    style="left: {step === 2
                        ? '18%'
                        : step === 3
                          ? '85%'
                          : '50%'}; bottom: {step === 2 ? '80px' : '60px'};"
                    class:animate-electron-hop={step === 2}
                    on:click={() => step === 2 && nextStep()}
                    on:keydown={(e) =>
                        step === 2 && e.key === "Enter" && nextStep()}
                    role="button"
                    tabindex="0"
                >
                    <div
                        class="hidden group-hover:block absolute -top-4 text-[8px] bg-black text-white px-1"
                    >
                        e-
                    </div>
                </div>
            {/if}

            {#if step === 3}
                <div
                    class="absolute bottom-32 right-8 text-yellow-300 font-bold text-xl animate-float-up z-50"
                >
                    ✨ ATP!
                </div>
                <div
                    class="absolute bottom-32 right-16 text-yellow-300 font-bold text-sm animate-float-up z-50"
                    style="animation-delay: 0.5s"
                >
                    ✨
                </div>
            {/if}
        </div>
    </div>

    <!-- TEXT BOX -->
    <div class="bg-[#3E2723] p-3 border-2 border-[#5D4037] relative shadow-lg">
        <h3 class="text-yellow-300 font-bold mb-1 uppercase tracking-wide">
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
                    ? "PARTICULE SUIVANTE ⚡"
                    : "CONTINUER ▶"}
            </button>
        </div>
    </div>
</div>

<style>
    /* PHOTON TRAJECTORY */
    @keyframes photonTravel {
        0% {
            transform: translate(0, 0) scale(0.5);
            opacity: 1;
        }
        100% {
            transform: translate(50px, 150px) scale(2);
            opacity: 0;
        }
    }
    .animate-photon-travel {
        animation: photonTravel 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)
            forwards;
    }

    /* EXPLOSION */
    @keyframes protonPop {
        0% {
            transform: translate(0, 0) scale(1);
        }
        50% {
            transform: translate(-10px, -20px) scale(1.5);
            color: #ffeb3b;
        }
        100% {
            transform: translate(-20px, 0) scale(1);
            opacity: 0.5;
        }
    }
    .animate-proton-pop {
        animation: protonPop 1s ease-out forwards;
    }

    @keyframes oxygenEscape {
        0% {
            transform: translate(0, 0);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        100% {
            transform: translate(20px, -100px) rotate(90deg);
            opacity: 0;
        }
    }
    .animate-oxygen-escape {
        animation: oxygenEscape 2s ease-in forwards;
    }

    /* HOPPING ELECTRON */
    @keyframes electronHop {
        0% {
            transform: translateY(0);
        }
        25% {
            transform: translateY(-20px);
        }
        50% {
            transform: translateY(0);
        }
        75% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0);
        }
    }
    .animate-electron-hop {
        animation: electronHop 2s ease-in-out infinite;
    }

    @keyframes spinSlow {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    .animate-spin-slow {
        animation: spinSlow 3s linear infinite;
    }

    @keyframes floatUp {
        0% {
            transform: translateY(0) scale(0.5);
            opacity: 0;
        }
        20% {
            opacity: 1;
            transform: translateY(-10px) scale(1.2);
        }
        100% {
            transform: translateY(-60px) scale(1);
            opacity: 0;
        }
    }
    .animate-float-up {
        animation: floatUp 1.5s ease-out infinite;
    }

    @keyframes rainDrop {
        0% {
            transform: translateY(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
            opacity: 1;
        }
        100% {
            transform: translateY(300px);
            opacity: 0;
        }
    }
</style>
