<script>
    import Canopy from "./Canopy.svelte";
    import Trunk from "./Trunk.svelte";
    import Roots from "./Roots.svelte";

    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let weather = null;
    export let temp = 20;
    export let soil_hum = 50;
    export let isDay = true;

    // Computed internal states for visual feedback
    $: stressLevel = soil_hum < 30 ? "high" : "low"; // Hydric stress
    $: activityLevel = temp > 10 && temp < 35 && isDay ? "high" : "low";
</script>

<div class="relative flex flex-col items-center z-20 pointer-events-none group">
    <!-- Structure Verticale -->

    <!-- 1. CANOPEE (Feuilles) -->
    <div class="relative z-30 mb-[-10px] pointer-events-auto">
        <Canopy
            {weather}
            {isDay}
            {stressLevel}
            on:openPhotosynthesis={() => dispatch("openPhotosynthesis")}
        />
    </div>

    <!-- 2. TRONC (Transport) -->
    <div class="relative z-20 pointer-events-auto">
        <Trunk
            {activityLevel}
            {stressLevel}
            on:openCirculation={() => dispatch("openCirculation")}
        />
    </div>

    <!-- 3. RACINES (Sol) -->
    <!-- Positioned absolutely below the trunk to align perfectly -->
    <div
        class="absolute top-[92%] left-1/2 -translate-x-1/2 z-30 pointer-events-auto"
    >
        <Roots
            {soil_hum}
            on:openRoots={() => dispatch("openRoots")}
            on:openSymbiosisC4={() => dispatch("openSymbiosisC4")}
            on:openCAM={() => dispatch("openCAM")}
        />
    </div>
</div>
