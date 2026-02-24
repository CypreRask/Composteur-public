<script>
    export let activityLevel = "low";
    export let stressLevel = "low";

    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
</script>

<div
    on:click={() => dispatch("openCirculation")}
    on:keydown={(e) => e.key === "Enter" && dispatch("openCirculation")}
    role="button"
    tabindex="0"
    class="relative w-24 h-48 flex flex-col items-center justify-end cursor-magnify group transition-transform hover:scale-105 origin-center"
>
    <!-- 1. BRANCHES (The Y Shape) - Visible under Canopy -->
    <div class="relative w-full h-16 z-10 -mb-2">
        <!-- Left Branch -->
        <div
            class="absolute bottom-0 left-2 w-4 h-16 bg-[#5D4037] border-l-4 border-[#3E2723] -skew-x-[15deg] origin-bottom"
        ></div>
        <!-- Right Branch -->
        <div
            class="absolute bottom-0 right-2 w-4 h-16 bg-[#5D4037] border-r-4 border-[#3E2723] skew-x-[15deg] origin-bottom"
        ></div>
        <!-- Center Filler -->
        <div
            class="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-8 bg-[#5D4037]"
        ></div>
    </div>

    <!-- 2. MAIN TRUNK (The Column) -->
    <div
        class="w-16 h-32 bg-[#5D4037] border-x-4 border-[#3E2723] relative shadow-[4px_0_0_rgba(0,0,0,0.3)] z-20"
    >
        <!-- Texture: Ecorce -->
        <div
            class="absolute top-4 left-2 w-2 h-8 bg-[#3E2723] opacity-30"
        ></div>
        <div
            class="absolute bottom-10 right-3 w-3 h-12 bg-[#3E2723] opacity-30"
        ></div>

        <!-- Simulation: Sève (Particles) -->
        {#if activityLevel === "high" && stressLevel === "low"}
            <!-- Rising Water (Xylem) - Blue -->
            <div
                class="absolute left-2 bottom-0 w-1 h-3 bg-[#4FC3F7] animate-flow-up opacity-80"
            ></div>
            <div
                class="absolute left-6 bottom-0 w-1 h-3 bg-[#4FC3F7] animate-flow-up opacity-80"
                style="animation-delay: 0.5s"
            ></div>

            <!-- Descending Sugar (Phloem) - Pink -->
            <div
                class="absolute right-4 top-0 w-1 h-3 bg-[#FFB74D] animate-flow-down opacity-80"
            ></div>
        {/if}
    </div>

    <!-- 3. ROOT FLARE (The Base) -->
    <!-- Widening steps for pixel look -->
    <div class="w-20 h-4 bg-[#5D4037] border-x-4 border-[#3E2723] z-20"></div>
    <div
        class="w-24 h-4 bg-[#5D4037] border-x-4 border-[#3E2723] relative z-20 shadow-[4px_4px_0_rgba(0,0,0,0.3)]"
    >
        <!-- Roots entering ground details -->
        <div
            class="absolute bottom-0 left-2 w-2 h-4 bg-[#3E2723] opacity-50"
        ></div>
        <div
            class="absolute bottom-0 right-4 w-2 h-4 bg-[#3E2723] opacity-50"
        ></div>
    </div>

    <!-- Tooltip -->
    <!-- Tooltip REMOVED -->
</div>

<style>
    @keyframes flowUp {
        0% {
            transform: translateY(100%);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-300%);
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
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(300%);
            opacity: 0;
        }
    }
    .animate-flow-down {
        animation: flowDown 3s linear infinite;
    }
</style>
