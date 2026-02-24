<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    // svelte-ignore unused-export-let
    export let isDay = true;
</script>

<!-- Maïs (Corn) - C4 Plant - BLOCKY Pixel Art Style like Tree/Compost -->
<div
    class="relative w-32 h-48 group"
    role="group"
    aria-label="Maïs C4"
>
    <!-- Tooltip -->
    <div
        class="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-white text-[10px] px-2 py-1 border border-white/50 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50"
    >
        🌽 Maïs (C4) — Cliquez une zone
    </div>

    <!-- FOLIAGE ZONE (Top - Clickable) -->
    <div
        class="absolute top-0 left-1/2 -translate-x-1/2 w-28 h-32 bg-[#4CAF50] border-4 border-[#2E7D32] shadow-[4px_4px_0_rgba(0,0,0,0.3)] cursor-magnify hover:brightness-110 hover:scale-[1.02] transition-all z-10"
        on:click|stopPropagation={() => dispatch("openC4")}
        on:keydown={(e) => e.key === "Enter" && dispatch("openC4")}
        role="button"
        tabindex="0"
        aria-label="Feuillage Maïs - Photosynthèse C4"
    >
        <!-- Leaf texture blocks -->
        <div
            class="absolute top-2 left-2 w-6 h-8 bg-[#66BB6A] opacity-60"
        ></div>
        <div
            class="absolute top-4 right-3 w-8 h-6 bg-[#388E3C] opacity-40"
        ></div>
        <div
            class="absolute bottom-4 left-4 w-10 h-5 bg-[#388E3C] opacity-40"
        ></div>
        <div
            class="absolute bottom-2 right-2 w-5 h-7 bg-[#66BB6A] opacity-50"
        ></div>

        <!-- CORN COB (Yellow block on side) -->
        <div
            class="absolute top-1/4 right-2 w-5 h-12 bg-[#FFEB3B] border-2 border-[#FBC02D] shadow-sm pointer-events-none"
        >
            <!-- Kernel pattern -->
            <div class="w-full h-full grid grid-cols-2 gap-px p-0.5">
                <div class="bg-[#FFD54F]"></div>
                <div class="bg-[#FFC107]"></div>
                <div class="bg-[#FFC107]"></div>
                <div class="bg-[#FFD54F]"></div>
                <div class="bg-[#FFD54F]"></div>
                <div class="bg-[#FFC107]"></div>
            </div>
        </div>

        <!-- Second cob (smaller, left) -->
        <div
            class="absolute bottom-1/3 left-2 w-4 h-8 bg-[#FFEB3B] border-2 border-[#FBC02D] pointer-events-none"
        ></div>

        <!-- Zone label on hover -->
        <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity bg-black/30 pointer-events-none">
            <span class="text-[8px] text-white font-bold bg-black/60 px-1 rounded">FEUILLAGE</span>
        </div>
    </div>

    <!-- TASSEL (Top decoration) -->
    <div
        class="absolute -top-3 left-1/2 -translate-x-1/2 w-8 h-4 bg-[#8D6E63] border-2 border-[#5D4037] pointer-events-none"
    ></div>

    <!-- STEM ZONE (Bottom - Clickable for Circulation C4) -->
    <div
        class="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-20 bg-[#558B2F] border-4 border-[#33691E] shadow-[2px_2px_0_rgba(0,0,0,0.2)] cursor-magnify hover:brightness-110 hover:scale-[1.02] transition-all z-0"
        on:click|stopPropagation={() => dispatch("openCirculationC4")}
        on:keydown={(e) => e.key === "Enter" && dispatch("openCirculationC4")}
        role="button"
        tabindex="0"
        aria-label="Tige Maïs - Circulation C4 (Kranz)"
    >
        <!-- Zone label on hover -->
        <div class="absolute inset-0 flex items-end justify-center pb-1 opacity-0 hover:opacity-100 transition-opacity bg-black/30 pointer-events-none">
            <span class="text-[7px] text-white font-bold bg-black/60 px-1 rounded">TIGE</span>
        </div>
    </div>
</div>
