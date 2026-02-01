<script>
    import PathMap from "./components/learn/PathMap.svelte";
    import TheoryWindow from "./widgets/learn/TheoryWindow.svelte";
    import ArcadeMenu from "./widgets/learn/ArcadeMenu.svelte";

    // Games Imports
    import Microscope from "./widgets/learn/Microscope.svelte";
    import CompostSorter from "./widgets/games/CompostSorter.svelte";
    import CycleBuilder from "./widgets/games/CycleBuilder.svelte";
    import FoodWeb from "./widgets/games/FoodWeb.svelte";
    import Chemistry from "./widgets/learn/Chemistry.svelte";
    import Quiz from "./widgets/learn/Quiz.svelte";

    import { createEventDispatcher } from "svelte";

    let viewMode = "path"; // 'path', 'arcade', 'game', 'theory'
    let activeGame = null; // ID string for game component (e.g. 'sorter')
    let activeTheory = null; // Node object for theory
    let activePathNode = null; // Node object for current path item (game or theory)

    function handlePathSelect(event) {
        const node = event.detail;
        activePathNode = node; // Track the node!

        if (node.type === "game") {
            activeGame = node.gameId;
            viewMode = "game";
        } else if (node.type === "theory") {
            activeTheory = node;
            viewMode = "theory";
        }
    }

    function handleArcadeSelect(event) {
        activeGame = event.detail;
        viewMode = "game";
    }

    function closeGame() {
        activeGame = null;
        viewMode = "path";
    }

    function completeTheory() {
        if (pathMapInstance && activePathNode) {
            pathMapInstance.completeNode(
                activePathNode.id,
                activePathNode.xp || 100,
            );
        }
        closeContent();
    }

    function handleGameComplete(event) {
        console.log("Game Complete Event:", event.detail);
        // Only mark complete if we are in Path mode (not Arcade) and have an active node
        if (
            pathMapInstance &&
            activePathNode &&
            activePathNode.type === "game"
        ) {
            // Optional: Check score requirement?
            // node.requirement.score
            pathMapInstance.completeNode(
                activePathNode.id,
                event.detail.score || 100,
            );
            alert("Niveau validé ! Retour au parcours...");
            closeContent();
        }
    }

    function closeContent() {
        activeGame = null;
        activeTheory = null;
        activePathNode = null;
        viewMode = "path";
    }

    let pathMapInstance;

    function goBack() {
        activeGame = null;
        activeTheory = null;
        viewMode = "path";
    }
</script>

<div class="h-full w-full bg-[#1A202C] text-white font-pixel flex flex-col">
    <!-- TOP BAR (Only when in game or theory) -->
    <div
        class="bg-[#2D3748] p-2 flex flex-wrap items-center justify-between gap-2 shadow-md z-50 shrink-0"
    >
        <div class="flex items-center gap-2 overflow-hidden">
            {#if viewMode !== "path" && viewMode !== "arcade"}
                <button
                    class="px-3 py-2 bg-red-900/80 text-white text-[10px] uppercase border border-red-500 hover:bg-red-800 flex items-center gap-1 shrink-0"
                    on:click={goBack}
                >
                    ⬅️ <span class="hidden sm:inline">Retour</span>
                </button>
            {/if}

            {#if viewMode === "game"}
                <span
                    class="text-gray-400 text-[10px] uppercase tracking-wider truncate"
                >
                    <span class="hidden sm:inline">Mission :</span>
                    <span class="text-white font-bold">{activeGame}</span>
                </span>
            {/if}
        </div>

        <div class="flex gap-2 shrink-0">
            <button
                class="text-[10px] uppercase px-3 py-1 rounded {viewMode ===
                'path'
                    ? 'bg-[#C0CA33] text-black font-bold'
                    : 'bg-gray-700 text-gray-400'}"
                on:click={() => (viewMode = "path")}
            >
                Parcours
            </button>
            <button
                class="text-[10px] uppercase px-3 py-1 rounded {viewMode ===
                'arcade'
                    ? 'bg-[#C0CA33] text-black font-bold'
                    : 'bg-gray-700 text-gray-400'}"
                on:click={() => (viewMode = "arcade")}
            >
                Arcade
            </button>
        </div>
    </div>

    <!-- CONTENT AREA -->
    <div class="flex-1 overflow-hidden relative p-4">
        <!-- PATH MAP (Always rendered, hidden via CSS to preserve state/instance) -->
        <div class="h-full w-full {viewMode === 'path' ? 'block' : 'hidden'}">
            <PathMap bind:this={pathMapInstance} on:select={handlePathSelect} />
        </div>

        {#if viewMode === "theory" && activeTheory}
            <TheoryWindow
                title={activeTheory.title}
                content={activeTheory.content}
                xp={activeTheory.xp}
                on:close={goBack}
                on:complete={completeTheory}
            />
        {:else if viewMode === "arcade"}
            <ArcadeMenu on:select={handleArcadeSelect} />
        {:else if viewMode === "game"}
            <!-- GAME CONTAINER: Centered + Max Width -->
            <div
                class="h-full w-full max-w-5xl mx-auto flex flex-col justify-center"
            >
                <!-- Pass on:complete handle to all games -->
                {#if activeGame === "microscope"}
                    <Microscope on:complete={handleGameComplete} />
                {:else if activeGame === "sorter"}
                    <CompostSorter
                        forceLevel={activePathNode?.config?.level}
                        on:complete={handleGameComplete}
                    />
                {:else if activeGame === "cycle" || activeGame === "cyclebuilder"}
                    <CycleBuilder on:complete={handleGameComplete} />
                {:else if activeGame === "foodweb"}
                    <FoodWeb on:complete={handleGameComplete} />
                {:else if activeGame === "chemistry"}
                    <Chemistry on:complete={handleGameComplete} />
                {:else if activeGame === "quiz"}
                    <Quiz on:complete={handleGameComplete} />
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    /* Global Pixel Font smoothing disabling */
    :global(body) {
        image-rendering: pixelated;
    }
</style>
