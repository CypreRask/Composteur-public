<script>
    export let data = null;
    export let weather = null;
    export let fluxState = null;

    // Safe Data
    $: safeData = data || {
        temp_scd: 0,
        mq137: 0,
        soil_ph: 7,
        soil_n: 0,
        soil_p: 0,
        soil_k: 0,
        soil_hum: 0,
        soil_temp: 0,
    };

    // Weather Logic
    $: isRaining =
        weather?.weather?.[0]?.main === "Rain" ||
        weather?.weather?.[0]?.main === "Drizzle" ||
        weather?.weather?.[0]?.main === "Thunderstorm";
    $: isCloudy = weather?.weather?.[0]?.main === "Clouds" || isRaining;

    $: isHot = safeData.temp_scd > 45;
    $: isDangerouslyHot = safeData.temp_scd > 70; // Risk of fire/ash
    $: isCold = safeData.temp_scd < 5;
    $: isScorching = safeData.temp_scd > 30; // Atmospheric Heat
    $: isSmelly = safeData.mq137 > 100;

    // Day/Night Logic for Photosynthesis
    $: isNight = weather?.sys
        ? Date.now() / 1000 < weather.sys.sunrise ||
          Date.now() / 1000 > weather.sys.sunset
        : false;

    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    // Interaction
    let isOpen = false;
    function toggleBin() {
        isOpen = !isOpen;
    }

    import CompostCabin from "./components/ecosystem/CompostCabin.svelte"; // NEW
    import SmartTree from "./components/ecosystem/tree/SmartTree.svelte"; // Phase 6

    // --- PROCEDURAL GENERATION ---
    const leafPiles = Array.from({ length: 5 }).map(() => ({
        x: Math.random() * 80 + 5,
        scale: 0.8 + Math.random() * 0.4,
        delay: Math.random() * 5,
        type: Math.random() > 0.5 ? "brown" : "orange",
    }));
</script>

<div class="h-64 w-full relative flex items-end justify-center font-pixel">
    <!-- 3. INTERACTIVE CONTAINER (Responsive) -->
    <!-- Max-width increased to 6xl for large screens, centered -->
    <div
        class="relative z-30 w-full max-w-6xl flex items-end justify-center gap-8 md:gap-16 px-4 md:px-10 h-full pointer-events-none"
    >
        <!-- C4 PLANT (Mixotroph) - Left of Tree -->
        <div
            class="relative pointer-events-auto z-10 origin-bottom scale-75 self-end mr-[-40px]"
        >
            <!-- Pixel Art Orchid/Orpin -->
            <div
                class="w-16 h-24 relative group cursor-help transition-transform hover:scale-110"
                role="button"
                tabindex="0"
                aria-label="Plante C4"
            >
                <!-- Tooltip (Pixel Art) -->
                <div
                    class="absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-white text-[10px] px-2 py-1 border border-white/50 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50"
                >
                    🌵 Orpin (C4)
                </div>
                <!-- Stem (Clickable for Circulation) -->
                <div
                    class="absolute bottom-0 left-1/2 w-4 h-16 -translate-x-1/2 cursor-crosshair z-20"
                    on:click|stopPropagation={() =>
                        dispatch("openCirculationC4")}
                    on:keydown|stopPropagation={(e) =>
                        e.key === "Enter" && dispatch("openCirculationC4")}
                    role="button"
                    tabindex="0"
                ></div>
                <!-- Visual Stem -->
                <div
                    class="absolute bottom-0 left-1/2 w-2 h-16 bg-lime-700 -translate-x-1/2 pointer-events-none"
                ></div>

                <!-- Leaves (Pixelated Steps) -->
                <div
                    class="absolute bottom-4 left-0 w-8 h-4 bg-lime-500 rounded-sm skew-y-12 border-b-2 border-lime-800"
                ></div>
                <div
                    class="absolute bottom-8 right-0 w-8 h-4 bg-lime-500 rounded-sm -skew-y-12 border-b-2 border-lime-800"
                ></div>
                <!-- Flower -->
                <div
                    class="absolute top-2 left-1/2 -translate-x-1/2 w-6 h-6 bg-pink-400 rotate-45 border-2 border-pink-600"
                ></div>
            </div>
        </div>

        <!-- SMART TREE (New Phase 6) -->
        <div class="relative pointer-events-auto z-30">
            <SmartTree
                {weather}
                temp={safeData.temp_scd}
                soil_hum={safeData.soil_hum}
                isDay={!isNight}
                on:openPhotosynthesis={() => dispatch("openPhotosynthesis")}
                on:openCirculation={() => dispatch("openCirculation")}
                on:openRoots={() => dispatch("openRoots")}
                on:openSymbiosisC4={() => dispatch("openSymbiosisC4")}
            />
        </div>

        <!-- COMPOST BIN (Updated Component) -->
        <div class="pointer-events-auto relative z-20">
            <CompostCabin
                {isOpen}
                temp={safeData.temp_scd}
                {isDangerouslyHot}
                on:click={toggleBin}
                on:openHardware={() => dispatch("openHardware")}
                on:inspectWaste={() => dispatch("inspectWaste")}
                on:inspectBiology={() => dispatch("inspectBiology")}
            />
        </div>
    </div>

    <!-- 4. GRASS & SOIL LINE (Matching App Theme) -->
    <div
        class="absolute bottom-0 w-full h-4 bg-terra-grass border-t-4 border-[#388E3C] z-20"
    >
        <!-- Grass Blades (CSS Repeat) -->
        <div
            class="w-full h-2 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4IiBoZWlnaHQ9IjgiPjxwYXRoIGQ9Ik0wIDhWNkw0IDhoNHYtMmw0IDJ6IiBmaWxsPSIjNENENDM3Ii8+PC9zdmc+')] opacity-80 absolute -top-2"
        ></div>
    </div>
</div>

<style>
    @keyframes float {
        0%,
        100% {
            transform: translateX(0);
        }
        50% {
            transform: translateX(20px);
        }
    }
    /* Keeping float as it might be used by clouds in future, but removing others */
</style>
