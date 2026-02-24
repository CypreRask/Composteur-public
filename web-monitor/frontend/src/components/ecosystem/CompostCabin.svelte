<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let isOpen = false;
    export let temp = 0;
    export let isDangerouslyHot = false;

    // Derived States
    $: isHot = temp > 45;

    // Steam generation based on temp (more particles if hotter)
    // We just render a fixed number for now if hot

    import Probe from "./Probe.svelte";
    import Dial from "./Dial.svelte";
</script>

<div
    class="relative w-56 h-64 group cursor-magnify hover:scale-[1.02] transition-transform font-pixel select-none"
    on:click={() => dispatch("click")}
    on:keydown={(e) => e.key === "Enter" && dispatch("click")}
    role="button"
    tabindex="0"
    aria-label="Compost Bin"
>
    <!-- STEAM EFFECTS (Behind) -->
    {#if isHot}
        <div
            class="absolute -top-10 left-0 w-full h-full pointer-events-none overflow-visible z-0"
        >
            {#each Array(5) as _, i}
                <div
                    class="absolute bg-white/40 w-3 h-3 animate-pixel-rise"
                    class:bg-gray-400={isDangerouslyHot}
                    style="left: {20 +
                        Math.random() *
                            60}%; top: 10px; animation-delay: {Math.random() *
                        2}s;"
                ></div>
            {/each}
        </div>
    {/if}

    <!-- MAIN STRUCTURE -->
    <div class="relative z-10 w-full h-full flex flex-col justify-end">
        <!-- ROOF (Lid) -->
        <div
            class="relative z-30 h-8 bg-[#4E342E] border-4 border-[#3E2723] shadow-md flex items-center justify-center -mb-2 mx-[-10px]"
        >
            <!-- Handle (Square) -->
            <div class="w-16 h-2 bg-[#3E2723]"></div>
            <!-- Texture -->
            <div
                class="absolute top-1 left-2 w-full h-[1px] bg-[#5D4037] opacity-50"
            ></div>
        </div>

        <!-- MAIN BODY (Wood Planks with Gaps) -->
        <div
            class="relative w-full h-[85%] flex flex-col justify-between py-1 shadow-[4px_4px_0_rgba(0,0,0,0.3)] bg-[#281815]"
        >
            <!-- Structure Beams (Corners - Static) -->
            <div
                class="absolute left-0 top-0 w-4 h-[105%] bg-[#3E2723] z-40 border-r-2 border-[#281815] shadow-lg"
            ></div>
            <div
                class="absolute right-0 top-0 w-4 h-[105%] bg-[#3E2723] z-40 border-l-2 border-[#281815] shadow-lg"
            ></div>

            <!-- SENSORS (New Pixel Art Hardware) -->
            <Probe humidity={65} />
            <!-- Mock value for now, fix later with real props -->
            <Dial {temp} />

            <!-- DOOR (The Front Panel - Slides Open) -->
            <div
                class="absolute inset-x-4 top-0 bottom-0 bg-[#281815] z-30 transition-transform duration-500 origin-left flex flex-col justify-between"
                class:scale-x-0={isOpen}
            >
                <!-- Planks -->
                {#each Array(7) as _, i}
                    <div
                        class="w-full h-[12%] bg-[#5D4037] border-y-2 border-[#3E2723] relative shadow-sm mx-[2px] w-[calc(100%-4px)] flex items-center justify-center"
                    >
                        <div
                            class="absolute left-1 top-1 w-1 h-1 bg-[#281815] opacity-50"
                        ></div>
                        <div
                            class="absolute right-1 top-1 w-1 h-1 bg-[#281815] opacity-50"
                        ></div>
                        <div
                            class="absolute top-1/2 left-4 w-8 h-[1px] bg-[#3E2723]/30"
                        ></div>
                    </div>
                {/each}
                <!-- Handle (Square) -->
                <div
                    class="absolute right-2 top-1/2 -translate-y-1/2 w-2 h-12 bg-[#3E2723] shadow-md border border-[#281815]"
                ></div>
            </div>

            <!-- INTERIOR (Visible when Door Opens) -->
            <div
                class="absolute inset-x-4 top-1 bottom-1 bg-[#1A100E] z-10 flex flex-col-reverse overflow-hidden border border-black/50"
            >
                <!-- META: SENSOR BOX (Square) -->
                <div
                    class="absolute top-0 right-1/2 translate-x-1/2 w-10 h-6 bg-blue-700 border-2 border-blue-900 border-t-0 z-50 flex items-center justify-center shadow-lg group/sensor cursor-magnify hover:bg-blue-600 transition-colors"
                    on:click|stopPropagation={() => dispatch("openHardware")}
                    on:keydown={(e) =>
                        e.key === "Enter" && dispatch("openHardware")}
                    role="button"
                    tabindex="0"
                >
                    <!-- LED -->
                    <div
                        class="w-2 h-2 bg-red-500 animate-pulse border border-red-900"
                    ></div>
                </div>

                <!-- 3. FOND: MATURATION (Humus & Clay) -->
                <div
                    class="h-[40%] w-full bg-[#3E2723] relative border-t border-black/20 overflow-hidden cursor-magnify hover:brightness-110 transition-all flex items-end"
                    on:click|stopPropagation={() => dispatch("inspectBiology")}
                    on:keydown={(e) =>
                        e.key === "Enter" && dispatch("inspectBiology")}
                    role="button"
                    tabindex="0"
                >
                    <!-- Texture "Argilo-Humique" (Pixel Noise) -->
                    <div
                        class="absolute inset-0 opacity-20 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPjxyZWN0IHg9IjAiIHk9IjAiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAiLz48cmVjdCB4PSIyIiB5PSIyIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjRkZGIiBvcGFjaXR5PSIwLjMiLz48L3N2Zz4=')]"
                    ></div>

                    <!-- Clusters d'Argile (Bleu sombre) -->
                    {#each Array(5) as _, i}
                        <div
                            class="absolute w-2 h-1 bg-[#1E88E5]/30"
                            style="left: {Math.random() *
                                90}%; top: {Math.random() * 80}%"
                        ></div>
                    {/each}
                </div>

                <!-- 2. COEUR: THERMOPHILE (Activité Intense) -->
                <div
                    class="h-[35%] w-full bg-[#5D4037] relative flex items-center justify-center border-t border-black/20 overflow-hidden cursor-magnify hover:brightness-110 transition-all"
                    on:click|stopPropagation={() => dispatch("inspectBiology")}
                    on:keydown={(e) =>
                        e.key === "Enter" && dispatch("inspectBiology")}
                    role="button"
                    tabindex="0"
                >
                    <!-- Texture "Matière en décomposition" -->
                    <div
                        class="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPjxyZWN0IHg9IjEiIHk9IjMiIHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNmZmYiLz48L3N2Zz4=')]"
                    ></div>

                    {#if isHot}
                        <!-- VISUAL: HEAT CORE (Pulsing Red) -->
                        <div
                            class="absolute inset-0 bg-red-900/40 animate-pulse"
                        ></div>
                        <!-- BACTERIAL CLOUD (Particles) -->
                        <div class="relative w-full h-full">
                            {#each Array(8) as _, i}
                                <div
                                    class="absolute bg-white/60 w-1 h-1 animate-pixel-rise"
                                    style="left: {10 +
                                        Math.random() *
                                            80}%; bottom: {Math.random() *
                                        50}%; animation-delay: {Math.random()}s; animation-duration: {1 +
                                        Math.random()}s"
                                ></div>
                            {/each}
                        </div>
                    {:else}
                        <!-- WORM ACTIVITY (If cold enough) -->
                        <div
                            class="absolute bottom-2 left-10 w-2 h-2 bg-pink-400/80 animate-bounce"
                        ></div>
                    {/if}
                </div>

                <!-- 1. SURFACE: LITIERE (Déchets Frais) -->
                <div
                    class="h-[25%] w-full bg-[#7CB342] relative border-t border-black/20 overflow-hidden cursor-magnify hover:brightness-110 transition-all"
                    on:click|stopPropagation={() => dispatch("inspectWaste")}
                    on:keydown={(e) =>
                        e.key === "Enter" && dispatch("inspectWaste")}
                    role="button"
                    tabindex="0"
                >
                    <!-- Debris Texture -->
                    <div
                        class="absolute inset-0 opacity-30 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4IiBoZWlnaHQ9IjgiPjxwYXRoIGQ9Ik0zIDJ2MWgydjJINXYxaDV2LTJIN3YtMkgzIiBmaWxsPSIjMzUzQTA4Ii8+PC9zdmc+')]"
                    ></div>

                    <!-- Apple Core -->
                    <div
                        class="absolute top-2 left-4 w-3 h-4 bg-red-700 border border-red-900 shadow-sm rotate-12"
                    >
                        <div
                            class="absolute -top-1 left-1 w-1 h-2 bg-green-900"
                        ></div>
                    </div>
                    <!-- Dead Leaf -->
                    <div
                        class="absolute top-4 right-8 w-4 h-2 bg-[#8D6E63] border border-[#5D4037] rotate-[-15deg]"
                    ></div>
                </div>
            </div>
        </div>

        <!-- LEGS -->
        <div class="flex justify-between w-full px-2">
            <div class="w-4 h-4 bg-[#3E2723]"></div>
            <div class="w-4 h-4 bg-[#3E2723]"></div>
        </div>
    </div>

    <!-- INSPECT HINT (Pixel Art Style - Clean) -->
    <div
        class="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-white text-[10px] px-2 py-1 border border-white/50 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-50 pointer-events-none"
    >
        ♻️ Composteur
    </div>
</div>

<style>
    @keyframes pixelRise {
        0% {
            transform: translateY(0) scale(1);
            opacity: 0.8;
        }
        100% {
            transform: translateY(-30px) scale(2);
            opacity: 0;
        }
    }
    .animate-pixel-rise {
        animation: pixelRise 3s steps(8) infinite;
    }

    /* Worm Crawling Animation Removed (Unused) */

    /* Custom Magnifying Glass Cursor */
    .cursor-magnify {
        cursor:
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(1px 1px 0 black);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>')
                12 12,
            zoom-in;
    }
</style>
