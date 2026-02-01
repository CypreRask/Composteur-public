<script>
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";
    import { SORTER_ITEMS } from "../../lib/gameData.js";
    import { createEventDispatcher, onMount } from "svelte";

    const dispatch = createEventDispatcher();

    export let forceLevel = null; // If set, skips menu

    // GAME STATE
    let gameActive = false;
    let gameOver = false;
    let victory = false;
    let level = 0; // 0: Select, 1: Summer (Easy), 2: Autumn (Hard)

    // Stockpile State
    let stockpile = {
        greens: [], // Max 3
        browns: [], // Max 3
    };

    let currentItem = null;
    let score = 0;
    let strikes = 0;
    let balanceCN = 0; // -10 (Green/Nitrogen) to +10 (Brown/Carbon). Ideal 0.
    let feedback = "";
    let timeLeft = 60;
    let timerInterval;

    const WIN_SCORE = 100;

    function startGame(selectedLevel) {
        if (!selectedLevel) return;
        level = selectedLevel;

        // Reset Logic
        score = 0;
        strikes = 0;
        balanceCN = 0;
        timeLeft = 60;
        stockpile = { greens: [], browns: [] };
        feedback = `Niveau ${level === 1 ? "ETE (Verts 🍏)" : "AUTOMNE (Bruns 🍂)"} : Equilibre le tas !`;
        gameActive = true;
        gameOver = false;
        victory = false;

        spawnItem();
        startTimer();
        spawnItem();
        startTimer();
    }

    onMount(() => {
        if (forceLevel) {
            startGame(forceLevel);
        }
    });

    function startTimer() {
        if (timerInterval) clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            timeLeft--;
            if (timeLeft <= 0) {
                endGame(false, "⏰ Temps écoulé !");
            }
        }, 1000);
    }

    function endGame(isVictory, msg) {
        gameActive = false;
        clearInterval(timerInterval);
        feedback = msg;
        if (isVictory) {
            victory = true;
            // Dispatch complete event specifically for Path Learning
            dispatch("complete", { score: score, level: level });
        } else {
            gameOver = true;
        }
    }

    function spawnItem() {
        // Season Logic
        // Level 1 (Summer): 70% Green, 30% Brown/Trash
        // Level 2 (Autumn): 30% Green, 70% Brown/Trash

        const isSummer = level === 1;
        const greenProb = isSummer ? 0.6 : 0.3; // Base prob for greens

        let typeGroup =
            Math.random() < greenProb
                ? "green"
                : Math.random() < 0.5
                  ? "brown"
                  : "trash";

        // Safety: ensure we don't get stuck if rand aligns weirdly, just pick random from full list if needed,
        // but better to filter list
        let pool = SORTER_ITEMS;
        if (Math.random() < 0.8) {
            // 80% of time respect season bias
            if (typeGroup === "green")
                pool = SORTER_ITEMS.filter(
                    (i) => i.type === "green" || i.type === "citrus",
                ); // citrus is green type
            else if (typeGroup === "brown")
                pool = SORTER_ITEMS.filter((i) => i.type === "brown");
            // else trash, use full pool or filter? Let's just use random for trash
        }

        const r = Math.floor(Math.random() * pool.length);
        currentItem = { ...pool[r], uid: Math.random() };
    }

    function addToStockpile() {
        if (!currentItem) return;

        const type =
            currentItem.type === "green" || currentItem.type === "citrus"
                ? "greens"
                : currentItem.type === "brown"
                  ? "browns"
                  : null;

        if (!type) {
            feedback = "🚫 Pas stockable ! (Seulement Verts/Bruns)";
            return;
        }

        if (stockpile[type].length >= 3) {
            feedback = "🚫 Stock Plein !";
            return;
        }

        stockpile[type] = [...stockpile[type], currentItem];
        feedback = "📦 Mis en réserve !";
        spawnItem();
    }

    function useFromStockpile(type) {
        if (!gameActive || currentItem) {
            if (currentItem) feedback = "🚫 Traite l'objet actuel d'abord !";
            return;
        }

        if (stockpile[type].length === 0) return;

        // Pop item
        const item = stockpile[type][stockpile[type].length - 1];
        stockpile[type] = stockpile[type].slice(0, -1);

        currentItem = item;
    }

    function handleAction(action) {
        if (!gameActive || !currentItem) return;

        const type = currentItem.type;
        let correct = false;

        // Logic
        if (action === "trash") {
            if (type === "trash" || type === "toxic") correct = true;
        } else {
            // Compost
            if (type === "green" || type === "brown") correct = true;
        }

        // Apply Results
        if (correct) {
            score += 10;
            // EDUCATIONAL FEEDBACK
            feedback = currentItem.info || "✨ Bien joué !";

            // Scientific Balance Logic
            if (action === "compost") {
                if (type === "green") balanceCN -= 2; // Adds Nitrogen (Wet/Green)
                if (type === "brown") balanceCN += 2; // Adds Carbon (Dry/Brown)
            }

            // Check Win
            if (score >= WIN_SCORE) {
                endGame(true, "🏆 Compost Parfait !");
                return;
            }
        } else {
            strikes++;
            feedback = "❌ Rate !";
            if (type === "toxic" && action === "compost") {
                endGame(false, "☠️ GAME OVER ! Tu as composté une pile !");
                return;
            }
            score = Math.max(0, score - 5);
        }

        // Check fatal balance
        if (Math.abs(balanceCN) > 10) {
            endGame(
                false,
                balanceCN > 0
                    ? "🌵 Trop sec ! (Manque d'eau/Vert)"
                    : "🤢 Trop mouillé ! (Manque d'air/Brun)",
            );
            return;
        }

        if (strikes >= 3) {
            endGame(false, "💀 Trop d'erreurs !");
        } else {
            spawnItem();
        }
    }
</script>

<div class="h-full relative">
    <!-- SCANLINES OVERLAY -->
    <div
        class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjNDg0ODQ4IiBmaWxsLW9wYWNpdHk9IjAuMSIvPgo8L3N2Zz4=')] opacity-50 pointer-events-none z-0"
    ></div>

    <RetroWindow title="Le Trieur Fou (V2)" mode="inline" width="w-full">
        {#if !gameActive && !victory && !gameOver}
            <!-- START SCREEN -->
            <div
                class="flex flex-col items-center justify-center p-8 space-y-4"
            >
                <div class="text-6xl animate-bounce">🗑️</div>
                <h2 class="text-2xl font-bold text-[#C0CA33]">LE TRIEUR FOU</h2>

                {#if level === 0}
                    <!-- LEVEL SELECT -->
                    <div class="grid grid-cols-2 gap-4 w-full max-w-sm">
                        <button
                            class="p-4 border-b-4 border-green-800 bg-green-600 hover:bg-green-500 text-white rounded active:border-b-0 active:mt-1 transition-all group"
                            on:click={() => startGame(1)}
                        >
                            <div
                                class="text-4xl mb-2 group-hover:scale-110 transition-transform"
                            >
                                ☀️
                            </div>
                            <div class="text-sm font-bold">ÉTÉ</div>
                        </button>
                        <button
                            class="p-4 border-b-4 border-orange-800 bg-orange-600 hover:bg-orange-500 text-white rounded active:border-b-0 active:mt-1 transition-all group"
                            on:click={() => startGame(2)}
                        >
                            <div
                                class="text-4xl mb-2 group-hover:scale-110 transition-transform"
                            >
                                🍂
                            </div>
                            <div class="text-sm font-bold">AUTOMNE</div>
                        </button>
                    </div>
                    <p class="text-[10px] text-gray-400 mt-4">
                        Choisis ta saison pour commencer
                    </p>
                {:else}
                    <!-- Should not happen with new flow logic but keeping safety -->
                    {#if !forceLevel}
                        <button on:click={() => (level = 0)}>Retour</button>
                    {/if}
                {/if}
            </div>
        {:else if victory}
            <!-- VICTORY SCREEN -->
            <div
                class="flex flex-col items-center justify-center p-8 space-y-4"
            >
                <div class="text-6xl animate-pulse">🏆</div>
                <h2 class="text-2xl font-bold text-yellow-400">VICTOIRE !</h2>
                <p class="text-sm text-center text-gray-300">
                    Tu es un Maître Composteur.
                </p>
                <div
                    class="text-xs font-mono bg-black/40 p-2 rounded border border-gray-600"
                >
                    C/N Final: {balanceCN === 0 ? "PARFAIT (0)" : balanceCN}
                </div>
                <button
                    class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500"
                    on:click={() => {
                        victory = false;
                        if (forceLevel) startGame(forceLevel);
                        else level = 0;
                    }}>Rejouer</button
                >
            </div>
        {:else if gameOver}
            <!-- GAMEOVER SCREEN -->
            <div
                class="flex flex-col items-center justify-center p-8 space-y-4"
            >
                <div class="text-6xl">💀</div>
                <h2 class="text-2xl font-bold text-red-500">PERDU !</h2>
                <p class="text-red-300 text-center font-bold">{feedback}</p>
                <button
                    class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-500"
                    on:click={() => {
                        gameOver = false;
                        if (forceLevel) startGame(forceLevel);
                        else level = 0;
                    }}>Réessayer</button
                >
            </div>
        {:else}
            <!-- GAME HUD -->
            <div
                class="flex justify-between items-center mb-4 bg-black/40 p-2 rounded border border-[#558B2F]"
            >
                <div class="flex flex-col">
                    <span class="text-[10px] text-gray-400">SCORE</span>
                    <span class="text-xl text-[#C0CA33] font-bold"
                        >{score}/{WIN_SCORE}</span
                    >
                </div>
                <div class="flex flex-col items-center">
                    <span class="text-[10px] text-gray-400">TEMPS</span>
                    <span
                        class="text-xl {timeLeft < 10
                            ? 'text-red-500 animate-pulse'
                            : 'text-white'}">{timeLeft}s</span
                    >
                </div>
                <div class="flex gap-1">
                    {#each Array(3) as _, i}
                        <div
                            class="text-lg {i < strikes
                                ? 'text-red-500'
                                : 'text-[#2E3B20]'}"
                        >
                            ❌
                        </div>
                    {/each}
                </div>
            </div>

            <!-- PLAY AREA -->
            <div class="flex flex-col items-center flex-1">
                {#if currentItem}
                    <div
                        class="w-32 h-32 bg-[#FFF8E1] border-4 border-[#8D6E63] rounded-lg shadow-xl flex flex-col items-center justify-center mb-6 animate-pop-in relative"
                    >
                        <div class="text-5xl mb-2 filter drop-shadow-md">
                            {currentItem.icon}
                        </div>
                        <div
                            class="text-[#3E2723] font-bold text-xs uppercase bg-white px-2 py-0.5 border border-[#3E2723] rounded-full"
                        >
                            {currentItem.name}
                        </div>
                    </div>
                {/if}

                <!-- STOCKPILE UI -->
                <div class="w-full max-w-sm flex justify-between gap-4 mb-4">
                    <!-- Greens Stock -->
                    <div class="flex flex-col items-center">
                        <div class="text-[10px] text-green-400 mb-1">
                            STOCK VERTS
                        </div>
                        <div
                            class="flex bg-black/40 p-1 rounded border border-green-800 gap-1 min-h-[40px] min-w-[100px]"
                        >
                            {#each stockpile.greens as item}
                                <div
                                    class="w-8 h-8 bg-[#2E3B20] rounded border border-green-600 flex items-center justify-center text-lg"
                                >
                                    {item.icon}
                                </div>
                            {/each}
                            {#if stockpile.greens.length < 3}
                                {#each Array(3 - stockpile.greens.length) as _}
                                    <div
                                        class="w-8 h-8 border border-green-900/50 rounded border-dashed"
                                    ></div>
                                {/each}
                            {/if}
                        </div>
                        {#if !currentItem && stockpile.greens.length > 0}
                            <button
                                class="mt-1 text-[9px] bg-green-700 px-2 rounded animate-pulse"
                                on:click={() => useFromStockpile("greens")}
                                >UTILISER</button
                            >
                        {/if}
                    </div>

                    <!-- Browns Stock -->
                    <div class="flex flex-col items-center">
                        <div class="text-[10px] text-orange-400 mb-1">
                            STOCK BRUNS
                        </div>
                        <div
                            class="flex bg-black/40 p-1 rounded border border-orange-800 gap-1 min-h-[40px] min-w-[100px]"
                        >
                            {#each stockpile.browns as item}
                                <div
                                    class="w-8 h-8 bg-[#3E2723] rounded border border-orange-600 flex items-center justify-center text-lg"
                                >
                                    {item.icon}
                                </div>
                            {/each}
                            {#if stockpile.browns.length < 3}
                                {#each Array(3 - stockpile.browns.length) as _}
                                    <div
                                        class="w-8 h-8 border border-orange-900/50 rounded border-dashed"
                                    ></div>
                                {/each}
                            {/if}
                        </div>
                        {#if !currentItem && stockpile.browns.length > 0}
                            <button
                                class="mt-1 text-[9px] bg-orange-700 px-2 rounded animate-pulse"
                                on:click={() => useFromStockpile("browns")}
                                >UTILISER</button
                            >
                        {/if}
                    </div>
                </div>

                <div
                    class="h-12 text-xs text-center font-bold text-yellow-200 mb-2 px-4 py-2 bg-black/20 rounded w-full whitespace-pre-wrap"
                >
                    {feedback}
                </div>

                <!-- CONTROLS -->
                <div class="flex gap-2 w-full max-w-md mb-6 px-2">
                    <button
                        class="flex-1 bg-red-900/80 border-b-4 border-red-700 hover:bg-red-800 p-2 rounded text-center group active:border-b-0 active:translate-y-1 transition-all flex flex-col items-center justify-center"
                        on:click={() => handleAction("trash")}
                    >
                        <span class="text-xl mb-1">⛔</span>
                        <span class="font-bold text-[10px]">JETER</span>
                    </button>

                    <!-- NEW STOCK BUTTON -->
                    <button
                        class="flex-1 bg-blue-900/80 border-b-4 border-blue-700 hover:bg-blue-800 p-2 rounded text-center group active:border-b-0 active:translate-y-1 transition-all flex flex-col items-center justify-center"
                        on:click={addToStockpile}
                    >
                        <span class="text-xl mb-1">📦</span>
                        <span class="font-bold text-[10px]">STOCK</span>
                    </button>

                    <button
                        class="flex-1 bg-green-900/80 border-b-4 border-green-700 hover:bg-green-800 p-2 rounded text-center group active:border-b-0 active:translate-y-1 transition-all flex flex-col items-center justify-center"
                        on:click={() => handleAction("compost")}
                    >
                        <span class="text-xl mb-1">♻️</span>
                        <span class="font-bold text-[10px]">COMPOST</span>
                    </button>
                </div>

                <!-- C/N GAUGE -->
                <div class="w-full max-w-sm space-y-1">
                    <div
                        class="flex justify-between text-[8px] text-gray-400 uppercase"
                    >
                        <span>Trop Vert (Azote)</span>
                        <span>Equilibre</span>
                        <span>Trop Brun (Carbone)</span>
                    </div>
                    <div
                        class="h-4 bg-gray-900 rounded-full border border-gray-600 relative overflow-hidden"
                    >
                        <!-- Zones -->
                        <div
                            class="absolute left-0 w-1/3 h-full bg-green-900/60"
                        ></div>
                        <!-- Wet -->
                        <div
                            class="absolute right-0 w-1/3 h-full bg-yellow-900/60"
                        ></div>
                        <!-- Dry -->
                        <!-- Needle -->
                        <div
                            class="absolute top-0 bottom-0 w-1 bg-white shadow-[0_0_5px_white] transition-all duration-300"
                            style="left: {50 + balanceCN * 5}%"
                        ></div>
                    </div>
                </div>
            </div>
        {/if}
    </RetroWindow>
</div>

<style>
    @keyframes pop-in {
        0% {
            transform: scale(0) rotate(-10deg);
        }
        80% {
            transform: scale(1.1) rotate(5deg);
        }
        100% {
            transform: scale(1) rotate(0deg);
        }
    }
    .animate-pop-in {
        animation: pop-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
</style>
