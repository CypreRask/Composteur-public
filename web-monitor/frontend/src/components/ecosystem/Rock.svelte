<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
</script>

<!-- Rocher avec mousse style pixel art -->
<div
    class="relative cursor-magnify group"
    on:click={() => dispatch("openGeology")}
    on:keydown={(e) => e.key === "Enter" && dispatch("openGeology")}
    role="button"
    tabindex="0"
    aria-label="Géologie et minéraux"
>
    <!-- Tooltip -->
    <div
        class="absolute -top-10 left-1/2 -translate-x-1/2 bg-black/80 text-white text-[10px] px-2 py-1 border border-white/30 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50"
    >
        🪨 Minéraux du sol
    </div>

    <!-- Rocher principal -->
    <div class="relative" style="width: 80px; height: 60px;">
        <!-- Forme principale du rocher - style bloc pixel -->
        <div
            class="absolute bottom-0 left-0 w-full h-12 bg-[#616161] border-2 border-[#424242]"
        >
            <!-- Texture pierre (cracks et variations) -->
            <div class="absolute top-2 left-2 w-8 h-1 bg-[#424242]"></div>
            <div class="absolute top-4 left-4 w-6 h-1 bg-[#757575]"></div>
            <div class="absolute bottom-3 right-3 w-4 h-1 bg-[#424242]"></div>
            <div class="absolute top-6 left-8 w-3 h-3 bg-[#757575]"></div>

            <!-- Ombre sur la pierre -->
            <div class="absolute right-0 top-0 bottom-0 w-3 bg-black/20"></div>
            <div class="absolute left-0 bottom-0 w-full h-2 bg-black/30"></div>
        </div>

        <!-- Partie haute du rocher (plus petite) -->
        <div
            class="absolute top-0 left-4 w-12 h-8 bg-[#757575] border-2 border-[#616161]"
        >
            <div class="absolute top-1 left-1 w-3 h-1 bg-[#9E9E9E]"></div>
            <div class="absolute right-0 top-0 bottom-0 w-2 bg-black/15"></div>
        </div>

        <!-- Petit caillou à côté -->
        <div
            class="absolute bottom-0 -right-2 w-6 h-5 bg-[#616161] border border-[#424242]"
        >
            <div class="absolute right-0 top-0 bottom-0 w-1 bg-black/20"></div>
        </div>

        <!-- MOUSSE sur le dessus -->
        <div class="absolute -top-2 left-2 w-16 h-6">
            <!-- Touffes de mousse -->
            <div
                class="absolute bottom-0 left-0 w-4 h-4 bg-[#2E7D32] border border-[#1B5E20]"
            ></div>
            <div
                class="absolute bottom-0 left-3 w-5 h-5 bg-[#388E3C] border border-[#2E7D32]"
            ></div>
            <div
                class="absolute bottom-0 left-6 w-4 h-4 bg-[#2E7D32] border border-[#1B5E20]"
            ></div>
            <div
                class="absolute bottom-0 left-9 w-5 h-3 bg-[#4CAF50] border border-[#388E3C]"
            ></div>

            <!-- Petites touffes -->
            <div class="absolute bottom-1 left-1 w-2 h-2 bg-[#66BB6A]"></div>
            <div class="absolute bottom-1 left-8 w-2 h-2 bg-[#66BB6A]"></div>
            <div class="absolute bottom-2 left-5 w-2 h-2 bg-[#81C784]"></div>
        </div>

        <!-- Mousse sur le côté -->
        <div class="absolute top-4 -left-1 w-3 h-8">
            <div
                class="absolute top-0 w-3 h-3 bg-[#2E7D32] border border-[#1B5E20]"
            ></div>
            <div
                class="absolute top-2 w-2 h-4 bg-[#388E3C] border border-[#2E7D32]"
            ></div>
        </div>

        <!-- Lichen clair -->
        <div
            class="absolute top-6 right-4 w-3 h-2 bg-[#AED581] opacity-80"
        ></div>
        <div
            class="absolute bottom-4 left-6 w-2 h-2 bg-[#C5E1A5] opacity-60"
        ></div>
    </div>

    <!-- Ombre portée -->
    <div
        class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-20 h-3 bg-black/20 rounded-full blur-sm"
    ></div>
</div>
