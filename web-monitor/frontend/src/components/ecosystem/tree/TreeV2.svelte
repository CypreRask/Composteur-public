<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  export let temp = 20;
  export let soil_hum = 50;
  export let isDay = true;

  $: stressLevel = soil_hum < 30 ? "high" : "low";
  $: activityLevel = temp > 10 && temp < 35 && isDay ? "high" : "low";
</script>

<!-- Arbre V2 - Plus grand que le composteur (224x256) -->
<div class="relative flex flex-col items-center group">
  
  <!-- CANOPY - 280x200px (plus large que composteur) -->
  <div 
    class="relative cursor-pointer transition-transform hover:scale-105 z-30"
    style="width: 280px; height: 200px;"
    on:click={() => dispatch("openPhotosynthesis")}
    on:keydown={(e) => e.key === 'Enter' && dispatch("openPhotosynthesis")}
    role="button"
    tabindex="0"
  >
    <!-- Forme organique simplifiée -->
    <!-- Centre -->
    <div class="absolute top-8 left-16 w-36 h-28 bg-[#2E7D32] border-2 border-[#1B5E20] shadow-[4px_4px_0_rgba(0,0,0,0.3)]"></div>
    <!-- Gauche -->
    <div class="absolute top-16 left-4 w-20 h-20 bg-[#388E3C] border-2 border-[#2E7D32] shadow-[3px_3px_0_rgba(0,0,0,0.3)]"></div>
    <!-- Droite -->
    <div class="absolute top-12 right-4 w-24 h-24 bg-[#388E3C] border-2 border-[#2E7D32] shadow-[3px_3px_0_rgba(0,0,0,0.3)]"></div>
    <!-- Haut -->
    <div class="absolute top-0 left-20 w-20 h-16 bg-[#4CAF50] border-2 border-[#388E3C] shadow-[3px_3px_0_rgba(0,0,0,0.3)]"></div>
    
    <!-- Fruits -->
    <div class="absolute top-12 left-24 w-3 h-3 bg-[#D32F2F] rounded-sm"></div>
    <div class="absolute top-20 right-12 w-3 h-3 bg-[#D32F2F] rounded-sm"></div>
    <div class="absolute bottom-8 left-12 w-2 h-2 bg-[#FF8F00] rounded-sm"></div>
  </div>

  <!-- TRONC - 60x180px (hauteur significative) -->
  <div 
    class="relative cursor-pointer hover:scale-105 transition-transform z-20 -mt-4"
    style="width: 60px; height: 180px;"
    on:click={() => dispatch("openCirculation")}
    on:keydown={(e) => e.key === 'Enter' && dispatch("openCirculation")}
    role="button"
    tabindex="0"
  >
    <!-- Base (plus large) -->
    <div class="absolute bottom-0 left-0 w-16 h-16 bg-[#4E342E] border-2 border-[#3E2723]"></div>
    <!-- Milieu -->
    <div class="absolute bottom-12 left-2 w-12 h-20 bg-[#5D4037] border-2 border-[#4E342E]"></div>
    <!-- Haut -->
    <div class="absolute bottom-28 left-3 w-10 h-24 bg-[#6D4C41] border-2 border-[#5D4037]"></div>
    
    <!-- Texture écorce (lignes) -->
    <div class="absolute bottom-4 left-4 w-0.5 h-12 bg-[#3E2723]/40"></div>
    <div class="absolute bottom-16 left-6 w-0.5 h-10 bg-[#3E2723]/40"></div>
    <div class="absolute bottom-32 left-5 w-0.5 h-8 bg-[#3E2723]/40"></div>
    
    <!-- Branche gauche -->
    <div class="absolute bottom-24 -left-8 w-10 h-4 bg-[#5D4037] border border-[#4E342E] rotate-12"></div>
    <!-- Branche droite -->
    <div class="absolute bottom-20 -right-6 w-8 h-4 bg-[#5D4037] border border-[#4E342E] -rotate-12"></div>
  </div>

  <!-- RACINES - À l'intérieur du sol (partie basse) -->
  <div 
    class="absolute bottom-0 left-1/2 -translate-x-1/2 cursor-pointer z-30"
    style="width: 140px; height: 60px;"
    on:click={() => dispatch("openRoots")}
    on:keydown={(e) => e.key === 'Enter' && dispatch("openRoots")}
    role="button"
    tabindex="0"
  >
    <!-- Racine principale -->
    <div class="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-8 bg-[#5D4037] border-2 border-[#4E342E]"></div>
    <!-- Latérales -->
    <div class="absolute top-4 left-8 w-10 h-4 bg-[#4E342E] border border-[#3E2723] rotate-6"></div>
    <div class="absolute top-6 right-8 w-12 h-4 bg-[#4E342E] border border-[#3E2723] -rotate-6"></div>
    <div class="absolute top-10 left-12 w-8 h-3 bg-[#5D4037] border border-[#4E342E]"></div>
    <div class="absolute top-8 right-12 w-6 h-3 bg-[#5D4037] border border-[#4E342E]"></div>
    
    <!-- MYCELIMUM (lignes blanches) -->
    <div class="absolute top-6 left-0 w-10 h-0.5 bg-[#E0E0E0]/60 border-t border-dashed border-[#BDBDBD]"></div>
    <div class="absolute top-10 right-0 w-8 h-0.5 bg-[#E0E0E0]/60 border-t border-dashed border-[#BDBDBD]"></div>
    <div class="absolute top-2 left-1/2 w-0.5 h-8 bg-[#E0E0E0]/40 border-l border-dashed border-[#BDBDBD]"></div>
  </div>

</div>
