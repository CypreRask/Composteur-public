<script>
  // @ts-nocheck
  import { onMount } from "svelte";
  import RetroWindow from "./components/uikit/RetroWindow.svelte";
  import BioMonitor from "./components/uikit/BioMonitor.svelte";

  let { data = [] } = $props();

  let timeRange = $state("24h");
  let forecast = $state(null);
  let isExpert = $state(false); // Default to Visitor Mode
  let historyData = $state([]); // For long-term views

  // ============ LOGIC ============
  function calcAeration(co2, ch4) {
    return (co2 / (ch4 + 1)) * 100;
  }
  function calcActivity(co2, temp) {
    return Math.max(0, Math.min(100, (co2 - 400) / 10 + temp / 2));
  }
  function getPhase(temp, co2) {
    if (!temp || !co2) return "-";
    if (temp < 20) return "Démarrage";
    if (temp < 45 && co2 > 600) return "Montée";
    if (temp >= 45 && temp <= 65) return "Thermophile";
    if (temp > 65) return "Surchauffe";
    if (temp < 45 && co2 < 500) return "Maturation";
    return "Stabilisation";
  }

  // ============ DATA FETCHING (HISTORY) ============
  async function fetchHistory(range) {
    let days = 1;
    let interval = "hour";

    if (range === "7j") days = 7;
    if (range === "30j") days = 30;
    if (range === "1an") {
      days = 365;
      interval = "day";
    }

    if (range === "24h") {
      historyData = []; // Use live data
      return;
    }

    try {
      const res = await fetch(
        `http://localhost:8085/api/history/aggregate?interval=${interval}&days=${days}`,
      );
      if (res.ok) {
        const raw = await res.json();
        // REMAP TO FRONTEND SCHEMA
        historyData = raw.map((d) => ({
          timestamp: d.timestamp,
          temp_scd: d.temp,
          hum_scd: d.hum,
          co2: d.co2,
          mq137: d.nh3,
          mq4: d.ch4,
        }));
      }
    } catch (e) {
      console.error("History fetch failed", e);
    }
  }

  // Auto-fetch when timeRange changes
  $effect(() => {
    fetchHistory(timeRange);
  });

  // ============ FILTRAGE ============
  function getFilteredData() {
    // If long range, use fetched history
    if (timeRange !== "24h" && historyData.length > 0) {
      return historyData;
    }

    // Else use props data (Live 24h)
    if (!data || data.length === 0) return [];
    // Just return last 24h if data is large, or all if short
    // Assuming 'data' prop is already limited to recent history by parent
    return data;
  }

  function smoothData(values) {
    if (values.length < 5) return values;
    // Less smoothing for aggregated data to keep precision?
    // Let's keep smooth for visuals
    return values.map((v, i) => {
      const start = Math.max(0, i - 2);
      const end = Math.min(values.length, start + 5);
      const window = values.slice(start, end);
      return window.reduce((a, b) => a + b, 0) / window.length;
    });
  }

  // ============ GRAPH UTIL ============
  function createPath(values, width, height, min, max) {
    if (values.length < 2) return "";
    const range = max - min || 1;
    return values
      .map((v, i) => {
        const x = (i / (values.length - 1)) * width;
        const y = height - ((v - min) / range) * height;
        return `${i === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`;
      })
      .join(" ");
  }

  function getReliabilityColor(reliability) {
    return reliability === "HIGH"
      ? "bg-green-500"
      : "bg-red-500 shadow-[0_0_10px_red] animate-pulse";
  }

  const heuristic = $derived(
    latest?.heuristic || {
      score: 50,
      reliability: "LOW",
      gate_label: "NO_DATA",
    },
  );

  async function fetchForecast() {
    if (!data || data.length < 1) return;
    try {
      const res = await fetch("http://localhost:8085/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          temp_scd: data[data.length - 1]?.temp_scd || 20,
          co2: data[data.length - 1]?.co2 || 400,
          soil_hum: data[data.length - 1]?.soil_hum || 50,
        }),
      });
      if (res.ok) forecast = await res.json();
    } catch (e) {}
  }

  onMount(fetchForecast);

  // ============ DERIVED ============
  // Use local 'filteredData' derived from function
  const filtered = $derived(getFilteredData());
  // Latest always comes from REAL data (prop), not aggregated history
  const latest = $derived(data[data.length - 1] || null);

  const indicators = $derived(
    latest
      ? {
          aeration: calcAeration(latest.co2, latest.mq4),
          activity: calcActivity(latest.co2, latest.temp_scd),
          phase: getPhase(latest.temp_scd, latest.co2),
        }
      : null,
  );

  const chart = $derived({
    temp: filtered.map((d) => d.temp_scd),
    hum: filtered.map((d) => d.hum_scd),
    co2: filtered.map((d) => d.co2),
    nh3: filtered.map((d) => d.mq137),
    ch4: filtered.map((d) => d.mq4),
  });
</script>

<div
  class="p-4 space-y-4 font-pixel text-[#FFF8E1] w-full max-w-[1400px] mx-auto"
>
  <!--HEADER / CONTROL BAR-->
  <div
    class="flex flex-col md:flex-row gap-4 justify-between items-center bg-[#3E2723] p-4 border-4 border-[#558B2F] shadow-[8px_8px_0_rgba(0,0,0,0.5)]"
  >
    <div class="flex items-center gap-4">
      <div
        class="text-2xl font-bold text-[#C0CA33] uppercase tracking-wider cursor-magnify select-none hover:text-white transition-colors"
        onclick={() => (isExpert = !isExpert)}
        onkeydown={(e) =>
          (e.key === "Enter" || e.key === " ") && (isExpert = !isExpert)}
        role="button"
        tabindex="0"
      >
        {isExpert ? "LABO DE MONITORING" : "MONITEUR BIOLOGIQUE"}
      </div>
      {#if filtered.length > 0}
        <div
          class="px-2 py-1 bg-[#22c55e]/20 border border-[#22c55e] text-[#22c55e] text-xs cursor-magnify"
          onclick={() => (isExpert = !isExpert)}
          onkeydown={(e) =>
            (e.key === "Enter" || e.key === " ") && (isExpert = !isExpert)}
          title="Mode Expert / Visiteur"
          role="button"
          tabindex="0"
        >
          {isExpert ? "EXPERT MODE" : "VISITOR MODE"}
        </div>
      {:else}
        <div
          class="px-2 py-1 bg-red-500/20 border border-red-500 text-red-500 text-xs animate-pulse"
        >
          OFFLINE
        </div>
      {/if}
    </div>

    <!-- Time Range Selector -->
    <div class="flex gap-1 p-1 bg-[#2d1b18] border-2 border-[#5d4037]">
      {#each ["24h", "7j", "30j", "1an"] as val}
        <button
          class="px-4 py-1 text-sm font-bold transition-all {timeRange === val
            ? 'bg-[#558B2F] text-white'
            : 'text-[#8d6e63] hover:text-[#C0CA33]'}"
          onclick={() => (timeRange = val)}>{val}</button
        >
      {/each}
    </div>
  </div>

  {#if !isExpert}
    <!-- VISITOR MODE: BIO-MONITOR -->
    <div class="h-[600px]">
      <BioMonitor {latest} {heuristic} />
    </div>
  {:else}
    <!-- EXPERT MODE: DASHBOARD (Existing Layout) -->
    <!-- MAIN DASHBOARD GRID -->
    <div
      class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-pop-in border-8 border-[#558B2F] p-8 bg-[#2d1b18]"
    >
      <!-- LEFT COL: GRAPHS (2/3 width) -->
      <div class="lg:col-span-2 space-y-6 flex flex-col">
        <!-- KPI CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 z-40 relative">
          <!-- TEMP -->
          <div
            class="bg-[#3E2723] p-3 border-2 border-[#558B2F] relative group cursor-magnify hover:z-50 hover:border-[#C0CA33] transition-all"
          >
            <div
              class="text-[#8d6e63] text-xs font-bold uppercase mb-1 flex justify-between group-hover:text-[#C0CA33]"
            >
              Température <span>?</span>
            </div>
            <div class="text-2xl text-[#C0CA33] font-black">
              {latest?.temp_scd?.toFixed(1) || "--"}°C
            </div>
            <div class="absolute bottom-0 right-0 p-1 opacity-20 text-4xl">
              🌡️
            </div>
            <!-- TOOLTIP -->
            <div
              class="absolute top-full left-0 mt-2 w-48 bg-[#2d1b18] border border-[#C0CA33] p-2 text-[10px] text-[#FFF8E1] hidden group-hover:block z-[100] shadow-[0_0_15px_rgba(0,0,0,0.8)]"
            >
              <strong>Activateur Métabolique:</strong><br />
              40-60°C = Idéal pour les bactéries thermophiles (dégradation rapide).
              <br /><span class="text-xs text-[#558B2F]"
                >Si > 70°C : Risque d'incendie!</span
              >
            </div>
          </div>
          <!-- HUM -->
          <div
            class="bg-[#3E2723] p-3 border-2 border-[#558B2F] relative group cursor-magnify hover:z-50 hover:border-[#06b6d4] transition-all"
          >
            <div
              class="text-[#8d6e63] text-xs font-bold uppercase mb-1 flex justify-between group-hover:text-[#06b6d4]"
            >
              Humidité <span>?</span>
            </div>
            <div class="text-2xl text-[#06b6d4] font-black">
              {latest?.hum_scd?.toFixed(0) || "--"}%
            </div>
            <div class="absolute bottom-0 right-0 p-1 opacity-20 text-4xl">
              💧
            </div>
            <!-- TOOLTIP -->
            <div
              class="absolute top-full left-0 mt-2 w-48 bg-[#2d1b18] border border-[#06b6d4] p-2 text-[10px] text-[#FFF8E1] hidden group-hover:block z-[100] shadow-[0_0_15px_rgba(0,0,0,0.8)]"
            >
              <strong>Vecteur de vie:</strong><br />
              L'eau permet aux bactéries de se déplacer et de manger.
              <br /><span class="text-xs text-[#06b6d4]"
                >Cible: 50-60% (Comme une éponge essorée).</span
              >
            </div>
          </div>
          <!-- CO2 -->
          <div
            class="bg-[#3E2723] p-3 border-2 border-[#558B2F] relative group cursor-magnify hover:z-50 hover:border-[#22c55e] transition-all"
          >
            <div
              class="text-[#8d6e63] text-xs font-bold uppercase mb-1 flex justify-between group-hover:text-[#22c55e]"
            >
              CO2 (Activité) <span>?</span>
            </div>
            <div class="text-2xl text-[#22c55e] font-black">
              {latest?.co2 || "--"}
            </div>
            <div class="absolute bottom-0 right-0 p-1 opacity-20 text-4xl">
              💨
            </div>
            <!-- TOOLTIP -->
            <div
              class="absolute top-full left-0 mt-2 w-48 bg-[#2d1b18] border border-[#22c55e] p-2 text-[10px] text-[#FFF8E1] hidden group-hover:block z-[100] shadow-[0_0_15px_rgba(0,0,0,0.8)]"
            >
              <strong>Souffle du Compost:</strong><br />
              Produit par la respiration des bactéries.
              <br />High CO2 = Forte activité biologique.
            </div>
          </div>
          <!-- PHASE -->
          <div
            class="bg-[#3E2723] p-3 border-2 border-[#558B2F] relative group hover:border-orange-500 transition-all hover:z-50"
          >
            <div
              class="text-[#8d6e63] text-xs font-bold uppercase mb-1 group-hover:text-orange-500 transition-colors"
            >
              Phase Bio
            </div>
            <div
              class="text-xl font-black truncate {latest?.mq4 > 200
                ? 'text-red-500 animate-pulse'
                : 'text-[#f97316]'}"
            >
              {latest?.mq4 > 200 ? "⚠️ HYPOXIE" : indicators?.phase || "--"}
            </div>
          </div>
        </div>

        <!-- MAIN GRAPH (Temperature & Humidity) -->
        <div
          class="bg-[#3E2723] border-4 border-[#558B2F] p-4 min-h-[300px] flex-grow flex flex-col shadow-[8px_8px_0_rgba(0,0,0,0.5)] z-0"
        >
          <div class="flex justify-between items-center mb-4">
            <div class="flex flex-col">
              <h3 class="text-[#C0CA33] text-lg font-bold">THERMO-DYNAMIQUE</h3>
              <div class="flex gap-4 text-[10px] font-mono mt-1">
                <span class="text-[#7CB342] flex items-center gap-1">
                  <span class="w-3 h-1 bg-[#7CB342]"></span> RÉEL
                </span>
                <span class="text-[#06b6d4] flex items-center gap-1">
                  <span class="w-3 h-1 border-t border-dashed border-[#06b6d4]"
                  ></span> SIMULATION (JUMEAU)
                </span>
              </div>
            </div>
            {#if forecast}
              <div
                class="text-[#06b6d4] text-xs bg-[#06b6d4]/10 px-2 py-1 border border-[#06b6d4]"
              >
                🔮 IA Prédiction (+12h): {forecast.forecast?.[11]?.temp ||
                  "?"}°C
              </div>
            {/if}
          </div>

          <div
            class="flex-grow flex items-center justify-center bg-[#2d1b18] border-2 border-[#5d4037] relative overflow-hidden min-h-[220px]"
          >
            {#if chart.temp.length > 2}
              {@const minT = Math.min(...chart.temp) * 0.9}
              {@const maxT = Math.max(...chart.temp) * 1.1}
              <svg
                viewBox="0 0 400 150"
                class="w-full h-full p-2"
                preserveAspectRatio="none"
              >
                <!-- Grid Lines -->
                {#each [1, 2, 3, 4] as i}
                  <line
                    x1="0"
                    y1={30 * i}
                    x2="400"
                    y2={30 * i}
                    stroke="#5d4037"
                    stroke-width="1"
                    stroke-dasharray="4 4"
                    opacity="0.5"
                  />
                {/each}

                <!-- TEMP AREA -->
                <path
                  d={createPath(smoothData(chart.temp), 400, 150, minT, maxT)}
                  fill="none"
                  stroke="#7CB342"
                  stroke-width="3"
                  style="filter: drop-shadow(0 0 4px #7CB342);"
                />
                <!-- HUM LINE -->
                <path
                  d={createPath(smoothData(chart.hum), 400, 150, 0, 100)}
                  fill="none"
                  stroke="#06b6d4"
                  stroke-width="2"
                  stroke-dasharray="2 2"
                  opacity="0.8"
                />
              </svg>
            {:else}
              <div class="text-center text-[#8d6e63]">
                <div class="text-4xl mb-2">📉</div>
                <div>PAS ASSEZ DE DONNÉES</div>
                <div class="text-xs mt-2">
                  Allumez le moniteur pour commencer l'enregistrement
                </div>
              </div>
            {/if}
          </div>
          <div
            class="flex justify-between text-xs text-[#8d6e63] mt-2 font-mono"
          >
            <span>{timeRange === "24h" ? "-24h" : "Début"}</span>
            <span>Maintenant</span>
          </div>
        </div>

        <!-- GAS DYNAMICS -->
        <div
          class="bg-[#3E2723] border-4 border-[#558B2F] p-4 shadow-[8px_8px_0_rgba(0,0,0,0.5)]"
        >
          <div
            class="flex justify-between items-center mb-4 border-b-2 border-[#558B2F] pb-1"
          >
            <h3 class="text-[#C0CA33] text-lg font-bold">
              SIGNATURES GAZEUSES
            </h3>
            <div class="group relative">
              <button
                class="w-5 h-5 rounded-full border border-[#8d6e63] text-[#8d6e63] text-xs hover:bg-[#8d6e63] hover:text-[#3E2723] transition-colors"
                >?</button
              >
              <div
                class="absolute bottom-full right-0 w-64 p-3 bg-[#2d1b18] border border-[#5d4037] text-[10px] text-[#8d6e63] hidden group-hover:block z-20 shadow-xl mb-2"
              >
                <strong>Analyse Spectrale:</strong> <br />
                On observe les ratios entre le CO2 (Respiration), le NH3 (Azote)
                et le CH4 (Méthane) pour déterminer l'état de santé bactérien.
              </div>
            </div>
          </div>

          <div
            class="h-32 bg-[#2d1b18] border-2 border-[#5d4037] flex items-center justify-center"
          >
            {#if chart.co2.length > 2}
              {@const allGases = [...chart.co2, ...chart.nh3, ...chart.ch4]}
              {@const minG = Math.min(...allGases) * 0.9}
              {@const maxG = Math.max(...allGases) * 1.1}
              <svg
                viewBox="0 0 400 100"
                class="w-full h-full p-2"
                preserveAspectRatio="none"
              >
                <!-- CO2 -->
                <path
                  d={createPath(smoothData(chart.co2), 400, 100, minG, maxG)}
                  fill="none"
                  stroke="#22c55e"
                  stroke-width="2"
                />
                <path
                  d={createPath(smoothData(chart.nh3), 400, 100, minG, maxG)}
                  fill="none"
                  stroke="#a855f7"
                  stroke-width="2"
                />
                <path
                  d={createPath(smoothData(chart.ch4), 400, 100, minG, maxG)}
                  fill="none"
                  stroke="#f97316"
                  stroke-width="2"
                />
              </svg>
            {:else}
              <div class="text-[#8d6e63] text-xs">
                En attente de signature gaz...
              </div>
            {/if}
          </div>
          <div class="flex gap-4 mt-2 justify-center text-xs">
            <span class="text-[#22c55e] flex items-center gap-1"
              ><div class="w-2 h-2 bg-[#22c55e]"></div>
              CO2</span
            >
            <span class="text-[#a855f7] flex items-center gap-1"
              ><div class="w-2 h-2 bg-[#a855f7]"></div>
              NH3</span
            >
            <span class="text-[#f97316] flex items-center gap-1"
              ><div class="w-2 h-2 bg-[#f97316]"></div>
              CH4</span
            >
          </div>
        </div>
      </div>

      <!-- RIGHT COL: DIGITAL TWIN (1/3 width) -->
      <div class="space-y-6 flex flex-col h-full">
        <!-- HEURISTIC ENGINE CARD -->
        <RetroWindow title="DIGITAL TWIN V2" mode="inline" height="h-auto">
          <div class="flex flex-col items-center p-2 relative">
            <!-- EDUCATIONAL TOOLTIP -->
            <div class="absolute top-0 right-2 group z-10">
              <div
                class="cursor-magnify text-[#558B2F] hover:text-[#C0CA33] transition-colors"
              >
                [METHOD?]
              </div>
              <!-- POPUP -->
              <div
                class="hidden group-hover:block absolute top-6 right-0 w-64 bg-[#212121] border border-[#558B2F] p-3 shadow-[0_0_15px_rgba(33,33,33,0.9)] text-left z-50"
              >
                <h4
                  class="text-[#C0CA33] font-bold text-xs uppercase mb-2 border-b border-[#558B2F] pb-1"
                >
                  Sim-to-Real Engine
                </h4>
                <p class="text-[10px] text-[#8d6e63] mb-2 leading-tight">
                  Ce modèle n'est pas une simple formule. C'est une Intelligence
                  Artificielle (Transformer) entraînée sur <strong
                    class="text-white">100,000h</strong
                  > de données synthétiques.
                </p>
                <p class="text-[10px] text-[#8d6e63] leading-tight">
                  Il "imagine" les réactions biologiques invisibles (bactéries,
                  fraction anoxique) pour prédire les pannes 72h avant qu'elles
                  n'arrivent.
                </p>
              </div>
            </div>

            <!-- Status Light -->
            <div
              class="w-full flex justify-between items-center mb-4 px-2 mt-4"
            >
              <span class="text-xs text-[#8d6e63]">MOTEUR HEURISTIQUE</span>
              <div class="flex items-center gap-1">
                <div
                  class="w-2 h-2 rounded-full {heuristic.reliability === 'HIGH'
                    ? 'bg-green-500'
                    : 'bg-red-500 animate-pulse'}"
                ></div>
                <span class="text-[10px] uppercase"
                  >{heuristic.reliability} CONFIDENCE</span
                >
              </div>
            </div>

            <!-- BIG SCORE -->
            <div
              class="relative w-40 h-40 flex items-center justify-center border-8 {heuristic.score >
              70
                ? 'border-orange-500'
                : heuristic.score < 30
                  ? 'border-blue-500'
                  : 'border-green-500'} rounded-full bg-[#2d1b18]"
            >
              <div class="flex flex-col items-center">
                <span class="text-6xl font-black text-white"
                  >{heuristic.score}</span
                >
                <span class="text-xs text-[#8d6e63]">C/N INDEX</span>
              </div>
            </div>

            <!-- TEXT DIAGNOSIS -->
            <div class="mt-4 text-center">
              <div class="text-lg font-bold text-[#C0CA33]">
                {!heuristic.gate_label || heuristic.gate_label === "NO_DATA"
                  ? "CALIBRATION EN COURS..."
                  : heuristic.gate_label}
              </div>
              <div class="text-xs text-[#8d6e63] mt-1 max-w-[200px]">
                {heuristic.score < 40
                  ? "Trop d'azote detected (NH3 high). Risque d'odeurs."
                  : heuristic.score > 60
                    ? "Trop de carbone. Décomposition lente."
                    : "Équilibre parfait. Activité optimale."}
              </div>
            </div>

            <!-- ACTIONS RECOMMANDÉES -->
            <div class="w-full mt-6 space-y-2">
              <div
                class="text-xs text-[#8d6e63] uppercase border-b border-[#8d6e63] mb-2 pb-1"
              >
                Actions Requises
              </div>
              {#if heuristic.score < 40}
                <div
                  class="bg-orange-900/30 border border-orange-500 p-2 text-xs text-orange-200 flex items-center gap-2"
                >
                  <span>🍂</span> Ajouter matière sèche (carton/broys)
                </div>
              {:else if heuristic.score > 60}
                <div
                  class="bg-blue-900/30 border border-blue-500 p-2 text-xs text-blue-200 flex items-center gap-2"
                >
                  <span>🥬</span> Ajouter déchets verts (cuisine)
                </div>
              {:else}
                <div
                  class="bg-green-900/30 border border-green-500 p-2 text-xs text-green-200 flex items-center gap-2"
                >
                  <span>✨</span> Aucune action nécessaire
                </div>
              {/if}
            </div>
          </div>
        </RetroWindow>

        <!-- SOIL ANALYSIS (NPK) -->
        <div
          class="bg-[#3E2723] border-4 border-[#558B2F] p-4 shadow-[8px_8px_0_rgba(0,0,0,0.5)] flex-grow"
        >
          <h3
            class="text-[#C0CA33] text-sm font-bold border-b-2 border-[#558B2F] mb-3"
          >
            ANALYSE SOL (NPK)
          </h3>
          <div class="space-y-3">
            <!-- N -->
            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>AZOTE (N)</span> <span>{latest?.soil_n || 0} mg/kg</span>
              </div>
              <div class="w-full h-2 bg-[#2d1b18] rounded-full overflow-hidden">
                <div
                  class="h-full bg-green-500"
                  style="width: {Math.min(100, (latest?.soil_n || 0) / 2)}%"
                ></div>
              </div>
            </div>
            <!-- P -->
            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>PHOSPHORE (P)</span>
                <span>{latest?.soil_p || 0} mg/kg</span>
              </div>
              <div class="w-full h-2 bg-[#2d1b18] rounded-full overflow-hidden">
                <div
                  class="h-full bg-blue-500"
                  style="width: {Math.min(100, (latest?.soil_p || 0) / 2)}%"
                ></div>
              </div>
            </div>
            <!-- K -->
            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>POTASSIUM (K)</span>
                <span>{latest?.soil_k || 0} mg/kg</span>
              </div>
              <div class="w-full h-2 bg-[#2d1b18] rounded-full overflow-hidden">
                <div
                  class="h-full bg-orange-500"
                  style="width: {Math.min(100, (latest?.soil_k || 0) / 2)}%"
                ></div>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-2 mt-4">
            <div class="text-center bg-[#2d1b18] p-1 border border-[#5d4037]">
              <div class="text-[10px] text-[#8d6e63]">pH</div>
              <div class="font-bold text-[#C0CA33]">
                {latest?.soil_ph?.toFixed(1) || "-"}
              </div>
            </div>
            <div class="text-center bg-[#2d1b18] p-1 border border-[#5d4037]">
              <div class="text-[10px] text-[#8d6e63]">Conductivité</div>
              <div class="font-bold text-[#C0CA33]">
                {latest?.soil_ec || "-"}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- End Grid -->
  {/if}
</div>
