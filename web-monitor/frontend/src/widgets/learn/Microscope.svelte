<script>
    import { MICRO_DATA } from "../../lib/gameData.js";
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";

    let microView = "meso"; // 'psychro', 'meso', 'thermo'
    $: currentPhase = MICRO_DATA[microView];
</script>

<div class="h-full">
    <RetroWindow title="Microscope V2" mode="inline">
        <!-- Header Controls -->
        <div class="flex justify-center gap-4 mb-6 relative z-10">
            {#each Object.entries(MICRO_DATA) as [key, phase]}
                <button
                    class="px-4 py-2 border-b-4 font-bold text-xs uppercase transition-all
                               {microView === key
                        ? phase.borderColor +
                          ' ' +
                          phase.color +
                          ' text-black border-b-0 mt-1'
                        : 'border-gray-600 text-gray-400 hover:text-white'}"
                    on:click={() => (microView = key)}
                >
                    {phase.title.split(" ")[1]}
                </button>
            {/each}
        </div>

        <!-- Content -->
        <div class="relative z-10 min-h-[300px]">
            <h3 class="text-2xl text-center mb-2 font-bold text-[#C0CA33]">
                {currentPhase.title}
            </h3>
            <p
                class="text-center text-sm text-[#FFF8E1] mb-8 italic font-serif"
            >
                "{currentPhase.desc}"
            </p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                {#each currentPhase.creatures as creature}
                    <div
                        class="bg-[#2E3B20]/80 p-4 border-2 border-[#558B2F] rounded-none shadow-[4px_4px_0_rgba(0,0,0,0.2)] hover:border-[#7CB342] transition-colors group flex flex-col items-center text-center text-[#FFF8E1]"
                    >
                        <!-- Creature Icon (Animated) -->
                        <div
                            class="text-6xl mb-4 p-4 bg-white/5 rounded-full relative overflow-hidden group-hover:scale-110 transition-transform"
                        >
                            <div
                                class="animate-{creature.behavior === 'spin'
                                    ? 'spin-slow'
                                    : creature.behavior === 'pulse'
                                      ? 'pulse-step'
                                      : 'bounce-step'}"
                            >
                                {creature.icon}
                            </div>
                        </div>

                        <h4 class="font-bold text-lg text-[#C0CA33] mb-1">
                            {creature.name}
                        </h4>
                        <span
                            class="text-[10px] uppercase tracking-wider bg-[#558B2F] px-2 py-0.5 text-white mb-2"
                            >{creature.type}</span
                        >
                        <p class="text-xs text-[#DCEDC8] leading-relaxed">
                            {creature.desc}
                        </p>
                    </div>
                {/each}
            </div>
        </div>

        <!-- Background Effect -->
        <div
            class="absolute inset-0 opacity-10 pointer-events-none"
            style="background-image: radial-gradient({microView === 'thermo'
                ? '#F56565'
                : microView === 'meso'
                  ? '#48BB78'
                  : '#4299E1'} 1px, transparent 1px); background-size: 20px 20px;"
        ></div>
    </RetroWindow>
</div>

<style>
    /* CSS Animations for creatures */
    @keyframes spin-slow {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    @keyframes bounce-step {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    @keyframes pulse {
        0% {
            scale: 1;
        }
        50% {
            scale: 1.2;
        }
        100% {
            scale: 1;
        }
    }

    .animate-spin-slow {
        animation: spin-slow 20s steps(12) infinite;
    }
    .animate-bounce-step {
        animation: bounce-step 1s steps(4) infinite;
    }
    .animate-pulse-step {
        animation: pulse 1s steps(2) infinite;
    }
</style>
