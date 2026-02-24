<script>
    import { createEventDispatcher, onMount, onDestroy } from "svelte";
    import { fly, fade } from "svelte/transition";
    const dispatch = createEventDispatcher();

    export let weather = null;

    // Simulation Props
    $: temperature = weather?.main?.temp || 20;
    $: isSunny = weather?.weather?.[0]?.main === "Clear";

    // --- BIO-MARKERS ---
    let activeMarker = null;
    const MARKERS = [
        {
            id: "thylakoid",
            x: 25,
            y: 30,
            label: "Thylakoïde (Grana)",
            text: "Les panneaux solaires ! C'est ici que l'énergie lumineuse est capturée pour casser les molécules d'eau (Phase Claire).",
        },
        {
            id: "stroma",
            x: 60,
            y: 60,
            label: "Stroma",
            text: "La cuisine ! C'est ce liquide gélatineux où l'ATP et le NADPH assemblent le CO2 en sucre (Cycle de Calvin).",
        },
        {
            id: "rubisco",
            x: 45,
            y: 45,
            label: "Rubisco",
            text: "L'enzyme star ⭐. C'est elle qui attrape le CO2 qui flotte pour le transformer en matière organique. Sans elle, pas de vie !",
        },
    ];

    function toggleMarker(marker) {
        if (activeMarker === marker) activeMarker = null;
        else activeMarker = marker;
    }

    // --- CALVIN CYCLE ENGINE ---
    let enzymes = [];
    let co2Particles = [];
    let animationId;

    class Rubisco {
        constructor() {
            this.x = Math.random() * 80 + 10;
            this.y = Math.random() * 80 + 10;
            this.angle = Math.random() * 360;
            this.state = "idle"; // idle, fixing, releasing
            this.timer = 0;
        }

        update(temp) {
            // Move slowly (Brownianish)
            this.x += (Math.random() - 0.5) * 0.5;
            this.y += (Math.random() - 0.5) * 0.5;
            this.angle += 1;

            // State Machine
            if (this.state === "idle") {
                if (Math.random() < 0.01 * (temp / 20)) {
                    this.state = "fixing";
                    this.timer = 60; // Frames to fix
                }
            } else if (this.state === "fixing") {
                this.timer--;
                if (this.timer <= 0) {
                    this.state = "releasing";
                    this.timer = 30;
                }
            } else if (this.state === "releasing") {
                this.timer--;
                if (this.timer <= 0) {
                    this.state = "idle";
                }
            }
        }
    }

    function init() {
        // Spawn 5 Rubiscos
        enzymes = Array.from({ length: 5 }, () => new Rubisco());
        // Spawn Ambient CO2
        co2Particles = Array.from({ length: 20 }, () => ({
            x: Math.random() * 100,
            y: Math.random() * 100,
            speed: 3 + Math.random() * 5,
        }));
    }

    function loop() {
        // Update Enzymes
        enzymes = enzymes.map((e) => {
            e.update(temperature);
            return e;
        });

        requestAnimationFrame(loop);
    }

    onMount(() => {
        init();
        animationId = requestAnimationFrame(loop);
    });

    onDestroy(() => cancelAnimationFrame(animationId));
</script>

<div
    class="flex flex-col h-full font-pixel text-white select-none relative"
    on:click={() => (activeMarker = null)}
    on:keydown={(e) => e.key === "Escape" && (activeMarker = null)}
    role="presentation"
>
    <!-- Header -->
    <div
        class="flex justify-between items-center mb-2 border-b-2 border-green-800 pb-2 bg-green-900/20 p-2"
    >
        <div class="flex items-center gap-2">
            <button
                class="text-xs border border-green-600 px-2 py-1 rounded hover:bg-green-800 transition-colors pointer-events-auto"
                on:click|stopPropagation={() => dispatch("close")}
            >
                ⬅ RETOUR
            </button>
            <h2 class="text-xl text-green-300 drop-shadow-md">
                🦠 Chloroplaste
            </h2>
        </div>
        <div class="text-xs text-green-400 animate-pulse">Niveau 3 : MICRO</div>
    </div>

    <!-- MAIN VIEW: STROMA & GRANA -->
    <div
        class="flex-grow relative bg-[#81C784] border-4 border-[#388E3C] rounded-lg overflow-hidden shadow-inner p-4 cursor-magnify"
    >
        <!-- STROMA BACKGROUND (Fluid) -->
        <div class="absolute inset-0 opacity-20 pointer-events-none"></div>

        <!-- AMBIENT CO2 PARTICLES -->
        {#each co2Particles as p}
            <div
                class="absolute w-1 h-1 bg-black/50 rounded-full animate-float-random"
                style="left: {p.x}%; top: {p.y}%; animation-duration: {p.speed}s"
            ></div>
        {/each}

        <!-- RUBISCO & CALVIN CYCLE ENGINE -->
        {#each enzymes as enzyme}
            <!-- Rubisco Sprite -->
            <div
                class="absolute flex items-center justify-center transition-transform duration-1000 ease-linear"
                style="
                    left: {enzyme.x}%; 
                    top: {enzyme.y}%; 
                    width: 32px; 
                    height: 32px;
                    transform: rotate({enzyme.angle}deg);
                "
            >
                <!-- The Enzyme (Pink Blob) -->
                <div
                    class="absolute w-full h-full bg-pink-500/80 border-2 border-pink-700 rounded-full animate-spin-slow"
                    style="animation-duration: {100 / (temperature || 20)}s"
                >
                    <!-- Speed vs Temp -->
                </div>
                <!-- Label -->
                <span class="relative text-[6px] font-bold text-white z-10"
                    >RuBi</span
                >

                <!-- CO2 Particles being absorbed -->
                {#if enzyme.state === "fixing"}
                    <div
                        class="absolute -top-4 text-[8px] text-black font-bold animate-fade-up"
                    >
                        CO₂
                    </div>
                {/if}
                <!-- Sugar Output -->
                {#if enzyme.state === "releasing"}
                    <div
                        class="absolute -bottom-4 text-[8px] text-yellow-200 font-bold animate-drop"
                    >
                        🍬
                    </div>
                {/if}
            </div>
        {/each}

        <!-- GRANA STACKS (The Interactive Elements) -->
        <!-- Stack 1 -->
        <div
            class="absolute top-1/4 left-1/4 cursor-magnify hover:scale-110 transition-transform group z-20"
            on:click|stopPropagation={() => dispatch("openThylakoid")}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && dispatch("openThylakoid")}
        >
            <div class="flex flex-col items-center">
                {#each Array(5) as _}
                    <div
                        class="w-16 h-4 bg-[#1B5E20] border-2 border-[#2E7D32] rounded-full mb-[-2px] shadow-sm relative overflow-hidden"
                    >
                        <!-- Shimmer effect for light reaction -->
                        {#if isSunny}
                            <div
                                class="absolute inset-0 bg-yellow-400/20 animate-pulse"
                            ></div>
                        {/if}
                    </div>
                {/each}
                <!-- Label -->
                <div
                    class="mt-2 bg-black/70 text-[10px] px-2 rounded text-white opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap"
                >
                    ⚡ Phase Claire (Thylakoïde)
                </div>
            </div>
        </div>

        <!-- Stack 2 -->
        <div
            class="absolute bottom-1/3 right-1/3 cursor-magnify hover:scale-110 transition-transform group z-20"
            on:click|stopPropagation={() => dispatch("openThylakoid")}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && dispatch("openThylakoid")}
        >
            <div class="flex flex-col items-center">
                {#each Array(7) as _}
                    <div
                        class="w-16 h-4 bg-[#1B5E20] border-2 border-[#2E7D32] rounded-full mb-[-2px] shadow-sm relative overflow-hidden"
                    >
                        {#if isSunny}
                            <div
                                class="absolute inset-0 bg-yellow-400/20 animate-pulse delay-75"
                            ></div>
                        {/if}
                    </div>
                {/each}
            </div>
        </div>

        <!-- CONNECTIONS (Lamellae) -->
        <div
            class="absolute top-[35%] left-[30%] w-32 h-2 bg-[#2E7D32] -z-10 transform rotate-12 opacity-80"
        ></div>

        <!-- BIO-MARKERS OVERLAY -->
        <!-- Placed ON TOP of everything -->
        {#each MARKERS as m}
            <button
                class="absolute w-5 h-5 bg-yellow-400 text-black border border-white rounded-full flex items-center justify-center text-[10px] font-bold shadow-lg hover:scale-110 transition-transform z-40 animate-bounce-slight"
                style="left: {m.x}%; top: {m.y}%; animation-delay: {Math.random()}s"
                on:click|stopPropagation={() => toggleMarker(m)}
            >
                ?
            </button>
        {/each}
    </div>

    <!-- MARKER TOOLTIP POPUP -->
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

    <!-- INFO BOX (Legacy) -->
    <!-- Only show if no marker is active -->
    {#if !activeMarker}
        <div
            class="mt-2 bg-[#1B5E20] p-2 border border-[#388E3C] text-xs text-green-100"
        >
            <p>
                <strong>Le Stroma :</strong> C'est ici que le sucre est fabriqué
                (Cycle de Calvin). Les piles vertes sont des
                <strong>Grana</strong>, les centrales solaires de la plante.
            </p>
        </div>
    {/if}
</div>

<style>
    @keyframes floatRandom {
        0% {
            transform: translate(0, 0);
        }
        25% {
            transform: translate(10px, -10px);
        }
        50% {
            transform: translate(-5px, 15px);
        }
        75% {
            transform: translate(-10px, -5px);
        }
        100% {
            transform: translate(0, 0);
        }
    }
    .animate-float-random {
        animation: floatRandom infinite ease-in-out;
    }
    .animate-spin-slow {
        animation: spin 8s linear infinite;
    }
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
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
