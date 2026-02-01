<script>
    import { createEventDispatcher, onMount } from "svelte";
    import { LEARNING_PATH } from "../../lib/learningPath.js";

    const dispatch = createEventDispatcher();

    // State
    let progress = {}; // { 'intro_1': { status: 'completed', score: 0 } }
    let pathNodes = [];

    // Load Progress
    onMount(() => {
        const saved = localStorage.getItem("compost_progress");
        if (saved) {
            try {
                progress = JSON.parse(saved);
            } catch (e) {
                console.error("Save corrupt", e);
            }
        } else {
            // Default: Unlock first
            progress = { [LEARNING_PATH[0].id]: { status: "unlocked" } };
            saveProgress();
        }
        updatePathState();
    });

    function saveProgress() {
        localStorage.setItem("compost_progress", JSON.stringify(progress));
    }

    function updatePathState() {
        let previousCompleted = true; // First node always technically "previous completed"

        pathNodes = LEARNING_PATH.map((node, index) => {
            let state = progress[node.id] || {};
            let status = state.status || "locked";

            // Logic: Unlock if previous is completed
            if (status === "locked" && previousCompleted) {
                status = "unlocked";
                // Auto-save unlock
                progress[node.id] = { status: "unlocked" };
                saveProgress();
            }

            if (status !== "completed") previousCompleted = false;

            return { ...node, status };
        });
    }

    function handleNodeClick(node) {
        if (node.status === "locked") return;
        dispatch("select", node);
    }

    // Export helper to mark completion from parent
    // Export helper to mark completion from parent
    export function completeNode(id, score = 0) {
        console.log("PathMap: Completing node", id, score);
        progress[id] = { status: "completed", score };
        progress = { ...progress }; // Force reactivity
        saveProgress();
        updatePathState();
    }
</script>

<div
    class="w-full h-full bg-[#1A100E] p-4 font-pixel flex flex-col items-center overflow-y-auto"
>
    <h2
        class="text-2xl text-[#C0CA33] mb-8 font-bold uppercase tracking-widest text-center"
    >
        🗺️ Le Sentier du Maître
    </h2>

    <div class="relative w-full max-w-2xl flex flex-col gap-0 pb-12">
        <!-- CENTRAL LINE -->
        <div
            class="absolute left-1/2 -translate-x-1/2 top-4 bottom-4 w-2 bg-[#3E2723] rounded"
        ></div>

        {#each pathNodes as node, i}
            <!-- NODE ITEM WRAPPER -->
            <div
                class="relative w-full flex {i % 2 === 0
                    ? 'justify-start'
                    : 'justify-end'} mb-8"
            >
                <!-- CONNECTION LINE TO CENTER (Horizontal) -->
                <div
                    class="absolute top-1/2 h-1 bg-[#3E2723] z-0
                    {i % 2 === 0
                        ? 'right-1/2 w-[10%] translate-x-2'
                        : 'left-1/2 w-[10%] -translate-x-2'}"
                ></div>

                <button
                    class="relative w-[45%] group transition-all duration-300 disabled:opacity-50 disabled:grayscale flex flex-col
                    {i % 2 === 0
                        ? 'items-end text-right pr-8'
                        : 'items-start text-left pl-8'}"
                    disabled={node.status === "locked"}
                    on:click={() => handleNodeClick(node)}
                >
                    <!-- CENTER ICON BUBBLE -->
                    <div
                        class="absolute top-1/2 -translate-y-1/2 w-16 h-16 rounded-full border-4 flex items-center justify-center z-20 transition-all duration-300 shadow-xl
                        {i % 2 === 0
                            ? '-right-[5.5rem] lg:-right-[6.5rem]'
                            : '-left-[5.5rem] lg:-left-[6.5rem]'}
                        {node.status === 'completed'
                            ? 'bg-[#558B2F] border-[#C0CA33] text-white scale-100'
                            : node.status === 'unlocked'
                              ? 'bg-[#FF6F00] border-white animate-pulse text-white scale-110'
                              : 'bg-[#3E2723] border-[#5D4037] text-gray-500 scale-90'}
                    "
                    >
                        {#if node.status === "locked"}
                            <span class="text-2xl">🔒</span>
                        {:else if node.status === "completed"}
                            <span class="text-2xl">✅</span>
                        {:else if node.type === "theory"}
                            <span class="text-2xl">📘</span>
                        {:else}
                            <span class="text-2xl">🎮</span>
                        {/if}
                    </div>

                    <!-- CARD -->
                    <div
                        class="w-full bg-[#2E3B20] border-2 border-[#558B2F] rounded p-4 shadow-lg group-hover:bg-[#3E4C2F] group-hover:scale-[1.02] transition-all relative overflow-hidden"
                    >
                        {#if node.status === "locked"}
                            <div
                                class="absolute inset-0 bg-black/60 z-10"
                            ></div>
                        {/if}

                        <div
                            class="flex justify-between items-start mb-1 {i %
                                2 ===
                            0
                                ? 'flex-row-reverse'
                                : ''}"
                        >
                            <span
                                class="text-[10px] uppercase font-bold tracking-wider
                                {node.type === 'game'
                                    ? 'text-orange-400'
                                    : 'text-blue-400'}"
                            >
                                {node.type === "game" ? "DÉFI" : "SAVOIR"}
                            </span>
                            <div class="text-[10px] text-gray-400 font-mono">
                                {node.xp} XP
                            </div>
                        </div>

                        <h3
                            class="text-lg text-white font-bold leading-tight mb-1"
                        >
                            {node.title}
                        </h3>
                        <p class="text-xs text-[#C0CA33] mb-2">
                            {node.subtitle}
                        </p>
                        <p class="text-[10px] text-gray-300 leading-snug">
                            {node.desc}
                        </p>

                        {#if node.status === "unlocked"}
                            <div
                                class="absolute bottom-2 text-[#C0CA33] opacity-0 group-hover:opacity-100 transition-opacity animate-bounce-step
                                {i % 2 === 0 ? 'left-2' : 'right-2'}"
                            >
                                <span class="text-xs">▶️</span>
                            </div>
                        {/if}
                    </div>
                </button>
            </div>
        {/each}

        <!-- END TROPHY -->
        <div class="relative w-full flex justify-center mt-8 opacity-50">
            <div
                class="w-16 h-16 rounded-full border-4 border-[#FFD700] bg-black/50 text-[#FFD700] flex items-center justify-center z-10"
            >
                <span class="text-3xl">⭐</span>
            </div>
        </div>
        <div class="text-xs text-gray-500 italic text-center mt-2">
            Bientôt d'autres niveaux...
        </div>
    </div>
</div>

<style>
    /* Custom Scrollbar for the list */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #1a100e;
    }
    ::-webkit-scrollbar-thumb {
        background: #3e2723;
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #5d4037;
    }
</style>
