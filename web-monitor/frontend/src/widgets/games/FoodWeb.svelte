<script>
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";
    import { onMount, createEventDispatcher } from "svelte";
    import { fade, scale } from "svelte/transition";

    const dispatch = createEventDispatcher();

    // --- GAME DATA: TROPHIC PYRAMID (EXTENDED) ---
    const NODES = [
        // TIER 0: RESOURCES
        {
            id: "leaf",
            tier: 0,
            x: 20,
            y: 90,
            label: "Feuille (C)",
            icon: "🍂",
            info: "Lignine pour les champignons.",
        },
        {
            id: "green",
            tier: 0,
            x: 80,
            y: 90,
            label: "Epluchure (N)",
            icon: "🥬",
            info: "Azote pour les bactéries.",
        },

        // TIER 1: DECOMPOSERS
        {
            id: "fungi",
            tier: 1,
            x: 30,
            y: 72,
            label: "Champignon",
            icon: "🍄",
            diet: ["leaf"],
            info: "Décomposeur primaire.",
        },
        {
            id: "bact",
            tier: 1,
            x: 70,
            y: 72,
            label: "Bactérie",
            icon: "🦠",
            diet: ["green"],
            info: "Décomposeur rapide.",
        },

        // TIER 2: GRAZERS
        {
            id: "collem",
            tier: 2,
            x: 20,
            y: 52,
            label: "Collembole",
            icon: "🐜",
            diet: ["fungi"],
            info: "Brouteur de champignons.",
        },
        {
            id: "nem",
            tier: 2,
            x: 80,
            y: 52,
            label: "Nématode",
            icon: "🪱",
            diet: ["bact"],
            info: "Brouteur de bactéries.",
        },

        // TIER 3: PREDATORS
        {
            id: "mite",
            tier: 3,
            x: 50,
            y: 35,
            label: "Acarien (Gamaside)",
            icon: "🕷️",
            diet: ["collem", "nem"],
            info: "Chasseur véloce.",
        },

        // TIER 4: APEX PREDATOR
        {
            id: "pseudo",
            tier: 4,
            x: 50,
            y: 15,
            label: "Pseudoscorpion",
            icon: "🦂",
            diet: ["mite", "collem"],
            info: "Le tigre du compost !",
        },
    ];

    let connections = [];
    let dragging = null;
    let mousePos = { x: 0, y: 0 };
    let container;
    let victory = false;
    let hoveredNodeId = null;

    // --- LOGIC ---
    function startDrag(node, e) {
        if (victory) return;
        e.preventDefault();
        e.stopPropagation();
        dragging = node;
        updateMousePos(e);
        updateContainerRect();
    }

    function handleGlobalMove(e) {
        if (!dragging) return;
        updateMousePos(e);
    }

    function handleGlobalUp(e) {
        if (!dragging) return;
        if (hoveredNodeId) {
            const target = NODES.find((n) => n.id === hoveredNodeId);
            if (target && target.id !== dragging.id) {
                tryConnect(dragging, target);
            }
        }
        dragging = null;
    }

    let containerRect = { left: 0, top: 0, width: 1, height: 1 };

    function updateContainerRect() {
        if (container) containerRect = container.getBoundingClientRect();
    }

    function updateMousePos(e) {
        let clientX, clientY;
        if (e.type.startsWith("touch")) {
            clientX = e.touches[0].clientX;
            clientY = e.touches[0].clientY;
            const targetEl = document.elementFromPoint(clientX, clientY);
            const nodeEl = targetEl?.closest(".node-element");
            hoveredNodeId = nodeEl ? nodeEl.dataset.id : null;
        } else {
            clientX = e.clientX;
            clientY = e.clientY;
        }

        if (containerRect.width > 0) {
            mousePos.x =
                ((clientX - containerRect.left) / containerRect.width) * 100;
            mousePos.y =
                ((clientY - containerRect.top) / containerRect.height) * 100;
        }
    }

    function tryConnect(source, target) {
        // Rule: Prey -> Predator (Drag from Food to Eater)
        if (target.diet && target.diet.includes(source.id)) {
            if (
                !connections.find(
                    (c) => c.from === source.id && c.to === target.id,
                )
            ) {
                connections = [
                    ...connections,
                    { from: source.id, to: target.id },
                ];
                checkVictory();
            }
        }
    }

    function checkVictory() {
        // REQUIRED LINKS:
        // Leaf->Fungi, Green->Bact
        // Fungi->Collem, Bact->Nem
        // Collem->Mite, Nem->Mite
        // Collem->Pseudo, Mite->Pseudo
        // Total = 8
        if (connections.length >= 8) {
            victory = true;
            dispatch("complete", { score: 100 });
        }
    }

    function restart() {
        connections = [];
        victory = false;
        dragging = null;
    }

    function isValidTarget(source, target) {
        if (!source || !target) return false;
        if (source.id === target.id) return false;
        return target.diet?.includes(source.id);
    }
</script>

<svelte:window
    on:mousemove={handleGlobalMove}
    on:mouseup={handleGlobalUp}
    on:touchmove|nonpassive={handleGlobalMove}
    on:touchend={handleGlobalUp}
    on:resize={updateContainerRect}
/>

<div
    class="h-full relative font-pixel flex flex-col select-none"
    bind:this={container}
>
    <RetroWindow
        title="Le Festin du Sol"
        mode="inline"
        height="h-full"
        width="w-full"
    >
        <!-- VICTORY OVERLAY -->
        {#if victory}
            <div
                class="absolute inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur"
                transition:fade
            >
                <div
                    class="text-center p-8 border-4 border-[#C0CA33] bg-[#2E3B20] rounded-xl shadow-2xl"
                    in:scale
                >
                    <div class="text-6xl animate-bounce mb-4">🦂</div>
                    <h2 class="text-3xl text-[#C0CA33] font-bold mb-2">
                        MAÎTRE DU SOL !
                    </h2>
                    <p class="text-white text-sm">
                        Le Pseudoscorpion règne en maître.
                    </p>
                    <button
                        class="mt-6 px-6 py-2 bg-[#558B2F] text-white border-b-4 border-[#33691E] active:border-b-0 active:translate-y-1"
                        on:click={restart}
                    >
                        Rejouer
                    </button>
                </div>
            </div>
        {/if}

        <div class="absolute inset-0 bg-[#3E2723] overflow-hidden">
            <div
                class="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCI+CiAgPGNpcmNsZSBjeD0iMiIgY3k9IjIiIHI9IjEiIGZpbGw9IiNmZmYiLz4KPC9zdmc+')]"
            ></div>

            <!-- Tier Labels -->
            <div
                class="absolute w-full border-b border-white/5 text-[8px] text-white/20 uppercase tracking-widest pl-2"
                style="top: 20%"
            >
                Super-Prédateurs
            </div>
            <div
                class="absolute w-full border-b border-white/5 text-[8px] text-white/20 uppercase tracking-widest pl-2"
                style="top: 40%"
            >
                Prédateurs
            </div>
            <div
                class="absolute w-full border-b border-white/5 text-[8px] text-white/20 uppercase tracking-widest pl-2"
                style="top: 60%"
            >
                Consommateurs I
            </div>
            <div
                class="absolute w-full border-b border-white/5 text-[8px] text-white/20 uppercase tracking-widest pl-2"
                style="top: 80%"
            >
                Décomposeurs
            </div>
            <div
                class="absolute w-full bottom-0 h-[8%] bg-black/20 text-[8px] text-white/20 uppercase tracking-widest pl-2 pt-1"
            >
                Sol (Matière Organique)
            </div>

            <!-- SVG LAYER -->
            <svg
                class="absolute inset-0 w-full h-full pointer-events-none z-10"
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
            >
                <defs>
                    <marker
                        id="arrow"
                        markerWidth="6"
                        markerHeight="6"
                        refX="15"
                        refY="3"
                        orient="auto"
                        markerUnits="strokeWidth"
                    >
                        <path d="M0,0 L0,6 L9,3 z" fill="#8BC34A" />
                    </marker>
                    <filter id="glow">
                        <feGaussianBlur
                            stdDeviation="0.5"
                            result="coloredBlur"
                        />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                {#each connections as conn}
                    {@const start = NODES.find((n) => n.id === conn.from)}
                    {@const end = NODES.find((n) => n.id === conn.to)}
                    <line
                        x1={start.x}
                        y1={start.y}
                        x2={end.x}
                        y2={end.y}
                        stroke="#8BC34A"
                        stroke-width="0.6"
                        marker-end="url(#arrow)"
                        stroke-dasharray="2,1"
                        class="animate-flow"
                        filter="url(#glow)"
                    />
                {/each}

                {#if dragging}
                    <line
                        x1={dragging.x}
                        y1={dragging.y}
                        x2={mousePos.x}
                        y2={mousePos.y}
                        stroke="#C0CA33"
                        stroke-width="1"
                        stroke-linecap="round"
                        stroke-dasharray="1,1"
                        class="opacity-80"
                    />
                {/if}
            </svg>

            <!-- NODES -->
            {#each NODES as node}
                <div
                    class="absolute w-14 h-14 -ml-7 -mt-7 rounded-full border-2 flex flex-col items-center justify-center shadow-lg transition-all z-20 node-element
                           {dragging?.id === node.id
                        ? 'scale-110 ring-4 ring-[#C0CA33] cursor-grabbing'
                        : 'cursor-grab hover:scale-105'}
                           {dragging && isValidTarget(dragging, node)
                        ? 'bg-green-900 border-green-400 animate-pulse'
                        : 'bg-[#1A202C] border-[#5D4037]'}
                           "
                    style="left: {node.x}%; top: {node.y}%;touch-action: none;"
                    data-id={node.id}
                    on:mousedown={(e) => startDrag(node, e)}
                    on:touchstart={(e) => startDrag(node, e)}
                    on:mouseenter={() => (hoveredNodeId = node.id)}
                    on:mouseleave={() => (hoveredNodeId = null)}
                >
                    <div class="text-xl pointer-events-none select-none">
                        {node.icon}
                    </div>
                    <div
                        class="absolute -bottom-5 bg-black/70 px-2 py-0.5 rounded text-[7px] text-gray-300 font-bold whitespace-nowrap pointer-events-none"
                    >
                        {node.label}
                    </div>
                    {#if connections.some((c) => c.to === node.id)}
                        <div
                            class="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-bounce shadow-green flex items-center justify-center text-[6px] text-black font-bold"
                        >
                            ⚡
                        </div>
                    {/if}
                </div>
            {/each}

            <!-- HUD -->
            <div
                class="absolute top-2 left-2 pointer-events-none z-0 opacity-80"
            >
                <div
                    class="bg-black/50 p-2 rounded border border-gray-600 max-w-[180px]"
                >
                    <h3
                        class="text-[#C0CA33] text-[9px] font-bold uppercase mb-1"
                    >
                        Mission : Maître du Sol
                    </h3>
                    <p class="text-[8px] text-gray-300 leading-tight">
                        Construis la chaîne complète jusqu'au <strong
                            >Pseudoscorpion</strong
                        >.<br />
                        Attention : Certains prédateurs mangent plusieurs proies
                        !
                    </p>
                </div>
            </div>

            <div
                class="absolute bottom-2 right-2 text-[9px] font-mono text-gray-400 z-0"
            >
                LIENS : {connections.length} / 8
            </div>
        </div>
    </RetroWindow>
</div>

<style>
    @keyframes flow {
        to {
            stroke-dashoffset: -3;
        }
    }
    .animate-flow {
        animation: flow 1s linear infinite;
    }
</style>
