<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let isDay = true;

    // Animation suivant le soleil (si jour)
    $: rotation = isDay ? -10 : 0;
</script>

<!-- Tournesol style pixel art détaillé -->
<div
    class="relative cursor-pointer group"
    style="transform: rotate({rotation}deg); transition: transform 2s ease;"
    on:click={() => dispatch("openLifecycle")}
    on:keydown={(e) => e.key === "Enter" && dispatch("openLifecycle")}
    role="button"
    tabindex="0"
    aria-label="Cycle de vie des plantes"
>
    <!-- Tooltip -->
    <div
        class="absolute -top-10 left-1/2 -translate-x-1/2 bg-black/80 text-white text-[10px] px-2 py-1 border border-white/30 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50"
    >
        🌻 Cycle de vie
    </div>

    <!-- TIGE - Texture bois comme le composteur -->
    <div class="relative mx-auto" style="width: 24px; height: 120px;">
        <!-- Tige principale avec texture -->
        <div class="absolute inset-x-0 top-0 bottom-0 bg-[#5D4037] border-x-2 border-[#3E2723]">
            <!-- Veines de la tige -->
            <div class="absolute left-1 top-4 w-1 h-8 bg-[#4E342E]"></div>
            <div class="absolute right-1 top-12 w-1 h-12 bg-[#4E342E]"></div>
            <div class="absolute left-2 top-24 w-1 h-6 bg-[#4E342E]"></div>
        </div>
        
        <!-- Ombre sur la tige -->
        <div class="absolute left-0 top-0 bottom-0 w-1/3 bg-black/10"></div>
    </div>

    <!-- FEUILLES - Style pixel blocks -->
    <!-- Feuille gauche -->
    <div 
        class="absolute top-16 -left-10 w-16 h-12 bg-[#2E7D32] border-2 border-[#1B5E20] shadow-[2px_2px_0_rgba(0,0,0,0.3)]"
        style="clip-path: polygon(100% 0, 100% 100%, 0 50%);"
    >
        <!-- Veines feuille -->
        <div class="absolute top-1/2 left-1/2 w-full h-0.5 bg-[#1B5E20] -translate-y-1/2 rotate-12"></div>
    </div>
    
    <!-- Feuille droite -->
    <div 
        class="absolute top-24 -right-10 w-16 h-12 bg-[#388E3C] border-2 border-[#1B5E20] shadow-[2px_2px_0_rgba(0,0,0,0.3)]"
        style="clip-path: polygon(0 0, 0 100%, 100% 50%);"
    >
        <!-- Veines feuille -->
        <div class="absolute top-1/2 left-0 w-full h-0.5 bg-[#1B5E20] -translate-y-1/2 -rotate-12"></div>
    </div>

    <!-- Petite feuille haute gauche -->
    <div 
        class="absolute top-8 -left-6 w-10 h-8 bg-[#4CAF50] border-2 border-[#2E7D32]"
        style="clip-path: polygon(100% 20%, 100% 80%, 0 50%);"
    ></div>

    <!-- FLEUR - Tournesol détaillé -->
    <div class="absolute -top-4 left-1/2 -translate-x-1/2">
        <!-- Pétales - plusieurs couches -->
        <div class="relative w-20 h-20">
            <!-- Pétales arrière (plus foncés) -->
            {#each [0, 45, 90, 135, 180, 225, 270, 315] as angle}
                <div
                    class="absolute top-1/2 left-1/2 w-4 h-10 bg-[#F57F17] border border-[#E65100] origin-bottom"
                    style="transform: translate(-50%, -100%) rotate({angle}deg);"
                ></div>
            {/each}
            
            <!-- Pétales avant (plus clairs) -->
            {#each [22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5] as angle}
                <div
                    class="absolute top-1/2 left-1/2 w-3 h-8 bg-[#FFEB3B] border border-[#FBC02D] origin-bottom z-10"
                    style="transform: translate(-50%, -100%) rotate({angle}deg) translateY(2px);"
                ></div>
            {/each}
            
            <!-- Centre de la fleur -->
            <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 bg-[#3E2723] border-4 border-[#5D4037] z-20 shadow-inner">
                <!-- Texture centre (graines) -->
                <div class="absolute inset-0 grid grid-cols-3 gap-0.5 p-0.5">
                    {#each Array(9) as _, i}
                        <div class="w-full h-full bg-[#5D4037] rounded-full"></div>
                    {/each}
                </div>
                <!-- Reflet -->
                <div class="absolute top-1 left-1 w-2 h-2 bg-[#6D4C41] rounded-full"></div>
            </div>
        </div>
    </div>

    <!-- Ombre portée au sol -->
    <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-16 h-4 bg-black/20 rounded-full blur-sm"></div>
</div>

<style>
    /* Animations */
    @keyframes gentle-sway {
        0%, 100% { transform: rotate(-2deg); }
        50% { transform: rotate(2deg); }
    }
    
    .animate-sway {
        animation: gentle-sway 4s ease-in-out infinite;
    }
</style>
