<script>
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    export let fluxState = { carbon: false, nitrogen: false, water: false };
    export let health = 100;
    export let isNight = false;

    function handleClick(zone) {
        dispatch("openWidget", { zone });
    }
</script>

<div
    class="h-full w-24 md:w-32 relative z-[90] pointer-events-auto font-pixel select-none flex flex-col justify-end items-center transition-all duration-1000"
    class:brightness-50={isNight}
>
    <!-- PIXEL ART TREE (CSS Based - Fully Absolute Layout) -->

    <!-- 2. TRUNK (Middle Layer) -->
    <div
        class="absolute bottom-16 top-24 w-8 bg-[#5D4037] border-x-4 border-[#3E2723] z-10 flex flex-col items-center"
        style="left: 50%; transform: translateX(-50%);"
    >
        <!-- Wood Texture -->
        <div class="w-1 h-4 bg-[#3E2723] mt-4 ml-2 opacity-50"></div>
        <div class="w-1 h-3 bg-[#3E2723] mt-8 mr-2 opacity-50"></div>
        <div
            class="absolute top-1/2 left-1 w-2 h-2 bg-[#3E2723] rounded-sm opacity-60"
        ></div>

        <!-- Sap Flow Visualization -->
        {#if fluxState.water || fluxState.carbon}
            <div
                class="absolute inset-0 flex justify-center opacity-70 pointer-events-none overflow-hidden"
            >
                <!-- Xylème (Water Up) -->
                {#if fluxState.water}
                    <div
                        class="w-1 h-full bg-blue-400 animate-flow-up mr-1 opacity-60"
                    ></div>
                {/if}
                <!-- Phloème (Sugar Down) -->
                {#if fluxState.carbon}
                    <div
                        class="w-1 h-full bg-amber-400 animate-flow-down ml-1 opacity-60"
                    ></div>
                {/if}
            </div>
        {/if}
    </div>

    <!-- 1. CANOPY (Leaves - Top Layer) -->
    <div
        class="absolute top-[2%] w-32 h-32 z-20 group-hover/canopy:animate-rustle"
    >
        <!-- Main Bulk -->
        <div
            class="absolute top-4 left-4 right-4 bottom-4 bg-[#2E7D32] shadow-[4px_4px_0_rgba(0,0,0,0.2)]"
        ></div>
        <!-- Highlights -->
        <div class="absolute top-4 left-4 w-16 h-4 bg-[#4CAF50]"></div>
        <div
            class="absolute top-4 right-4 w-4 h-8 bg-[#1B5E20] opacity-20"
        ></div>

        <!-- Details (Pixel blocks) -->
        <div class="absolute -top-2 left-8 w-16 h-6 bg-[#2E7D32]"></div>
        <div class="absolute -bottom-2 right-8 w-12 h-6 bg-[#2E7D32]"></div>
        <div class="absolute top-10 -left-2 w-6 h-12 bg-[#2E7D32]"></div>
        <div class="absolute top-8 -right-2 w-6 h-10 bg-[#2E7D32]"></div>

        <!-- Fruits (if health > 80) -->
        {#if health > 80}
            <div
                class="absolute top-10 right-8 w-3 h-3 bg-red-600 border border-red-900"
            ></div>
            <div
                class="absolute bottom-10 left-8 w-3 h-3 bg-red-600 border border-red-900"
            ></div>
        {/if}
    </div>

    <!-- 3. ROOTS (Bottom Layer) -->
    <div class="absolute bottom-0 w-full h-16 pointer-events-none z-0">
        <!-- Main Root Mass (Connecting to Trunk) -->
        <div
            class="absolute bottom-0 left-1/2 -translate-x-1/2 w-12 h-10 bg-[#5D4037]"
        ></div>
        <!-- Branching Roots -->
        <div
            class="absolute bottom-[-5px] left-[30%] w-4 h-12 bg-[#5D4037] -rotate-12 border-l-4 border-[#3E2723]"
        ></div>
        <div
            class="absolute bottom-[-5px] right-[30%] w-4 h-12 bg-[#5D4037] rotate-12 border-r-4 border-[#3E2723]"
        ></div>
    </div>

    <!-- INTERACTIVE ZONES (Invisible Click Layers) -->

    <!-- Canopy Zone -->
    <div
        class="absolute top-0 left-0 w-full h-[40%] cursor-magnify group/canopy hover:bg-white/5 z-50"
        on:click={() => handleClick("foliage")}
        on:keydown={(e) => e.key === "Enter" && handleClick("foliage")}
        role="button"
        tabindex="0"
    >
        <div
            class="hidden group-hover/canopy:block absolute left-full top-10 ml-2 bg-[#2D3748] border-2 border-white text-white text-[10px] px-2 py-1 shadow-[4px_4px_0_black]"
        >
            🌿 PHOTOSYNTHÈSE
        </div>
    </div>

    <!-- Trunk Zone -->
    <div
        class="absolute top-[40%] left-0 w-full h-[30%] cursor-magnify group/trunk hover:bg-white/5 z-50"
        on:click={() => handleClick("trunk")}
        on:keydown={(e) => e.key === "Enter" && handleClick("trunk")}
        role="button"
        tabindex="0"
    >
        <div
            class="hidden group-hover/trunk:block absolute left-full top-4 ml-2 bg-[#2D3748] border-2 border-white text-white text-[10px] px-2 py-1 shadow-[4px_4px_0_black]"
        >
            🪵 CIRCULATION
        </div>
    </div>

    <!-- Roots Zone -->
    <div
        class="absolute bottom-0 left-0 w-full h-[30%] cursor-magnify group/roots hover:bg-white/5 z-50"
        on:click={() => handleClick("roots")}
        on:keydown={(e) => e.key === "Enter" && handleClick("roots")}
        role="button"
        tabindex="0"
    >
        <div
            class="hidden group-hover/roots:block absolute left-full top-0 ml-2 bg-[#2D3748] border-2 border-white text-white text-[10px] px-2 py-1 shadow-[4px_4px_0_black]"
        >
            🍄 SYMBIOSE
        </div>
    </div>
</div>

<style>
    @keyframes flowUp {
        0% {
            transform: translateY(100%);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100%);
            opacity: 0;
        }
    }
    .animate-flow-up {
        animation: flowUp 2s linear infinite;
    }

    @keyframes flowDown {
        0% {
            transform: translateY(-100%);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(100%);
            opacity: 0;
        }
    }
    .animate-flow-down {
        animation: flowDown 3s linear infinite;
    }
</style>
