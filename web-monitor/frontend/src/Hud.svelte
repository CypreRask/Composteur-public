<script>
    import {
        xp,
        getRank,
        getNextRank,
        getProgress,
        showLevelUp,
    } from "./lib/progression.js";
    import { fly } from "svelte/transition";

    export let data = null;

    // Default mock
    $: safeData = data || {
        soil_n: 0,
        soil_p: 0,
        soil_k: 0,
        soil_ph: 0,
        soil_ec: 0,
        mq137: 0,
        mq4: 0,
        mq7: 0,
        soil_temp: 20, // Added missing props
        soil_hum: 50,
    };

    let minimized = false;
    function toggle() {
        minimized = !minimized;
    }

    // Reactive Progression
    $: currentXp = $xp;
    $: rank = getRank(currentXp);
    $: nextRank = getNextRank(currentXp);
    $: progress = getProgress(currentXp);
</script>

<div class="absolute top-20 right-4 z-50 flex flex-col items-end">
    <!-- Bouton Toggle (Sac à dos) -->
    <button
        on:click={toggle}
        class="bg-[#2D3748] border-4 border-white text-white p-2 mb-2 font-pixel text-xs hover:bg-[#4A5568] transition-colors shadow-lg active:translate-y-1"
    >
        {minimized ? "🎒 INVENTAIRE" : "🔽 MASQUER"}
    </button>

    {#if !minimized}
        <!-- Panneau Inventaire Style RPG -->
        <div
            class="bg-[#1A202C] border-4 border-[#4A5568] p-1 shadow-[8px_8px_0_rgba(0,0,0,0.5)] w-80 font-pixel relative"
        >
            <!-- LEVEL UP NOTIFICATION -->
            {#if $showLevelUp}
                <div
                    in:fly={{ y: 20 }}
                    class="absolute -top-16 left-0 right-0 bg-yellow-400 text-black border-4 border-white p-2 text-center text-xs font-bold animate-bounce z-50"
                >
                    ⭐ NIVEAU SUPÉRIEUR ! ⭐
                </div>
            {/if}

            <!-- PLAYER PROFILE BANNER -->
            <div
                class="bg-[#2D3748] mb-1 p-2 border-b-2 border-[#4A5568] flex items-center gap-3"
            >
                <div
                    class="w-12 h-12 bg-[#1A202C] border-2 border-[#CBD5E0] flex items-center justify-center text-2xl relative"
                >
                    {rank.icon}
                    <div
                        class="absolute -bottom-2 -right-2 bg-yellow-500 text-black text-[8px] px-1 rounded border border-white font-bold"
                    >
                        Lvl {rank.level}
                    </div>
                </div>
                <div class="flex-1">
                    <div class="text-[#E2E8F0] text-xs font-bold">
                        {rank.name}
                    </div>

                    <!-- XP BAR -->
                    <div
                        class="w-full bg-[#1A202C] h-2 mt-1 border border-[#4A5568] relative"
                    >
                        <div
                            class="h-full bg-gradient-to-r from-blue-400 to-purple-500 transition-all duration-500"
                            style="width: {progress}%"
                        ></div>
                    </div>
                    <div
                        class="flex justify-between text-[8px] text-gray-400 mt-0.5"
                    >
                        <span>{currentXp} XP</span>
                        <span>{nextRank ? nextRank.minXp + " XP" : "MAX"}</span>
                    </div>
                </div>
            </div>

            <div class="bg-[#2D3748] p-3">
                <h2
                    class="text-[#A0AEC0] border-b-2 border-[#4A5568] pb-2 mb-3 text-[10px] uppercase tracking-widest"
                >
                    Inventaire du Sol
                </h2>

                <div class="grid grid-cols-2 gap-2 mb-4">
                    <!-- NPK Slots -->
                    <div
                        class="bg-[#1A202C] p-2 border-4 border-[#4A5568] flex items-center gap-2 relative group hover:border-emerald-500 transition-colors shadow-none"
                    >
                        <!-- N Icon (Pixel Art CSS) -->
                        <div class="w-6 h-6 relative shrink-0">
                            <div
                                class="absolute inset-0 bg-emerald-500 clip-pixel-n"
                            ></div>
                            <!-- Simplified for quick render: Square Block -->
                            <div
                                class="w-full h-full bg-emerald-900 border-2 border-emerald-500 flex items-center justify-center text-xs font-bold text-emerald-400"
                            >
                                N
                            </div>
                        </div>
                        <div>
                            <div
                                class="text-[8px] text-emerald-400 font-bold tracking-widest"
                            >
                                AZOTE
                            </div>
                            <div class="text-xs text-white bg-black/20 px-1">
                                {safeData.soil_n}
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-[#1A202C] p-2 border-4 border-[#4A5568] flex items-center gap-2 hover:border-amber-500 transition-colors"
                    >
                        <div
                            class="w-6 h-6 bg-amber-900 border-2 border-amber-500 flex items-center justify-center text-xs font-bold text-amber-400"
                        >
                            P
                        </div>
                        <div>
                            <div
                                class="text-[8px] text-amber-400 font-bold tracking-widest"
                            >
                                PHOS
                            </div>
                            <div class="text-xs text-white bg-black/20 px-1">
                                {safeData.soil_p}
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-[#1A202C] p-2 border-4 border-[#4A5568] flex items-center gap-2 hover:border-purple-500 transition-colors"
                    >
                        <div
                            class="w-6 h-6 bg-purple-900 border-2 border-purple-500 flex items-center justify-center text-xs font-bold text-purple-400"
                        >
                            K
                        </div>
                        <div>
                            <div
                                class="text-[8px] text-purple-400 font-bold tracking-widest"
                            >
                                POTAS
                            </div>
                            <div class="text-xs text-white bg-black/20 px-1">
                                {safeData.soil_k}
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-[#1A202C] p-2 border-4 border-[#4A5568] flex items-center gap-2 hover:border-blue-400 transition-colors"
                    >
                        <div
                            class="w-6 h-6 bg-blue-900 border-2 border-blue-400 flex items-center justify-center text-[8px] font-bold text-blue-300"
                        >
                            pH
                        </div>
                        <div>
                            <div
                                class="text-[8px] text-blue-300 font-bold tracking-widest"
                            >
                                pH/EC
                            </div>
                            <div
                                class="text-[10px] text-white bg-black/20 px-1"
                            >
                                {safeData.soil_ph}/{safeData.soil_ec}
                            </div>
                        </div>
                    </div>

                    <!-- NEW: Soil Temp & Hum -->
                    <div
                        class="bg-[#1A202C] p-2 border-4 border-[#4A5568] flex items-center gap-2 hover:border-orange-600 transition-colors col-span-2"
                    >
                        <div
                            class="w-6 h-6 bg-orange-900 border-2 border-orange-600 flex items-center justify-center text-[10px] font-bold text-orange-300"
                        >
                            T°
                        </div>
                        <div class="flex justify-between w-full">
                            <div>
                                <div
                                    class="text-[8px] text-orange-300 font-bold tracking-widest"
                                >
                                    TEMP
                                </div>
                                <div
                                    class="text-[10px] text-white bg-black/20 px-1"
                                >
                                    {safeData.soil_temp}°C
                                </div>
                            </div>
                            <div class="text-right">
                                <div
                                    class="text-[8px] text-blue-300 font-bold tracking-widest"
                                >
                                    EAU
                                </div>
                                <div
                                    class="text-[10px] text-white bg-black/20 px-1"
                                >
                                    {safeData.soil_hum}%
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Section Gaz (Danger) -->
                <div class="border-t-2 border-[#4A5568] pt-2">
                    <h3 class="text-[#A0AEC0] text-[10px] mb-2 uppercase">
                        Détecteur Gaz
                    </h3>
                    <div class="space-y-1">
                        <div
                            class="flex justify-between items-center bg-[#1A202C] px-2 py-1 border border-red-900/50"
                        >
                            <span class="text-[8px] text-red-400"
                                >NH3 (Odeur)</span
                            >
                            <span
                                class="text-[10px] {safeData.mq137 > 100
                                    ? 'text-red-500 animate-pulse'
                                    : 'text-gray-400'}">{safeData.mq137}</span
                            >
                        </div>
                        <div
                            class="flex justify-between items-center bg-[#1A202C] px-2 py-1 border border-orange-900/50"
                        >
                            <span class="text-[8px] text-orange-400"
                                >CH4 (Méthane)</span
                            >
                            <span
                                class="text-[10px] {safeData.mq4 > 100
                                    ? 'text-orange-500 animate-pulse'
                                    : 'text-gray-400'}">{safeData.mq4}</span
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>
