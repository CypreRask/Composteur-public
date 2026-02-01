<script>
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
</script>

<!-- Orpin V2 - Plus petit et bien proportionné -->
<div class="relative cursor-pointer group hover:scale-105 transition-transform">
  <div style="width: 60px; height: 100px;">
    
    <!-- TIGE -->
    <div class="absolute bottom-0 left-1/2 -translate-x-1/2" style="width: 16px; height: 50px;">
      <div class="absolute bottom-0 left-0 w-full h-full bg-[#33691E] border-2 border-[#1B5E20]"></div>
      <div class="absolute top-0 left-0 w-full h-3 bg-[#558B2F]"></div>
    </div>

    <!-- FEUILLES - Écailles empilées -->
    <!-- Bas gauche -->
    <div class="absolute bottom-6 left-0 w-10 h-5 bg-[#4CAF50] border-2 border-[#388E3C] shadow-[2px_2px_0_rgba(0,0,0,0.2)]" style="clip-path: polygon(0 0, 100% 100%, 100% 0);"></div>
    
    <!-- Bas droite -->
    <div class="absolute bottom-8 right-0 w-10 h-5 bg-[#43A047] border-2 border-[#2E7D32] shadow-[2px_2px_0_rgba(0,0,0,0.2)]" style="clip-path: polygon(0 0, 0 100%, 100% 0);"></div>
    
    <!-- Milieu gauche -->
    <div class="absolute bottom-14 left-1 w-8 h-4 bg-[#388E3C] border-2 border-[#2E7D32] shadow-[2px_2px_0_rgba(0,0,0,0.2)]" style="clip-path: polygon(0 0, 100% 100%, 100% 0);"></div>
    
    <!-- Milieu droite -->
    <div class="absolute bottom-16 right-1 w-8 h-4 bg-[#2E7D32] border-2 border-[#1B5E20] shadow-[2px_2px_0_rgba(0,0,0,0.2)]" style="clip-path: polygon(0 0, 0 100%, 100% 0);"></div>
    
    <!-- Haut -->
    <div class="absolute bottom-22 left-1/2 -translate-x-1/2 w-6 h-4 bg-[#66BB6A] border-2 border-[#4CAF50] shadow-[2px_2px_0_rgba(0,0,0,0.2)]"></div>

    <!-- FLEUR -->
    <div class="absolute -top-1 left-1/2 -translate-x-1/2" style="width: 20px; height: 20px;">
      <!-- Centre -->
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-4 bg-[#FFC107] border border-[#FF8F00] rounded-full z-10"></div>
      <!-- Pétales -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-2 h-2 bg-[#F48FB1] border border-[#EC407A] rotate-45"></div>
      <div class="absolute bottom-0 left-1/2 -translate-x-1/2 w-2 h-2 bg-[#F48FB1] border border-[#EC407A] rotate-45"></div>
      <div class="absolute top-1/2 left-0 -translate-y-1/2 w-2 h-2 bg-[#F48FB1] border border-[#EC407A] rotate-45"></div>
      <div class="absolute top-1/2 right-0 -translate-y-1/2 w-2 h-2 bg-[#F48FB1] border border-[#EC407A] rotate-45"></div>
    </div>

  </div>

  <!-- Tooltip -->
  <div class="absolute -top-6 left-1/2 -translate-x-1/2 bg-black/80 text-white text-[9px] px-2 py-1 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
    🌵 Orpin (C4)
  </div>
</div>
