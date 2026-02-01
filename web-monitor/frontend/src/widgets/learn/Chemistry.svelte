<script>
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";
    import { fly, scale } from "svelte/transition";

    // --- GAME STATE ---
    let cCount = 10; // Carbon (Browns)
    let nCount = 1; // Nitrogen (Greens)

    // Target: C/N between 25 and 30
    $: ratio = nCount > 0 ? (cCount / nCount).toFixed(1) : "∞";
    $: isStable = ratio >= 25 && ratio <= 30;
    $: status = getStatus(ratio);

    // Atoms for animation
    let atoms = [];

    function getStatus(r) {
        if (r == "∞") return "Trop de Carbone !";
        if (r > 35) return "Trop Sec / Lent (Manque d'Azote)";
        if (r < 20) return "Ça pue ! (Trop d'Azote -> Ammoniaque)";
        if (r >= 25 && r <= 30) return "PARFAIT ! (Équilibre d'Or)";
        return "Instable...";
    }

    // --- ACTIONS ---
    function addAtom(type) {
        if (type === "C") cCount += 5;
        if (type === "N") nCount += 1; // Nitrogen is potent!

        // Spawn visual atom
        const id = Math.random();
        atoms = [...atoms, { id, type, x: Math.random() * 80 + 10, y: 100 }];
        setTimeout(() => {
            atoms = atoms.filter((a) => a.id !== id);
        }, 2000);
    }

    function reset() {
        cCount = 0;
        nCount = 0;
    }

    // --- MOLECULE FACTS ---
    let selectedMolecule = null;
    const MOLECULES = [
        {
            formula: "CH₄",
            name: "Méthane",
            desc: "Produit si pas d'air (Anaérobie). Puissant gaz à effet de serre !",
            icon: "🟢",
        },
        {
            formula: "NH₃",
            name: "Ammoniac",
            desc: "L'odeur d'oeuf pourri/pipi ! Trop d'azote qui s'échappe.",
            icon: "🟡",
        },
        {
            formula: "CO₂",
            name: "Dioxyde de Carbone",
            desc: "Respiration normale des bactéries. C'est bon signe !",
            icon: "⚪",
        },
    ];
</script>

<div class="h-full font-pixel relative flex flex-col gap-4">
    <!-- TOP: BALANCE SCALE (ALCHEMIST POT) -->
    <RetroWindow title="L'Alchimiste du C/N" mode="inline" height="h-2/3">
        <div
            class="flex flex-col items-center justify-center h-full relative overflow-hidden bg-[#2E3B20]"
        >
            <!-- BACKGROUND LAB -->
            <div
                class="absolute inset-0 opacity-20 pointer-events-none text-6xl flex flex-wrap gap-8 p-8 justify-center"
            >
                <span>⚗️</span><span>🧪</span><span>🧬</span><span>🔬</span>
            </div>

            <!-- THE CAULDRON -->
            <div class="relative z-10 mt-8">
                <!-- Liquid Color matches status -->
                <div
                    class="w-48 h-48 rounded-full border-4 border-gray-600 bg-black relative overflow-hidden flex items-center justify-center shadow-xl"
                >
                    <div
                        class="absolute bottom-0 w-full transition-all duration-1000 ease-in-out opacity-80"
                        style="height: {Math.min(100, cCount + nCount * 5)}%; 
                                background-color: {ratio < 20
                            ? '#8BC34A'
                            : ratio > 35
                              ? '#795548'
                              : '#FFD700'}"
                    >
                        <!-- Bubbles -->
                        {#if cCount + nCount > 0}
                            <div
                                class="absolute w-full h-full animate-pulse opacity-50 bg-white/10"
                            ></div>
                        {/if}
                    </div>

                    <!-- RATIO DISPLAY CENTER -->
                    <div
                        class="z-20 text-center bg-black/50 p-2 rounded backdrop-blur-sm"
                    >
                        <div class="text-xs text-gray-300">RATIO C/N</div>
                        <div
                            class="text-4xl font-bold {isStable
                                ? 'text-yellow-400 animate-bounce'
                                : 'text-white'}"
                        >
                            {ratio}
                        </div>
                    </div>
                </div>

                <!-- Support -->
                <div
                    class="w-32 h-4 bg-gray-700 mx-auto mt-0 rounded-b-lg"
                ></div>
                <div
                    class="w-48 h-2 bg-red-900/50 mx-auto mt-2 rounded blur-sm animate-pulse"
                ></div>
                <!-- Fire -->
            </div>

            <!-- FEEDBACK TEXT -->
            <div
                class="mt-6 text-center z-10 bg-black/60 p-2 rounded border {isStable
                    ? 'border-yellow-500'
                    : 'border-gray-500'}"
            >
                <p
                    class="text-sm font-bold {isStable
                        ? 'text-yellow-300'
                        : 'text-white'}"
                >
                    {status}
                </p>
            </div>

            <!-- FLOATING ATOMS -->
            {#each atoms as atom (atom.id)}
                <div
                    out:scale
                    class="absolute text-xl font-bold transition-all duration-[2000ms] ease-out"
                    style="left: {atom.x}%; bottom: {atom.y}%; transform: translateY(-200px); color: {atom.type ===
                    'C'
                        ? '#8D6E63'
                        : '#AED581'}"
                >
                    {atom.type}
                </div>
            {/each}
        </div>
    </RetroWindow>

    <!-- BOTTOM: CONTROLS & INFO -->
    <div class="h-1/3 flex gap-4">
        <!-- INGREDIENTS -->
        <RetroWindow title="Ingrédients" mode="inline" width="w-1/2">
            <div class="flex justify-around items-center h-full p-4">
                <button
                    class="flex flex-col items-center gap-2 group"
                    on:click={() => addAtom("C")}
                >
                    <div
                        class="w-16 h-16 bg-[#5D4037] rounded border-4 border-[#3E2723] flex items-center justify-center text-3xl shadow-lg group-active:translate-y-1"
                    >
                        🍂
                    </div>
                    <div class="text-[10px] text-[#D7CCC8]">
                        CARBONE (Bruns)<br />+5 C
                    </div>
                </button>

                <div class="text-2xl text-gray-500">VS</div>

                <button
                    class="flex flex-col items-center gap-2 group"
                    on:click={() => addAtom("N")}
                >
                    <div
                        class="w-16 h-16 bg-[#7CB342] rounded border-4 border-[#558B2F] flex items-center justify-center text-3xl shadow-lg group-active:translate-y-1"
                    >
                        🥬
                    </div>
                    <div class="text-[10px] text-[#DCEDC8]">
                        AZOTE (Verts)<br />+1 N
                    </div>
                </button>
            </div>
            <div class="absolute top-2 right-2">
                <button
                    class="text-[10px] text-red-400 hover:underline"
                    on:click={reset}>Reset</button
                >
            </div>
        </RetroWindow>

        <!-- MOLECULE LIBRARY -->
        <RetroWindow title="Molécules Chimiques" mode="inline" width="w-1/2">
            <div class="flex flex-col gap-2 p-2 overflow-y-auto h-full">
                {#each MOLECULES as mol}
                    <div
                        class="flex items-center gap-3 bg-black/20 p-2 rounded border border-gray-700 hover:bg-white/5 cursor-help transition-colors"
                        title={mol.desc}
                    >
                        <div class="text-2xl">{mol.icon}</div>
                        <div>
                            <div class="font-bold text-xs text-white">
                                {mol.formula} - {mol.name}
                            </div>
                            <div class="text-[9px] text-gray-400 leading-tight">
                                {mol.desc}
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </RetroWindow>
    </div>
</div>
