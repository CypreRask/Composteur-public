<script>
    export let weather = null;
    export let isDay = true;
    export const stressLevel = "low"; // Export pour référence externe, non utilisé dans ce composant

    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    // Visual State
    $: isSunHitting = isDay && (weather?.clouds?.all || 0) < 50;
</script>

<!-- The Foliage Click Area -->
<!-- Centered relative to the parent flex col -->
<div
    class="relative w-[300px] h-[250px] -mb-16 z-50 flex items-center justify-center transition-transform hover:scale-105 cursor-pointer origin-center"
    on:click={() => dispatch("openPhotosynthesis")}
    on:keydown={(e) => e.key === "Enter" && dispatch("openPhotosynthesis")}
    role="button"
    tabindex="0"
    aria-label="Voir la photosynthèse"
>
    <!-- MAIN FOLIAGE BLOCK (Big & Green) -->
    <div
        class="w-full h-full bg-[#2E7D32] shadow-[8px_8px_0_rgba(0,0,0,0.4)] relative border-4 border-[#1B5E20]"
    >
        <!-- Texture: Leaves (Pixel Noise) -->
        <div
            class="absolute top-4 left-4 w-8 h-8 bg-[#4CAF50] opacity-50"
        ></div>
        <div
            class="absolute top-12 left-20 w-12 h-12 bg-[#1B5E20] opacity-30"
        ></div>
        <div
            class="absolute bottom-8 right-8 w-16 h-16 bg-[#1B5E20] opacity-30"
        ></div>
        <div
            class="absolute top-8 right-12 w-6 h-6 bg-[#66BB6A] opacity-60"
        ></div>

        <!-- Fruits (Apples) -->
        <div
            class="absolute top-1/4 right-1/4 w-5 h-5 bg-[#D32F2F] shadow-sm animate-bounce border border-black"
        ></div>
        <div
            class="absolute bottom-1/3 left-1/4 w-5 h-5 bg-[#D32F2F] shadow-sm animate-bounce border border-black"
            style="animation-delay: 0.7s"
        ></div>

        <!-- HIGHLIGHT (Sun) -->
        {#if isSunHitting}
            <div
                class="absolute top-2 right-2 w-24 h-24 bg-yellow-400/20 rounded-full blur-xl animate-pulse"
            ></div>
        {/if}
    </div>
    <!-- Label on Hover (Pixel Art) -->
    <div
        class="absolute -top-6 left-1/2 -translate-x-1/2 bg-black text-white text-[10px] px-2 py-1 border border-white/50 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none"
    >
        🌳 Pommier (C3)
    </div>
</div>
