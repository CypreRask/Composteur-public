<script>
  import { onMount } from "svelte";
  import Sky from "./Sky.svelte";
  import Surface from "./Surface.svelte";
  import SurfaceV2 from "./SurfaceV2.svelte";
  import Underground from "./Underground.svelte";
  import StageFrame from "./components/layout/StageFrame.svelte";
  import Hud from "./Hud.svelte";
  import LaboControls from "./LaboControls.svelte";
  import Totem from "./components/ecosystem/Totem.svelte"; // RESTORED
  import MicroscopeView from "./components/ecosystem/MicroscopeView.svelte"; // NEW
  import RetroWindow from "./components/uikit/RetroWindow.svelte"; // NEW
  import RetroButton from "./components/uikit/RetroButton.svelte"; // NEW
  import LearnView from "./LearnView.svelte"; // RESTORED
  import DataView from "./DataView.svelte"; // RESTORED
  import PhotosynthesisModule from "./components/ecosystem/tree/edu/PhotosynthesisModule.svelte"; // TREE MODULE (C3)
  import PhotosynthesisModuleAdvanced from "./components/ecosystem/tree/edu/PhotosynthesisModuleAdvanced.svelte"; // TREE MODULE (C3) - ADVANCED
  import PhotosynthesisC4 from "./components/ecosystem/tree/edu/PhotosynthesisC4.svelte"; // C4 MODULE
  import CirculationModule from "./components/ecosystem/tree/edu/CirculationModule.svelte"; // TREE MODULE (C3)
  import CirculationC4 from "./components/ecosystem/tree/edu/CirculationC4.svelte"; // C4 MODULE
  import SymbiosisModule from "./components/ecosystem/tree/edu/SymbiosisModule.svelte"; // TREE MODULE (C3)
  import SymbiosisC4 from "./components/ecosystem/tree/edu/SymbiosisC4.svelte"; // C4 MODULE
  import CellView from "./components/ecosystem/tree/edu/CellView.svelte"; // Level 2
  import FoliageView from "./components/ecosystem/tree/edu/FoliageView.svelte"; // Level 1.5
  import ChloroplastView from "./components/ecosystem/tree/edu/ChloroplastView.svelte"; // NEW: Deep Zoom Level 3
  import PhotosynthesisCAM from "./components/ecosystem/tree/edu/PhotosynthesisCAM.svelte"; // CAM MODULE

  // Mock Data
  const MOCK_DATA = {
    timestamp: new Date().toISOString(),
    temp_scd: 45.2,
    hum_scd: 68,
    co2: 1250,
    temp_aht: 18.5,
    hum_aht: 55,
    mq137: 120,
    soil_hum: 65,
    soil_temp: 42.0,
    soil_ph: 6.8,
    soil_n: 140,
    soil_p: 85,
    soil_k: 200,
  };

  let latest = MOCK_DATA;
  let weather = null;
  let history = [];

  // --- NAVIGATION STATE ---
  let activeTab = "monitor"; // 'monitor', 'data', 'learn'

  // --- GOD MODE / LABO INFRASTRUCTURE ---
  let mode = "MONITORING"; // 'MONITORING' | 'LABO'

  let laboState = {
    timestamp: new Date().toISOString(),
    soil_temp: 20,
    soil_hum: 50,
    soil_ph: 7.0,
    soil_n: 150,
    temp_scd: 22,
    co2: 400,
    cn_ratio: 25,
    oxygen: 100,
  };

  let fluxState = { carbon: false, nitrogen: false, water: false };

  $: displayData = mode === "MONITORING" ? latest : laboState;
  $: isNight = weather?.sys
    ? Date.now() / 1000 < weather.sys.sunrise ||
      Date.now() / 1000 > weather.sys.sunset
    : false;

  // --- WIDGET SYSTEM (Replacement for Tabs) ---
  let activeWidget = null; // 'foliage', 'trunk', 'roots', 'cah'

  function handleWidgetOpen(event) {
    activeWidget = event.detail.zone;
  }

  function closeWidget() {
    activeWidget = null;
  }

  // Fetch Logic (Simplified for brevity)
  async function fetchData() {
    try {
      const res = await fetch("http://localhost:8085/api/latest");
      if (res.ok) latest = await res.json();
    } catch (e) {
      console.log("Backend offline (Latest)");
    }

    try {
      const resW = await fetch("http://localhost:8085/api/weather");
      if (resW.ok) weather = await resW.json();
    } catch (e) {}
  }

  async function fetchHistory() {
    try {
      const res = await fetch("http://localhost:8085/api/history?limit=1000");
      if (res.ok) {
        history = await res.json();
        history.reverse(); // Backend sends DESC, Frontend needs ASC (Oldest -> Newest)
        console.log("[DATA] History loaded:", history.length, "records");
      }
    } catch (e) {
      console.log("Backend offline (History)");
    }
  }

  onMount(() => {
    fetchData();
    fetchHistory();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  });
</script>

<main
  class="h-screen w-screen overflow-hidden flex flex-col font-pixel bg-black text-white relative"
>
  <!-- HEADER (Minimalist) -->
  <div
    class="h-10 bg-[#2D3748] border-b-4 border-[#1A202C] flex items-center px-2 sm:px-4 justify-between z-50 shrink-0 overflow-hidden"
  >
    <div
      class="text-xs text-gray-400 uppercase tracking-widest flex items-center gap-2 sm:gap-4 overflow-hidden"
    >
      <span class="hidden sm:inline whitespace-nowrap">SmartCompost</span>

      <!-- NAVIGATION TABS -->
      <div
        class="flex gap-1 sm:gap-2 ml-0 sm:ml-8 overflow-x-auto no-scrollbar mask-gradient"
      >
        <RetroButton
          small
          active={activeTab === "monitor"}
          color="blue"
          on:click={() => (activeTab = "monitor")}
          label="MONITOR"
        />
        <RetroButton
          small
          active={activeTab === "data"}
          color="blue"
          on:click={() => (activeTab = "data")}
          label="DATA"
        />
        <RetroButton
          small
          active={activeTab === "learn"}
          color="blue"
          on:click={() => (activeTab = "learn")}
          label="LEARN"
        />
      </div>
    </div>
  </div>

  <!-- CONTENT AREA -->
  {#if activeTab === "monitor"}
    <!-- MAIN SCENE (Unifed Surface + Underground) -->
    <div class="flex-1 relative flex flex-col pointer-events-none">
      <!-- Scene is background -->

      <!-- SKY -->
      <div class="h-[45%] w-full relative z-0 pointer-events-auto">
        <Sky weatherData={weather} />
        <!-- Legacy HUD hidden or kept for details? Kept for now -->
        <Hud data={displayData} />

        <!-- GOD MODE SWITCH (Overlay) -->
        <div
          class="absolute top-4 right-4 z-50 flex bg-black/80 p-1 border border-white/20 rounded shadow-lg backdrop-blur-sm"
        >
          <RetroButton
            small
            active={mode === "MONITORING"}
            color="green"
            on:click={() => (mode = "MONITORING")}
            label="LIVE"
          />
          <div class="w-1"></div>
          <RetroButton
            small
            active={mode === "LABO"}
            color="gray"
            on:click={() => (mode = "LABO")}
            label="LABO"
          />
        </div>
      </div>

      <!-- SURFACE LINE -->
      <div
        class="h-8 bg-terra-grass border-b-4 border-terra-deep w-full relative z-10 shrink-0 pointer-events-auto"
      >
        <div class="absolute bottom-0 w-full flex justify-center">
          <div class="origin-bottom scale-75 md:scale-100">
            <Surface
              data={displayData}
              {weather}
              on:openMicroscope={() => (activeWidget = "microscope")}
              on:openHardware={() => (activeWidget = "hardware")}
              on:inspectWaste={() => (activeWidget = "waste")}
              on:inspectBiology={() => (activeWidget = "microscope")}
              on:openPhotosynthesis={() => (activeWidget = "foliage")}
              on:openCirculation={() => (activeWidget = "circulation")}
              on:openRoots={() => (activeWidget = "roots")}
              on:openFoliageC4={() => (activeWidget = "foliage_c4")}
              on:openCirculationC4={() => (activeWidget = "circulation_c4")}
              on:openSymbiosisC4={() => (activeWidget = "symbiosis_c4")}
              on:openCAM={() => (activeWidget = "foliage_cam")}
              on:openC4={() => (activeWidget = "foliage_c4")}
            />
          </div>
        </div>
      </div>

      <!-- UNDERGROUND -->
      <div
        class="flex-1 relative overflow-hidden pointer-events-auto bg-[#3E2723]"
      >
        <Underground data={displayData} {weather} {fluxState} />
      </div>

      <!-- TOTEM INTERFACE REMOVED -->

      <!-- WIDGET OVERLAY (Blocking/Modal) -->
      {#if activeWidget}
        <div
          class="fixed inset-0 z-[100] flex items-center justify-center pointer-events-auto bg-black/50 backdrop-blur-sm p-4"
          on:click|self={closeWidget}
          on:keydown={(e) => e.key === "Escape" && closeWidget()}
          role="button"
          tabindex="0"
        >
          <RetroWindow
            title={activeWidget === "hardware"
              ? "HARDWARE_SCHEMATIC"
              : activeWidget.toUpperCase()}
            on:close={closeWidget}
            color={activeWidget === "photosynthesis" ? "green" : "blue"}
            mode="inline"
            width="w-full max-w-2xl"
            closable={true}
          >
            <div class="text-black">
              {#if activeWidget === "cell"}
                <div class="h-[500px] w-full">
                  <CellView
                    on:close={closeWidget}
                    on:openChloroplast={() => (activeWidget = "chloroplast")}
                  />
                </div>
              {:else if activeWidget === "chloroplast"}
                <div class="h-[500px] w-full">
                  <ChloroplastView
                    {weather}
                    on:close={() => (activeWidget = "cell")}
                    on:openThylakoid={() => (activeWidget = "photosynthesis")}
                  />
                </div>
              {:else if activeWidget === "photosynthesis"}
                <PhotosynthesisModuleAdvanced
                  on:back={() => (activeWidget = "chloroplast")}
                />
              {:else if activeWidget === "photosynthesis_c4"}
                <div class="h-[500px] w-full">
                  <PhotosynthesisC4
                    on:back={() => (activeWidget = "foliage_c4")}
                  />
                </div>
              {:else if activeWidget === "circulation"}
                <!-- EDUCATIONAL MODULE: CIRCULATION (C3) -->
                <div class="h-[500px] w-full">
                  <CirculationModule />
                </div>
              {:else if activeWidget === "circulation_c4"}
                <!-- EDUCATIONAL MODULE: CIRCULATION (C4) -->
                <div class="h-[500px] w-full">
                  <CirculationC4 />
                </div>
              {:else if activeWidget === "roots"}
                <!-- EDUCATIONAL MODULE: SYMBIOSIS (C3) -->
                <div class="h-[500px] w-full">
                  <SymbiosisModule />
                </div>
              {:else if activeWidget === "symbiosis_c4"}
                <div class="h-[500px] w-full">
                  <SymbiosisC4 />
                </div>
              {:else if activeWidget === "foliage"}
                <div class="h-[500px] w-full">
                  <FoliageView
                    plantType="C3"
                    showToggle={false}
                    on:close={closeWidget}
                    on:openCell={() => (activeWidget = "cell")}
                  />
                </div>
              {:else if activeWidget === "foliage_c4"}
                <div class="h-[500px] w-full">
                  <FoliageView
                    plantType="C4"
                    showToggle={false}
                    on:close={closeWidget}
                    on:openC4={() => (activeWidget = "photosynthesis_c4")}
                  />
                </div>
              {:else if activeWidget === "foliage_cam"}
                <div class="h-[500px] w-full">
                  <FoliageView
                    plantType="CAM"
                    showToggle={false}
                    on:close={closeWidget}
                    on:openCAM={() => (activeWidget = "photosynthesis_cam")}
                  />
                </div>
              {:else if activeWidget === "photosynthesis_cam"}
                <div class="h-[500px] w-full">
                  <PhotosynthesisCAM
                    on:back={() => (activeWidget = "foliage_cam")}
                  />
                </div>
              {:else if activeWidget === "microscope"}
                <!-- BIOLOGY INSPECTION -->
                <h3 class="font-bold mb-2 text-lime-400">
                  🔬 Analyse Microbiologique
                </h3>
                <div
                  class="h-64 w-full bg-black border border-green-800 relative overflow-hidden rounded"
                >
                  <MicroscopeView
                    temp={displayData.temp_scd}
                    humidity={displayData.hum_scd}
                  />
                </div>
                <p
                  class="text-[10px] text-green-700 mt-2 text-center animate-pulse"
                >
                  > CLIQUEZ SUR L'ÉCRAN POUR DÉTAILS ESPIÈCES
                </p>
              {:else if activeWidget === "waste"}
                <!-- WASTE INSPECTION -->
                <div class="p-2 font-pixel">
                  <h3 class="font-bold mb-2 text-orange-600">
                    🍂 Décomposition des Déchets
                  </h3>
                  <div class="flex gap-4">
                    <!-- Animation -->
                    <div
                      class="w-32 h-32 bg-[#5D4037] border-2 border-orange-900 relative overflow-hidden flex items-center justify-center"
                    >
                      <!-- Leaf -->
                      <div
                        class="w-8 h-8 bg-green-500 rounded-tr-xl rounded-bl-xl absolute animate-pulse"
                      ></div>
                      <!-- Eating Worms -->
                      <div
                        class="absolute w-2 h-2 bg-pink-400 top-1/2 left-1/2 -translate-x-4 animate-bounce"
                      ></div>
                      <div
                        class="absolute w-2 h-2 bg-pink-400 top-1/2 left-1/2 translate-x-4 animate-bounce delay-75"
                      ></div>
                    </div>
                    <!-- Info -->
                    <div class="flex-1 text-[10px]">
                      <p class="mb-2">
                        Les <strong>Matières Vertes</strong> (Azote) et
                        <strong>Brunes</strong> (Carbone) sont mélangées ici.
                      </p>
                      <p>
                        Ratio C/N Actuel: <span class="text-blue-600 font-bold"
                          >{laboState.cn_ratio}:1</span
                        >
                      </p>
                      <p class="mt-2 italic opacity-70">
                        "C'est le carburant du réacteur !"
                      </p>
                    </div>
                  </div>
                </div>
              {:else if activeWidget === "hardware"}
                <!-- HARDWARE SCHEMATIC -->
                <div
                  class="bg-[#1a202c] p-4 font-mono text-xs text-green-400 border border-green-800 rounded relative"
                >
                  <h3
                    class="text-center font-bold mb-4 border-b border-green-700 pb-2"
                  >
                    SCHÉMA ÉLECTRONIQUE (V2)
                  </h3>

                  <div class="flex flex-col gap-6 items-center">
                    <!-- SENSORS -->
                    <div class="flex gap-4">
                      <div
                        class="border border-blue-500 p-2 text-blue-300 text-center rounded"
                      >
                        [DS18B20]<br /><span class="text-[8px] opacity-70"
                          >Température (Tige)</span
                        >
                      </div>
                      <div
                        class="border border-blue-500 p-2 text-blue-300 text-center rounded"
                      >
                        [CAPACITIF]<br /><span class="text-[8px] opacity-70"
                          >Humidité (Sol)</span
                        >
                      </div>
                    </div>

                    <!-- WIRES -->
                    <div class="h-4 w-[1px] bg-green-900"></div>

                    <!-- MCU -->
                    <div
                      class="border-2 border-green-500 p-3 bg-green-900/20 rounded shadow-lg text-center relative w-full"
                    >
                      <span
                        class="absolute -top-2 left-2 bg-[#1a202c] px-1 text-[8px] text-green-300"
                        >ESP32</span
                      >
                      <div class="font-bold text-lg">Cerveau</div>
                      <div class="text-[8px]">WiFi + Traitement</div>
                    </div>

                    <!-- WIRE -->
                    <div class="h-4 w-[1px] bg-green-900 animate-pulse"></div>

                    <!-- COMMS -->
                    <div
                      class="border border-orange-500 p-2 text-orange-300 text-center rounded w-full flex items-center justify-between px-4"
                    >
                      <span>📡 LoRaWAN</span>
                      <span class="text-[8px] opacity-70"
                        >Transmission Longue Portée</span
                      >
                    </div>
                  </div>
                </div>
              {/if}
            </div>
          </RetroWindow>
        </div>
      {/if}
    </div>

    <!-- GOD MODE CONTROLS -->
    {#if mode === "LABO"}
      <LaboControls bind:state={laboState} bind:flux={fluxState} />
    {/if}
  {:else if activeTab === "data"}
    <div class="flex-1 bg-gray-900 overflow-auto">
      <DataView data={history} />
    </div>
  {:else if activeTab === "learn"}
    <div class="flex-1 bg-gray-900 overflow-auto">
      <LearnView />
    </div>
  {/if}
</main>
