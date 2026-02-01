<script>
    export let state; // Bound to laboState in App.svelte
    export let flux; // Bound to fluxState in App.svelte

    // Actions instantanées
    function triggerRain() {
        // Simule une pluie (Met à jour le state global ou dispatch un event)
        // Pour l'instant, on toggle juste une prop si nécessaire,
        // ou on laisse l'utilisateur gérer via le slider humidité.
        // Mais pour "Le Déluge", on peut forcer l'humidité à 100% temporairement ?
        state.soil_hum = 100;
    }

    function Aerate() {
        state.oxygen = 100;
        state.temp_scd = Math.max(state.temp_scd, 40); // Ca chauffe quand on aère
    }
</script>

<div
    class="fixed bottom-0 left-0 w-full bg-[#1A202C]/90 border-t-4 border-[#2D3748] p-4 font-pixel z-50 shadow-[0_-5px_20px_rgba(0,0,0,0.5)]"
>
    <div
        class="max-w-4xl mx-auto flex flex-col md:flex-row gap-6 items-center justify-between"
    >
        <!-- TITLE -->
        <div class="flex flex-col items-center shrink-0">
            <div class="text-2xl">🧪</div>
            <div class="font-bold text-purple-400">LABO</div>
            <div class="text-[10px] text-gray-400 uppercase tracking-widest">
                God Mode
            </div>
        </div>

        <!-- SLIDERS -->
        <div class="flex items-center gap-6 flex-1 w-full md:w-auto">
            <!-- Temperature -->
            <div class="flex flex-col gap-1 flex-1">
                <div class="flex justify-between text-xs">
                    <span class="text-red-300">Température</span>
                    <span class="font-bold">{state.temp_scd.toFixed(1)}°C</span>
                </div>
                <input
                    type="range"
                    min="-10"
                    max="80"
                    step="0.5"
                    bind:value={state.temp_scd}
                    class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-red-500"
                />
                <div class="flex justify-between text-[8px] text-gray-500">
                    <span>❄️ Gel</span>
                    <span>🔥 Surchauffe</span>
                </div>
            </div>

            <!-- Humidity -->
            <div class="flex flex-col gap-1 flex-1">
                <div class="flex justify-between text-xs">
                    <span class="text-blue-300">Humidité</span>
                    <span class="font-bold">{state.soil_hum.toFixed(0)}%</span>
                </div>
                <input
                    type="range"
                    min="0"
                    max="100"
                    step="1"
                    bind:value={state.soil_hum}
                    class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
                <div class="flex justify-between text-[8px] text-gray-500">
                    <span>🍂 Sec</span>
                    <span>🌊 Noyé</span>
                </div>
            </div>

            <!-- C/N Ratio -->
            <div class="flex flex-col gap-1 flex-1">
                <div class="flex justify-between text-xs">
                    <span class="text-green-300">Équilibre C/N</span>
                    <span class="font-bold">{state.cn_ratio}</span>
                </div>
                <input
                    type="range"
                    min="10"
                    max="60"
                    step="1"
                    bind:value={state.cn_ratio}
                    class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-green-500"
                />
                <div class="flex justify-between text-[8px] text-gray-500">
                    <span>🥗 Azote</span>
                    <span>🪵 Carbone</span>
                </div>
            </div>
        </div>

        <!-- ACTIONS -->
        <div class="flex gap-2 shrink-0">
            <button
                class="bg-blue-900/50 hover:bg-blue-800 border-2 border-blue-500 p-2 rounded-lg transition-transform active:scale-95 flex flex-col items-center w-16"
                on:click={triggerRain}
            >
                <span class="text-xl">🌧️</span>
                <span class="text-[8px] font-bold">Déluge</span>
            </button>
            <button
                class="bg-orange-900/50 hover:bg-orange-800 border-2 border-orange-500 p-2 rounded-lg transition-transform active:scale-95 flex flex-col items-center w-16"
                on:click={Aerate}
            >
                <span class="text-xl">🚜</span>
                <span class="text-[8px] font-bold">Aérer</span>
            </button>
        </div>

        <!-- FLUX TOGGLES (Layers) -->
        <div
            class="flex gap-2 shrink-0 border-l border-gray-600 pl-4 items-center"
        >
            <div class="flex flex-col gap-1">
                <button
                    class="px-2 py-1 text-[10px] border border-gray-500 rounded {flux.carbon
                        ? 'bg-gray-200 text-black font-bold'
                        : 'text-gray-400 hover:text-white'}"
                    on:click={() => (flux.carbon = !flux.carbon)}
                >
                    Cycle C
                </button>
                <button
                    class="px-2 py-1 text-[10px] border border-blue-500 rounded {flux.nitrogen
                        ? 'bg-blue-200 text-blue-900 font-bold'
                        : 'text-blue-400 hover:text-white'}"
                    on:click={() => (flux.nitrogen = !flux.nitrogen)}
                >
                    Cycle N
                </button>
                <button
                    class="px-2 py-1 text-[10px] border border-cyan-500 rounded {flux.water
                        ? 'bg-cyan-200 text-cyan-900 font-bold'
                        : 'text-cyan-400 hover:text-white'}"
                    on:click={() => (flux.water = !flux.water)}
                >
                    Cycle H2O
                </button>
            </div>
        </div>
    </div>
</div>
