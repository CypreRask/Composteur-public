<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
</script>

<!-- Champignon Amanite style pixel art détaillé -->
<div
    class="relative cursor-pointer group"
    on:click={() => dispatch("openMycelium")}
    on:keydown={(e) => e.key === "Enter" && dispatch("openMycelium")}
    role="button"
    tabindex="0"
    aria-label="Réseau mycélium"
>
    <!-- Tooltip -->
    <div
        class="absolute -top-10 left-1/2 -translate-x-1/2 bg-black/80 text-white text-[10px] px-2 py-1 border border-white/30 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50"
    >
        🍄 Mycélium
    </div>

    <div class="relative" style="width: 60px; height: 80px;">
        <!-- Pied du champignon -->
        <div class="absolute bottom-0 left-1/2 -translate-x-1/2" style="width: 20px; height: 40px;">
            <!-- Pied épais -->
            <div class="absolute bottom-0 left-0 right-0 h-10 bg-[#FFEBEE] border-x-2 border-[#FFCDD2]">
                <!-- Texture pied (stries) -->
                <div class="absolute top-2 left-0 right-0 h-0.5 bg-[#FFCDD2]"></div>
                <div class="absolute top-4 left-0 right-0 h-0.5 bg-[#FFCDD2]"></div>
                <div class="absolute top-6 left-0 right-0 h-0.5 bg-[#FFCDD2]"></div>
                
                <!-- Ombre sur le pied -->
                <div class="absolute right-0 top-0 bottom-0 w-1/3 bg-[#FFCDD2]/50"></div>
            </div>
            
            <!-- Base renflée (volva) -->
            <div class="absolute -bottom-1 -left-2 right-0 h-4 w-12 bg-[#FFEBEE] border-2 border-[#FFCDD2] rounded-b-sm">
                <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-2 bg-[#EF9A9A]/30"></div>
            </div>
        </div>

        <!-- Chapeau -->
        <div class="absolute top-0 left-1/2 -translate-x-1/2" style="width: 56px; height: 36px;">
            <!-- Dôme rouge -->
            <div 
                class="w-full h-full bg-[#D32F2F] border-2 border-[#B71C1C] relative overflow-hidden"
                style="border-radius: 50% 50% 20% 20% / 60% 60% 40% 40%;"
            >
                <!-- Dégradé haut (plus clair) -->
                <div class="absolute top-0 left-0 right-0 h-1/2 bg-gradient-to-b from-[#E53935] to-transparent"></div>
                
                <!-- Taches blanches (characteristique Amanite) -->
                <div class="absolute top-2 left-3 w-4 h-4 bg-[#FFEBEE] rounded-sm transform rotate-12"></div>
                <div class="absolute top-4 right-4 w-3 h-3 bg-[#FFEBEE] rounded-sm transform -rotate-6"></div>
                <div class="absolute top-1 right-1/2 w-2 h-2 bg-[#FFEBEE] rounded-sm"></div>
                <div class="absolute bottom-3 left-6 w-3 h-3 bg-[#FFEBEE] rounded-sm transform rotate-45"></div>
                <div class="absolute top-6 left-1/2 w-2 h-2 bg-[#FFEBEE] rounded-sm"></div>
                
                <!-- Ombre sous le chapeau -->
                <div class="absolute bottom-0 left-0 right-0 h-3 bg-[#B71C1C]"></div>
            </div>
            
            <!-- Lamelles (sous le chapeau) -->
            <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-12 h-3 bg-[#FFEBEE] border-x border-[#FFCDD2] flex justify-center gap-0.5 overflow-hidden">
                {#each Array(8) as _}
                    <div class="w-0.5 h-full bg-[#FFCDD2]"></div>
                {/each}
            </div>
        </div>

        <!-- Anneau sur le pied -->
        <div class="absolute top-10 left-1/2 -translate-x-1/2 w-12 h-3 bg-[#FFEBEE] border border-[#FFCDD2] -skew-x-12">
            <div class="absolute right-0 top-0 bottom-0 w-2 bg-[#FFCDD2]/50"></div>
        </div>
    </div>

    <!-- Petits champignons à côté -->
    <div class="absolute bottom-0 -left-3 w-4 h-6">
        <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-4 bg-[#FFEBEE] border border-[#FFCDD2]"></div>
        <div class="absolute top-0 left-0 w-4 h-3 bg-[#E53935] border border-[#B71C1C] rounded-t-full"></div>
    </div>

    <!-- Ombre portée -->
    <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-16 h-3 bg-black/20 rounded-full blur-sm"></div>
</div>
