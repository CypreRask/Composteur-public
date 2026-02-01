<script>
  export let data = null;
  // svelte-ignore unused-export-let
  export let weather = null; // Export pour référence externe
  export let isDay = true;

  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();

  import CompostCabin from "./components/ecosystem/CompostCabin.svelte";
  import TreeV2 from "./components/ecosystem/tree/TreeV2.svelte";
  import OrpinV2 from "./components/ecosystem/OrpinV2.svelte";
</script>

<!-- Surface V2 - Alignement bottom strict -->
<div class="w-full h-full flex items-end justify-center gap-4 px-4 pb-0">
  <!-- Orpin à gauche - plus petit -->
  <div class="flex-shrink-0" style="margin-bottom: 8px;">
    <OrpinV2 />
  </div>

  <!-- Arbre V2 au centre - plus grand que composteur -->
  <div class="flex-shrink-0" style="margin-bottom: 0;">
    <TreeV2
      temp={data?.temp_scd || 20}
      soil_hum={data?.soil_hum || 50}
      {isDay}
      on:openPhotosynthesis={() => dispatch("openPhotosynthesis")}
      on:openCirculation={() => dispatch("openCirculation")}
      on:openRoots={() => dispatch("openRoots")}
    />
  </div>

  <!-- Composteur à droite - référence (224x256px) -->
  <div class="flex-shrink-0" style="margin-bottom: 8px;">
    <CompostCabin
      temp={data?.temp_scd || 20}
      isDangerouslyHot={(data?.temp_scd || 0) > 70}
      on:click={() => dispatch("inspectWaste")}
      on:openHardware={() => dispatch("openHardware")}
      on:inspectWaste={() => dispatch("inspectWaste")}
      on:inspectBiology={() => dispatch("inspectBiology")}
    />
  </div>
</div>
