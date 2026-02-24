<script>
    export let data = null;
    export let weather = null;
    export let fluxState = { carbon: false, nitrogen: false, water: false };

    $: isRaining =
        weather?.weather &&
        weather.weather.length > 0 &&
        (weather.weather[0].main === "Rain" ||
            weather.weather[0].main === "Drizzle" ||
            weather.weather[0].main === "Thunderstorm");

    $: safeData = data || { soil_hum: 0, soil_temp: 20 };

    // --- CONDITIONS DE VIE ---
    $: soilState =
        safeData.soil_hum > 60
            ? "moist"
            : safeData.soil_hum < 20
              ? "dry"
              : "normal";

    // Logique Vie :
    // - Si Temp = 0 (souvent capteur déconnecté/init), on considère "Normal" pour pas bloquer l'affichage.
    // - Gelé seulement si < 2°C ET non nul (ou proche 0 mais avec données valides, dur à dire sans flag status, assumons 0=bug)
    $: isFrozen = safeData.soil_temp < 2 && safeData.soil_temp !== 0;
    $: isActive = safeData.soil_temp > 10;
    $: isOverheated = safeData.soil_temp > 30; // Vers fuient

    // Conditions Critiques (Mode Labo / God Mode)
    $: isAnaerobic = safeData.soil_hum > 80; // Manque d'oxygène -> Méthane
    $: isRotting = safeData.soil_hum > 90; // Racines pourrissent

    $: lifeDensity =
        isActive && !isOverheated && safeData.soil_hum > 30
            ? "high"
            : isFrozen || isOverheated
              ? "frozen"
              : "low";

    $: soilColor =
        soilState === "moist"
            ? "bg-[#3E2723]"
            : soilState === "dry"
              ? "bg-[#795548]"
              : "bg-[#5D4037]";

    // --- GENERATION PROCEDURALE (Decor) ---
    // 1. Minéraux, Fossiles & Complexe Argilo-Humique (CAH)
    const items = Array.from({ length: 25 }).map(() => ({
        left: Math.random() * 95,
        top: Math.random() * 90 + 5,
        // Probabilités : 50% Caillou, 20% Fossile, 10% Or, 5% Diamant, 15% CAH (Nouveau !)
        type: Math.random(),
        scale: Math.random() * 0.5 + 0.5,
    }));

    // Helper pour le type
    function getItemType(val) {
        if (val < 0.5) return "rock";
        if (val < 0.7) return "fossil";
        if (val < 0.85) return "cah"; // Complexe Argilo Humique
        if (val < 0.95) return "gold";
        return "gem";
    }

    // --- GENERATION FAUNE (Dynamique) ---
    // Classification Scientifique :
    // - Endogés (Horizontaux) : Vivent dans le sol, galeries horizontales.
    // - Anéciques (Verticaux) : Font des allers-retours surface-profondeur.

    // REACTIVITÉ CORRIGÉE : wormCount doit dépendre de lifeDensity dynamiquement
    $: wormCount = lifeDensity === "high" ? 8 : lifeDensity === "low" ? 3 : 0;

    // On génère le pool maximum (8) une fois pour éviter reset animation
    const wormsPool = Array.from({ length: 8 }).map((_, i) => ({
        id: i,
        type: Math.random() > 0.5 ? "endoge" : "anecique",
        top: Math.random() * 80 + 10,
        left: Math.random() * 90 + 5,
        // RALENTISSEMENT : 60s à 120s pour traverser l'écran. C'est zen.
        duration: Math.random() * 60 + 60,
        delay: Math.random() * -100,
        direction: Math.random() > 0.5 ? 1 : -1,
        color: Math.random() > 0.8 ? "#F06292" : "#F48FB1",
    }));

    // Filtre dynamique
    $: activeWorms = wormsPool.slice(0, wormCount);

    // 4. COLLEMBOLES (Les sauteurs)
    $: collemboleCount = isFrozen ? 0 : soilState === "moist" ? 20 : 8;
    // Pool statique pour eviter re-render
    const collembolePool = Array.from({ length: 20 }).map(() => ({
        left: Math.random() * 90 + 5,
        top: Math.random() * 90 + 5,
        delay: Math.random() * 5,
        scale: 0.5 + Math.random() * 0.5,
    }));

    // 3. LE ROI DU SOUS-SOL : RONGEURS (Mulot / Campagnol)
    let showRodent = false;
    let rodentType = "mulot"; // 'mulot' (oreilles) ou 'campagnol' (rond)
    setInterval(() => {
        if (Math.random() > 0.6) {
            // 40% chance every 12s
            showRodent = true;
            rodentType = Math.random() > 0.5 ? "mulot" : "campagnol";
            setTimeout(() => (showRodent = false), 5000); // Reste 5s
        }
    }, 12000);

    // Infos Scientifiques (au survol)
    let selectedInfo = null;
    function showInfo(type, x, y) {
        selectedInfo = { type, x, y };
    }
    function hideInfo() {
        selectedInfo = null;
    }

    // --- ETAT INTERACTIF (MODALE) ---
    let selectedDetail = null; // 'cah', 'anecique', 'endoge'
    let discoveredItems = new Set(); // Track unique discoveries per session

    function openDetail(type) {
        selectedDetail = type;

        // Gamification: Award XP for first discovery or rare clicks
        let xpGain = 0;
        let label = "";

        if (type === "gold" || type === "gem") {
            xpGain = 50;
            label = "Trésor !";
        } else if (type === "fossil") {
            xpGain = 20;
            label = "Paléontologue";
        } else if (!discoveredItems.has(type)) {
            // First time discovering a species/element
            xpGain = 100;
            label = "Découverte !";
            discoveredItems.add(type);
        } else {
            // Small XP for re-examining
            xpGain = 5;
            label = "Observation";
        }

        if (xpGain > 0) addXp(xpGain, label);
    }

    function closeDetail() {
        selectedDetail = null;
    }

    import RetroWindow from "./components/uikit/RetroWindow.svelte";
    // import Roots from "./components/ecosystem/tree/Roots.svelte"; // Moved back to Surface
    import { addXp, lastXpGain } from "./lib/progression.js";
    import { fly } from "svelte/transition";

    // EXPERT MODE (L3 Bio)
    let isExpertMode = false;

    // XP FEEDBACK LOGIC
    let feedback = null;
    lastXpGain.subscribe((val) => {
        if (val.amount > 0) {
            feedback = val;
            setTimeout(() => (feedback = null), 2000);
        }
    });
</script>

<div
    class="w-full h-full relative overflow-hidden font-pixel group select-none"
>
    <!-- ... (backgrounds remain same) ... -->
    <!-- 1. BACKGROUND GRADIENT (Depth) -->
    <div
        class="absolute inset-0 bg-gradient-to-b from-[#4E342E] via-[#3E2723] to-[#1A100E] z-0"
    ></div>

    <!-- 2. TEXTURE OVERLAY (Noise) -->
    <div
        class="absolute inset-0 opacity-20 pointer-events-none z-0"
        style="background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSIjMDAwIiBvcGFjaXR5PSIwLjEiLz48L3N2Zz4='); background-size: 4px 4px;"
    ></div>

    <!-- 3a. PXEL-ART MYCELIUM & NITROGEN CYCLE -->
    {#if soilState === "moist" && !isFrozen}
        <!-- MYCELIUM (Pixel Art Style: White dotted web) -->
        <div class="absolute inset-0 z-0 opacity-40 pointer-events-none">
            <!-- Horizontal Connections -->
            <div
                class="absolute top-[20%] left-0 w-full h-[1px] bg-white/30"
                style="background-image: linear-gradient(90deg, white 50%, transparent 50%); background-size: 4px 1px;"
            ></div>
            <div
                class="absolute top-[60%] left-0 w-full h-[1px] bg-white/30"
                style="background-image: linear-gradient(90deg, white 50%, transparent 50%); background-size: 4px 1px;"
            ></div>

            <!-- Vertical tap roots/connections -->
            <div
                class="absolute top-0 left-[30%] h-full w-[1px] bg-white/20"
                style="background-image: linear-gradient(0deg, white 50%, transparent 50%); background-size: 1px 4px;"
            ></div>
            <div
                class="absolute top-0 left-[70%] h-full w-[1px] bg-white/20"
                style="background-image: linear-gradient(0deg, white 50%, transparent 50%); background-size: 1px 4px;"
            ></div>

            <!-- Random Nodes (Spores) -->
            {#each Array(15) as _, i}
                <div
                    class="absolute w-1 h-1 bg-white opacity-60"
                    style="left: {Math.random() * 90}%; top: {Math.random() *
                        90}%; box-shadow: 2px 0 0 white, -2px 2px 0 white;"
                ></div>
            {/each}
        </div>
    {/if}

    <!-- 3b. FLUX LAYERS (Educational) -->

    <!-- NITROGEN CYCLE (Blue Particles) -->
    {#if fluxState.nitrogen}
        <div class="absolute inset-0 z-10 pointer-events-none">
            {#each Array(12) as _, i}
                <div
                    class="absolute text-[8px] font-bold text-blue-200 animate-nitrogen-flow flex flex-col items-center"
                    style="left: {10 + Math.random() * 80}%; top: {80 +
                        Math.random() * 20}%; animation-delay: {Math.random() *
                        5}s"
                >
                    <span>{isExpertMode ? "NO₃⁻" : "N"}</span>
                    {#if isExpertMode}<span class="text-[6px] text-yellow-500"
                            >NH₄⁺</span
                        >{/if}
                </div>
            {/each}
        </div>
    {/if}

    <!-- CARBON CYCLE (Humus Storage - Brown Particles) -->
    {#if fluxState.carbon}
        <div class="absolute inset-0 z-10 pointer-events-none">
            {#each Array(15) as _, i}
                <div
                    class="absolute w-2 h-2 bg-[#3E2723] opacity-80 animate-settle border border-black/20"
                    style="left: {Math.random() * 95}%; top: {10 +
                        Math.random() * 40}%; animation-duration: {5 +
                        Math.random() * 5}s"
                >
                    {#if isExpertMode}<span
                            class="text-[6px] text-white absolute -top-2"
                            >C</span
                        >{/if}
                </div>
            {/each}
        </div>
    {/if}

    <!-- 3b. METHANE BUBBLES (Anaerobic State) -->
    {#if isAnaerobic}
        <div class="absolute inset-0 z-10 pointer-events-none">
            {#each Array(10) as _, i}
                <div
                    class="absolute w-2 h-2 rounded-full border border-green-400 bg-green-900/50 animate-bubble"
                    style="left: {Math.random() * 90}%; top: {100 -
                        Math.random() * 50}%; animation-delay: {Math.random() *
                        3}s; animation-duration: {3 + Math.random()}s"
                >
                    {#if isExpertMode}
                        <span
                            class="text-[6px] text-green-300 absolute -top-3 left-0"
                            >CH₄</span
                        >
                    {/if}
                </div>
            {/each}
        </div>
    {/if}

    <!-- EXPERT TOGGLE -->
    <button
        class="absolute top-4 left-4 z-50 bg-black/50 hover:bg-black/80 text-white text-[10px] px-2 py-1 rounded border border-white/20 transition-colors"
        on:click={() => (isExpertMode = !isExpertMode)}
    >
        {isExpertMode ? "🧪 Mode : L3 (Expert)" : "🎓 Mode : Découverte"}
    </button>

    <!-- 3c. RAIN INFILTRATION (If Raining) -->
    {#if isRaining}
        <div class="absolute inset-0 z-10 pointer-events-none opacity-50">
            {#each Array(10) as _, i}
                <div
                    class="absolute w-[1px] h-20 bg-blue-400 opacity-60 animate-infiltrate"
                    style="left: {Math.random() *
                        100}%; top: -20px; animation-delay: {Math.random() *
                        2}s; animation-duration: {1 + Math.random()}s"
                ></div>
            {/each}
        </div>

        <!-- LEACHING LESSON (Tooltip floating) -->
        <div
            class="absolute top-4 right-4 z-50 cursor-magnify animate-bounce"
            on:click={() => openDetail("leaching")}
            on:keydown={(e) => e.key === "Enter" && openDetail("leaching")}
            role="button"
            tabindex="0"
        >
            <div
                class="bg-blue-100 border-l-4 border-blue-500 text-blue-900 p-2 text-xs font-bold shadow-lg flex items-center gap-2"
            >
                🌧️ Il pleut ! (Lessivage ?)
            </div>
        </div>
    {/if}

    <!-- 3b. DECORATIONS (Roots & Stones - Static) -->
    {#each Array(10) as _, i}
        <div
            class="absolute bg-[#3E2723] rounded opacity-50 z-0"
            style="
                left: {Math.random() * 100}%; 
                top: {Math.random() * 100}%; 
                width: {4 + Math.random() * 8}px; 
                height: {4 + Math.random() * 8}px;
             "
        ></div>
    {/each}
    <!-- Big Roots (CSS Art) - Clickable for Symbiosis -->
    <div
        class="absolute top-0 left-10 w-4 h-32 cursor-magnify z-20 group/root"
        on:click={() => openDetail("symbiosis")}
        on:keydown={(e) => e.key === "Enter" && openDetail("symbiosis")}
        role="button"
        tabindex="0"
    >
        <div
            class="w-full h-full {isRotting
                ? 'bg-black'
                : 'bg-[#3E2723]'} opacity-80 rotate-6 group-hover/root:bg-[#5D4037] transition-colors duration-1000"
        ></div>
        <!-- Tooltip hint -->
        <div
            class="absolute top-1/2 left-full ml-2 opacity-0 group-hover/root:opacity-100 bg-black/70 text-white text-[10px] p-1 rounded whitespace-nowrap pointer-events-none"
        >
            🤝 Symbiose ?
        </div>
    </div>
    <div
        class="absolute top-0 left-14 w-2 h-20 {isRotting
            ? 'bg-black'
            : 'bg-[#3E2723]'} opacity-60 z-0 -rotate-3 pointer-events-none transition-colors duration-1000"
    ></div>

    <!-- 4. INTERACTIVE ITEMS -->
    <!-- TREE ROOTS moved back to SmartTree -->

    {#each items as item}
        {@const type = getItemType(item.type)}
        <div
            class="absolute group/item cursor-magnify transition-transform hover:scale-125 z-10"
            style="left: {item.left}%; top: {item.top}%; transform: scale({item.scale *
                2});"
            on:click={() => openDetail(type)}
            on:keydown={(e) => e.key === "Enter" && openDetail(type)}
            role="button"
            tabindex="0"
            on:mouseenter={(e) => showInfo(type, e.clientX, e.clientY)}
            on:mouseleave={hideInfo}
        >
            {#if type === "rock"}
                <div
                    class="w-3 h-3 bg-[#5D4037] border-r-2 border-b-2 border-black/30"
                >
                    <div class="w-1 h-1 bg-[#8D6E63]"></div>
                </div>
            {:else if type === "fossil"}
                <div class="relative">
                    <div class="w-4 h-3 bg-[#D7CCC8]"></div>
                    <div
                        class="w-1 h-1 bg-[#3E2723] absolute top-1 left-1"
                    ></div>
                </div>
            {:else if type === "cah"}
                <!-- CAH MINI (Icone cliquable) -->
                <div class="relative animate-pulse">
                    <div
                        class="w-2 h-2 bg-blue-400 absolute left-0 top-0 ring-1 ring-blue-300"
                    ></div>
                    <!-- Argile -->
                    <div
                        class="w-2 h-2 bg-stone-900 absolute left-2 top-0 ring-1 ring-stone-600"
                    ></div>
                    <!-- Humus -->
                    <div
                        class="w-4 h-1 bg-yellow-500 absolute top-1 left-0 z-10 opacity-80"
                    ></div>
                </div>
            {:else if type === "gold"}
                <div
                    class="w-2 h-2 bg-yellow-400 border border-yellow-600 animate-pulse shadow-[0_0_5px_gold]"
                ></div>
            {:else}
                <!-- Gem -->
                <div
                    class="w-2 h-3 bg-cyan-300 animate-pulse shadow-[0_0_8px_cyan]"
                ></div>
            {/if}
        </div>
    {/each}

    <!-- 5. VERS DE TERRE (PIXEL ART STRICT) -->
    <!-- ANECIQUE (Vertical, Sombre, Costaud) vs ENDOGE (Horizontal, Pale, Fin) -->
    {#if lifeDensity !== "frozen"}
        {#each activeWorms as worm}
            <div
                class="absolute z-20 cursor-magnify hover:z-50 group/worm"
                on:click={() => openDetail(worm.type)}
                on:keydown={(e) => e.key === "Enter" && openDetail(worm.type)}
                role="button"
                tabindex="0"
                on:mouseenter={(e) => showInfo(worm.type, e.clientX, e.clientY)}
                on:mouseleave={hideInfo}
                style="
                    top: {worm.top}%; 
                    left: {worm.left}%;
                    --duration: {worm.duration}s; 
                    --delay: {worm.delay}s;
                    --dir: {worm.direction};
                    --v-range: {worm.top > 50 ? -40 : 40}vh; 
                 "
                class:animate-crawl-across={worm.type === "endoge"}
                class:animate-crawl-vertical={worm.type === "anecique"}
            >
                {#if worm.type === "anecique"}
                    <!-- VERS ANECIQUE (VERTICAL/ROBUSTE) -->
                    <!-- Design: BLOCS SOLIDES (Pas de bordure floue) -->
                    <div class="flex flex-col items-center">
                        <!-- Tête (Carré sombre) -->
                        <div class="w-4 h-4 bg-[#3E2723]"></div>
                        <!-- Corps (Bande large) -->
                        <div class="w-3 h-3 bg-[#5D4037]"></div>
                        <div class="w-3 h-3 bg-[#4E342E]"></div>
                        <div class="w-3 h-3 bg-[#5D4037]"></div>
                        <!-- Clitellum (Anneau large) -->
                        <div class="w-4 h-2 bg-[#8D6E63]"></div>
                        <div class="w-3 h-3 bg-[#5D4037]"></div>
                        <div class="w-2 h-2 bg-[#4E342E]"></div>
                    </div>
                {:else}
                    <!-- VERS ENDOGE (HORIZONTAL/PALE) -->
                    <!-- Design: LIGNE DE PIXELS (Fil rose) -->
                    <div class="flex items-center animate-wiggle gap-[1px]">
                        <!-- Tête -->
                        <div class="w-2 h-2 bg-[#D81B60]"></div>
                        <!-- Corps (Segments simples) -->
                        <div class="w-2 h-2 bg-[#F48FB1]"></div>
                        <div class="w-2 h-2 bg-[#F8BBD0]"></div>
                        <div class="w-2 h-2 bg-[#F48FB1]"></div>
                        <!-- Clitellum -->
                        <div class="w-2 h-2 bg-[#FFCDD2]"></div>
                        <div class="w-2 h-2 bg-[#F48FB1]"></div>
                        <div class="w-2 h-2 bg-[#F8BBD0]"></div>
                        <div class="w-1 h-1 bg-[#F48FB1]"></div>
                    </div>
                {/if}
            </div>
        {/each}

        <!-- 5b. COLLEMBOLES (Micro-pixels blancs sauteurs) -->
        {#each collembolePool.slice(0, collemboleCount) as c}
            <div
                class="absolute w-1 h-1 bg-white opacity-90 animate-jump pointer-events-none z-10"
                style="left: {c.left}%; top: {c.top}%; animation-delay: {c.delay}s; transform: scale({c.scale});"
            ></div>
        {/each}

        <!-- RONGEUR (Mulot / Campagnol) - SPRITE PIXEL ART -->
        <div
            class="absolute bottom-0 left-20 z-40 transition-transform duration-1000 ease-out cursor-magnify group/rodent"
            style="transform: translateY({showRodent ? '0%' : '100%'});"
            role="button"
            tabindex="0"
            on:click={() => openDetail(rodentType)}
            on:keydown={(e) => e.key === "Enter" && openDetail(rodentType)}
            on:mouseenter={(e) => showInfo(rodentType, e.clientX, e.clientY)}
            on:mouseleave={hideInfo}
        >
            <div class="relative w-16 h-12">
                {#if rodentType === "mulot"}
                    <!-- MULOT (Pixel Block Sprite) -->
                    <!-- Body -->
                    <div
                        class="absolute bottom-0 left-2 w-12 h-8 bg-[#5D4037] border-t-4 border-r-4 border-[#3E2723]"
                    ></div>
                    <!-- Head -->
                    <div
                        class="absolute bottom-2 left-10 w-6 h-6 bg-[#5D4037] border-4 border-[#3E2723]"
                    ></div>
                    <!-- Big Ear -->
                    <div
                        class="absolute top-0 left-10 w-2 h-4 bg-[#8D6E63] border-2 border-[#3E2723]"
                    ></div>
                    <!-- Tail -->
                    <div
                        class="absolute bottom-0 left-0 w-8 h-1 bg-pink-300 -translate-x-full"
                    ></div>
                {:else}
                    <!-- CAMPAGNOL (Chunky Block) -->
                    <div
                        class="absolute bottom-0 left-0 w-14 h-10 bg-[#3E2723] border-4 border-black/30"
                    ></div>
                    <!-- Small Ear -->
                    <div
                        class="absolute top-0 left-10 w-2 h-2 bg-[#5D4037]"
                    ></div>
                {/if}

                <!-- Common Face -->
                <div
                    class="absolute bottom-4 right-1 w-1 h-1 bg-black animate-blink"
                ></div>
                <!-- Eye -->
                <div
                    class="absolute bottom-6 right-0 w-1 h-1 bg-pink-400"
                ></div>
                <!-- Nose -->
            </div>
        </div>
    {:else}
        <div
            class="absolute inset-0 flex items-center justify-center z-30 pointer-events-none"
        >
            <div
                class="{isOverheated
                    ? 'bg-red-900/80 border-red-500 text-red-100'
                    : 'bg-blue-900/80 border-blue-500 text-blue-100'} p-4 border-4 text-xl text-center font-bold shadow-2xl backdrop-blur-sm transition-colors duration-500"
            >
                {#if isOverheated}
                    🔥 SOL BRÛLANT ({safeData.soil_temp}°C)
                {:else if isFrozen}
                    ❄️ SOL GELÉ ({safeData.soil_temp}°C)
                {:else}
                    ❄️ SOL INACTIF ({safeData.soil_temp}°C)
                {/if}
            </div>
        </div>
    {/if}

    <!-- MODALE DETAIL (Center Overlay) -->
    <!-- (Garder le code de modale existant, il est bon) -->
    {#if selectedDetail}
        <div
            class="absolute inset-0 z-[100] bg-black/90 flex items-center justify-center p-4 backdrop-blur-sm"
            on:click={closeDetail}
            on:keydown={(e) => e.key === "Escape" && closeDetail()}
            role="button"
            tabindex="0"
        >
            <div
                class="relative bg-[#3E2723] p-1 shadow-[8px_8px_0_rgba(0,0,0,0.5)] max-w-lg w-full max-h-[90vh] flex flex-col pointer-events-auto border-4 border-[#558B2F]"
                on:click|stopPropagation
                on:keydown|stopPropagation
                role="presentation"
            >
                <!-- INNER CONTENT -->
                <div class="h-full flex flex-col p-6 overflow-y-auto">
                    <!-- Close Button (Nature - Enhanced for Mobile) -->
                    <button
                        class="absolute top-2 right-2 bg-[#558B2F] border-2 border-[#7CB342] text-white w-10 h-10 flex items-center justify-center font-bold text-xl leading-none z-50 hover:bg-[#7CB342] transition-colors shadow-lg active:scale-95"
                        on:click={closeDetail}
                        aria-label="Fermer">X</button
                    >

                    <!-- HEADER IMAGE / ICON (Mobile Friendly) -->
                    <div class="mt-8 mb-4"></div>

                    {#if selectedDetail === "cah"}
                        <!-- HEADER -->
                        <h2
                            class="text-2xl text-[#C0CA33] mb-2 border-b-2 border-[#558B2F] pb-2 font-bold flex items-center gap-2"
                        >
                            <span>✨ Le Complexe Argilo-Humique</span>
                        </h2>
                        <p
                            class="text-[#DCEDC8] text-xs italic mb-4 font-serif"
                        >
                            "Le Garde-Manger du Sol"
                        </p>

                        <!-- VISUALISATION CAH -->
                        <div
                            class="flex flex-col items-center gap-4 mb-6 py-6 bg-[#2E3B20] rounded-xl border border-[#558B2F] relative overflow-hidden"
                        >
                            <!-- Diagramme Interactif -->
                            <div
                                class="flex items-center justify-center gap-2 relative z-10 scale-125 my-4"
                            >
                                <!-- ARGILE (-) -->
                                <div
                                    class="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-[10px] font-bold shadow-[0_0_15px_blue] z-10 border-2 border-blue-300"
                                >
                                    ARGILE (-)
                                </div>

                                <!-- PONT CALCIUM (++) -->
                                <div
                                    class="flex flex-col items-center gap-1 animate-pulse"
                                >
                                    <div class="w-8 h-1 bg-yellow-500"></div>
                                    <div
                                        class="w-6 h-6 bg-yellow-500 rounded-full text-black font-bold text-xs flex items-center justify-center border border-white"
                                    >
                                        Ca²+
                                    </div>
                                    <div class="w-8 h-1 bg-yellow-500"></div>
                                </div>

                                <!-- HUMUS (-) -->
                                <div
                                    class="w-16 h-16 bg-[#5D4037] rounded-full flex items-center justify-center text-[#EFEBE9] text-[10px] font-bold shadow-[0_0_15px_#5D4037] z-10 border-2 border-[#8D6E63] relative"
                                >
                                    HUMUS (-)
                                    <!-- Micro-bactéries dessus -->
                                    <div
                                        class="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-bounce"
                                    ></div>
                                </div>
                            </div>

                            <!-- Legend -->
                            <div
                                class="bg-black/50 px-4 py-2 rounded text-[10px] text-center border border-gray-700"
                            >
                                <span class="text-blue-300">Argile</span> et
                                <span class="text-[#A1887F]">Humus</span>
                                sont chargés <strong>négativement</strong>.<br
                                />
                                Ils se repoussent... sauf si le
                                <span class="text-yellow-400 font-bold"
                                    >CALCIUM (Ca²+)</span
                                > fait le pont !
                            </div>
                        </div>

                        <div class="space-y-3 text-sm text-gray-200 font-sans">
                            <div class="flex gap-2 items-start">
                                <span class="text-xl">🛡️</span>
                                <p>
                                    <strong>Protection :</strong> Cette structure
                                    protège l'Humus contre une dégradation trop rapide
                                    par les bactéries.
                                </p>
                            </div>
                            <div class="flex gap-2 items-start">
                                <span class="text-xl">💧</span>
                                <p>
                                    <strong>Éponge :</strong> Le C.A.H retient l'eau
                                    et les nutriments (Azote, Phosphore) pour les
                                    donner aux plantes quand elles ont faim.
                                </p>
                            </div>
                            <div
                                class="bg-yellow-900/30 p-2 rounded border border-yellow-700 text-xs mt-2"
                            >
                                💡 <strong>Le Saviez-vous ?</strong> Les vers de
                                terre créent ce complexe dans leur intestin en mélangeant
                                terre et matière organique !
                            </div>
                        </div>
                    {:else if selectedDetail === "mulot" || selectedDetail === "campagnol"}
                        <!-- DETAIL RONGEURS -->
                        {@const isMulot = selectedDetail === "mulot"}
                        <h2
                            class="text-2xl mb-2 border-b-4 pb-2 font-bold flex items-center gap-2 text-orange-400 border-orange-700"
                        >
                            {isMulot
                                ? "🐭 Le Mulot Sylvestre"
                                : "🐹 Le Campagnol"}
                        </h2>

                        <div
                            class="flex gap-4 items-center mb-4 bg-black/40 p-4 rounded-lg text-sm text-gray-200"
                        >
                            <div class="text-4xl">{isMulot ? "🏃" : "🚜"}</div>
                            <div>
                                <p class="font-bold text-white mb-1">
                                    {isMulot ? "Le Sprinter" : "Le Bulldozer"}
                                </p>
                                <p>
                                    {isMulot
                                        ? "Il saute et court partout."
                                        : "Il creuse des galeries massives."}
                                </p>
                            </div>
                        </div>

                        <div class="space-y-3 text-sm text-gray-300 font-sans">
                            <p>
                                {isMulot
                                    ? "Le mulot est un opportuniste. Il utilise souvent les galeries des autres (taupes, campagnols) pour se déplacer à l'abri."
                                    : "Le campagnol laboure la terre ! Ses galeries aèrent le sol et mangent les racines (aïe pour le jardinier, mais utile pour le sol sauvage)."}
                            </p>
                            <div
                                class="bg-orange-900/30 p-3 rounded border border-orange-700 mt-2"
                            >
                                🍽️ <strong>Régime :</strong>
                                {isMulot
                                    ? "Graines, insectes, escargots."
                                    : "Racines, tubercules, herbes."}
                            </div>
                        </div>
                    {:else if selectedDetail === "symbiosis"}
                        <!-- DETAIL SYMBIOSE -->
                        <h2
                            class="text-2xl mb-2 border-b-4 pb-2 font-bold flex items-center gap-2 text-green-400 border-green-700"
                        >
                            🤝 Le "Deal" Souterrain
                        </h2>
                        <p class="text-gray-400 text-xs italic mb-4">
                            La Symbiose Mycorhizienne
                        </p>

                        <div
                            class="flex flex-col items-center gap-6 py-4 bg-[#1A202C] rounded-xl border border-gray-700 relative overflow-hidden"
                        >
                            <!-- Visualization of the Deal -->
                            <div
                                class="flex items-center justify-between w-full px-8 relative z-10"
                            >
                                <!-- PLANT -->
                                <div class="flex flex-col items-center gap-2">
                                    <div class="text-4xl">🌱</div>
                                    <div class="font-bold text-green-300">
                                        Plante
                                    </div>
                                    <div
                                        class="bg-green-900/50 p-2 rounded text-center text-[10px] w-24 border border-green-700"
                                    >
                                        Photosynthèse<br />(Soleil)
                                    </div>
                                </div>

                                <!-- EXCHANGE ARROWS -->
                                <div
                                    class="flex flex-col gap-4 items-center flex-1"
                                >
                                    <!-- Sugar Down -->
                                    <div
                                        class="flex items-center gap-2 animate-pulse text-pink-300"
                                    >
                                        <span class="text-xs">SUCRES 🍬</span>
                                        <div
                                            class="w-16 h-1 bg-gradient-to-r from-green-500 to-white"
                                        ></div>
                                        <span>➡️</span>
                                    </div>

                                    <!-- Nutrients Up -->
                                    <div
                                        class="flex items-center gap-2 animate-pulse text-blue-300"
                                        style="animation-delay: 0.5s"
                                    >
                                        <span>⬅️</span>
                                        <div
                                            class="w-16 h-1 bg-gradient-to-l from-white to-green-500"
                                        ></div>
                                        <span class="text-xs"
                                            >EAU + AZOTE 💧</span
                                        >
                                    </div>
                                </div>

                                <!-- FUNGI -->
                                <div class="flex flex-col items-center gap-2">
                                    <div class="text-4xl">🍄</div>
                                    <div class="font-bold text-white">
                                        Champignon
                                    </div>
                                    <div
                                        class="bg-gray-700/50 p-2 rounded text-center text-[10px] w-24 border border-gray-600"
                                    >
                                        Réseau Mycélium<br />(Internet du Sol)
                                    </div>
                                </div>
                            </div>

                            <div
                                class="bg-blue-900/30 p-3 mx-4 rounded border border-blue-700 text-xs text-center"
                            >
                                La plante ne peut pas aller chercher l'eau très
                                loin.<br />
                                Le champignon rallonge ses racines de
                                <strong>x1000</strong> ! En échange, elle le nourrit
                                en sucre.
                            </div>
                        </div>
                    {:else if selectedDetail === "gold" || selectedDetail === "gem"}
                        <!-- DETAIL GEOLOGIE -->
                        <h2
                            class="text-2xl mb-2 border-b-4 pb-2 font-bold flex items-center gap-2 text-yellow-400 border-yellow-700"
                        >
                            💎 La Fausse Richesse
                        </h2>

                        <div
                            class="flex flex-col items-center gap-4 py-8 bg-[#1A202C] rounded-xl border border-gray-700 text-center"
                        >
                            <div class="text-6xl animate-bounce">0️⃣</div>

                            <div class="space-y-2 px-6">
                                <p class="text-white font-bold text-lg">
                                    Valeur Biologique : NULLE.
                                </p>
                                <p class="text-gray-400 text-sm">
                                    Pour un humain, c'est précieux.<br />
                                    Mais pour une plante ? C'est juste un caillou
                                    qui brille.
                                </p>
                                <p class="text-gray-400 text-sm">
                                    Ça ne se mange pas, ça ne retient pas l'eau.
                                </p>
                            </div>

                            <div
                                class="mt-4 bg-green-900/50 p-3 rounded border border-green-700 text-green-200 text-sm font-bold"
                            >
                                La vraie richesse du sol, c'est l'Humus (l'Or
                                Noir) ! 🌱
                            </div>
                        </div>
                    {:else if selectedDetail === "leaching"}
                        <!-- DETAIL LESSIVAGE (Bataille Engrais) -->
                        <h2
                            class="text-2xl mb-2 border-b-4 pb-2 font-bold flex items-center gap-2 text-blue-400 border-blue-700"
                        >
                            🌧️ La Bataille des Engrais
                        </h2>

                        <div
                            class="bg-[#2D3748] p-4 rounded text-center space-y-4"
                        >
                            <div
                                class="flex justify-center gap-8 text-xs font-bold"
                            >
                                <div
                                    class="w-1/2 p-2 bg-red-900/30 border border-red-700 rounded opacity-50 grayscale"
                                >
                                    <span class="text-xl">🧪</span><br />Engrais
                                    Chimique<br />
                                    <span class="text-red-400">LESSIVÉ !</span>
                                    <div
                                        class="mt-2 h-1 w-full bg-red-500 rounded animate-ping"
                                    ></div>
                                </div>
                                <div
                                    class="w-1/2 p-2 bg-green-900/30 border border-green-700 rounded"
                                >
                                    <span class="text-xl">🛡️</span><br
                                    />C.A.H<br />
                                    <span class="text-green-400">RETENU !</span>
                                    <div
                                        class="mt-2 text-[10px] text-left text-gray-300"
                                    >
                                        Les nutriments (Ca, K, N, P) sont collés
                                        à l'argile et l'humus. L'eau passe
                                        claire.
                                    </div>
                                </div>
                            </div>

                            <p class="text-sm text-gray-300">
                                Quand il pleut fort, les engrais liquides sont
                                emportés dans la nappe phréatique (pollution).<br
                                />
                                Mais le <strong>Complexe Argilo-Humique</strong>
                                agit comme un aimant : il retient tout pour plus
                                tard !
                            </p>
                        </div>
                    {:else if selectedDetail === "anecique" || selectedDetail === "endoge"}
                        <!-- DETAIL VERS -->
                        {@const isAnecique = selectedDetail === "anecique"}
                        <h2
                            class="text-2xl mb-2 border-b-4 pb-2 font-bold flex items-center gap-2 {isAnecique
                                ? 'text-pink-800 border-pink-800'
                                : 'text-purple-800 border-purple-800'}"
                        >
                            {isAnecique
                                ? "🪱 Le Ver Anécique"
                                : "🚇 Le Ver Endogé"}
                        </h2>

                        <div
                            class="flex flex-col sm:flex-row gap-6 items-start mt-4 font-sans"
                        >
                            <!-- Portrait Robot -->
                            <div
                                class="w-full sm:w-1/3 bg-black/40 p-4 rounded-lg border border-white/10 flex flex-col items-center"
                            >
                                <div class="text-4xl mb-2">
                                    {isAnecique ? "↕️" : "↔️"}
                                </div>
                                <div class="font-bold text-white mb-1">
                                    {isAnecique ? "Le Géant" : "L'Architecte"}
                                </div>
                                <div class="text-xs text-gray-400 text-center">
                                    {isAnecique
                                        ? "Vit jusqu'à 3m de profondeur !"
                                        : "Vit dans les 20 premiers cm."}
                                </div>

                                <!-- Visualisation Galerie -->
                                <div
                                    class="mt-4 w-full h-24 bg-[#3E2723] relative border border-[#5D4037] overflow-hidden rounded"
                                >
                                    {#if isAnecique}
                                        <div
                                            class="absolute inset-x-0 top-0 bottom-0 w-2 bg-black/50 mx-auto"
                                        ></div>
                                        <!-- Vertical -->
                                        <div
                                            class="absolute bottom-0 left-1/2 -translate-x-1/2 text-xs"
                                        >
                                            🏠
                                        </div>
                                    {:else}
                                        <div
                                            class="absolute inset-y-0 left-0 right-0 h-2 bg-black/50 my-auto top-1/2"
                                        ></div>
                                        <!-- Horizontal -->
                                        <div
                                            class="absolute top-1/2 left-4 text-xs -translate-y-1/2"
                                        >
                                            🏠
                                        </div>
                                    {/if}
                                </div>
                            </div>

                            <!-- Fiche Technique -->
                            <div
                                class="w-full sm:w-2/3 space-y-4 text-sm text-gray-200"
                            >
                                <div>
                                    <h4
                                        class="font-bold text-white uppercase text-xs mb-1 bg-white/10 px-1 inline-block rounded"
                                    >
                                        Son Rôle
                                    </h4>
                                    <p>
                                        {isAnecique
                                            ? "Il monte chercher les feuilles en surface la nuit et les redescend au fond. C'est le grand mélangeur du sol."
                                            : "Il creuse des galeries horizontales sans arrêt. Il mange la terre et la digère."}
                                    </p>
                                </div>

                                <div>
                                    <h4
                                        class="font-bold text-white uppercase text-xs mb-1 bg-white/10 px-1 inline-block rounded"
                                    >
                                        Super-Pouvoir
                                    </h4>
                                    <ul class="list-disc pl-4 space-y-1">
                                        {#if isAnecique}
                                            <li>
                                                Crée de la fertilité en
                                                profondeur.
                                            </li>
                                            <li>
                                                Ses galeries permettent à l'eau
                                                de pluie de s'infiltrer
                                                rapidement.
                                            </li>
                                        {:else}
                                            <li>
                                                Ses excréments (turricules)
                                                contiennent 5x plus d'azote que
                                                la terre environnante !
                                            </li>
                                            <li>
                                                Aère le sol pour les racines des
                                                plantes.
                                            </li>
                                        {/if}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    {/if}

                    <!-- Mobile Bottom Close Button -->
                    <div class="mt-8 flex justify-center w-full">
                        <button
                            class="bg-[#558B2F] border-2 border-[#7CB342] text-white px-6 py-3 font-bold rounded-none shadow-[4px_4px_0_black] active:translate-y-1 active:shadow-none transition-all hover:bg-[#689F38]"
                            on:click={closeDetail}
                        >
                            FERMER
                        </button>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>

<style>
    /* HORIZONTAL (Endogés) - STOP & GO (RALENTI) */
    @keyframes crawlAcrossStopGo {
        0% {
            transform: translateX(-10vw) scaleX(1);
        }
        10% {
            transform: translateX(-10vw) scaleX(1);
        }

        20% {
            transform: translateX(5vw) scaleX(0.9);
        }
        35% {
            transform: translateX(5vw) scaleX(1);
        }

        50% {
            transform: translateX(20vw) scaleX(0.9);
        }
        65% {
            transform: translateX(20vw) scaleX(1);
        }

        80% {
            transform: translateX(40vw) scaleX(0.9);
        }
        100% {
            transform: translateX(110vw) scaleX(1);
        }
    }

    .animate-crawl-across {
        position: absolute;
        left: 0;
        scale: var(--dir) 1;
        /* RALENTI : 80s au lieu de 45s */
        animation: crawlAcrossStopGo 80s steps(20) infinite;
        animation-delay: var(--delay);
    }

    /* VERTICAL (Anéciques) - STOP & GO (RALENTI) */
    @keyframes crawlVerticalStopGo {
        0% {
            transform: translateY(0);
        }
        15% {
            transform: translateY(0);
        } /* Longue pause Surface */

        30% {
            transform: translateY(var(--v-range));
        } /* Plongée par à-coups via steps() */
        50% {
            transform: translateY(var(--v-range));
        } /* Pause Fond */

        70% {
            transform: translateY(0);
        } /* Remonte */
        100% {
            transform: translateY(0);
        }
    }

    .animate-crawl-vertical {
        position: absolute;
        /* RALENTI : 60s au lieu de 30s */
        animation: crawlVerticalStopGo 60s steps(15) infinite;
        animation-delay: var(--delay);
    }

    /* WIGGLE (Ondulation Endogé) */
    @keyframes wiggle {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-2px);
        }
    }
    .animate-wiggle {
        animation: wiggle 0.5s ease-in-out infinite;
    }

    @keyframes jump {
        0%,
        90% {
            transform: translate(0, 0);
        }
        95% {
            transform: translate(0, -10px);
        }
        100% {
            transform: translate(5px, 0);
        }
    }
    .animate-jump {
        animation: jump 2s ease-in-out infinite;
    }

    @keyframes blink {
        0%,
        90%,
        100% {
            transform: scaleY(1);
        }
        95% {
            transform: scaleY(0.1);
        }
    }
    .animate-blink {
        animation: blink 3s infinite;
    }

    @keyframes nitrogenFlow {
        0% {
            transform: translate(0, 0);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        100% {
            transform: translate(0, -60vh);
            opacity: 0;
        }
    }
    .animate-nitrogen-flow {
        animation: nitrogenFlow 4s linear infinite;
    }

    @keyframes infiltrate {
        0% {
            transform: translateY(0);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        100% {
            transform: translateY(100vh);
            opacity: 0;
        }
    }
    .animate-infiltrate {
        animation: infiltrate 2s linear infinite;
    }

    @keyframes bubble {
        0% {
            transform: translateY(0) scale(0.5);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        100% {
            transform: translateY(-50vh) scale(1.2);
            opacity: 0;
        }
    }
    .animate-bubble {
        animation: bubble 4s ease-in infinite;
    }

    @keyframes nitrogenFlow {
        0% {
            transform: translateY(0);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: translateY(-20px);
            opacity: 0;
        }
    }
    .animate-nitrogen-flow {
        animation: nitrogenFlow 3s linear infinite;
    }

    @keyframes settle {
        0% {
            transform: translateY(0);
            opacity: 0;
        }
        20% {
            opacity: 1;
        }
        100% {
            transform: translateY(20px);
            opacity: 0.5;
        }
    }
    .animate-settle {
        animation: settle 5s ease-out infinite;
    }
</style>
