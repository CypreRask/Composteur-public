<script>
    export let soil_hum = 50; // Simule l'humidité/qualité du sol
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();

    // Si l'humidité est bonne, le réseau s'active
    $: isActive = soil_hum > 30;

    // Tooltip State
    let hoveredInfo = null;
    function setHover(info) {
        hoveredInfo = info;
    }
    function clearHover() {
        hoveredInfo = null;
    }
</script>

<!-- CONTAINER: Adjusted width to encompass both Tree (Center) and C4 (Left) -->
<div
    class="relative w-[900px] h-[350px] overflow-visible cursor-pointer select-none group"
    on:click={() => dispatch("openRoots")}
    on:keydown={(e) => e.key === "Enter" && dispatch("openRoots")}
    role="button"
    tabindex="0"
>
    <!-- VIEWBOX: -300 to 600 (Width 900) -->
    <svg
        width="100%"
        height="100%"
        viewBox="-300 -20 900 350"
        preserveAspectRatio="xMidYMin meet"
        class="block overflow-visible"
        style="image-rendering: pixelated; shape-rendering: crispEdges;"
    >
        <defs>
            <pattern
                id="pixelGrid"
                width="4"
                height="4"
                patternUnits="userSpaceOnUse"
            >
                <rect width="4" height="4" fill="transparent" />
            </pattern>
            <!-- Gradient for Mycelium Glow -->
            <filter id="mycoGlow">
                <feGaussianBlur stdDeviation="1" result="coloredBlur" />
                <feMerge>
                    <feMergeNode in="coloredBlur" />
                    <feMergeNode in="SourceGraphic" />
                </feMerge>
            </filter>
        </defs>

        <!-- === 1. TREE ROOT SYSTEM (CENTER) - V7.5 FINAL (SOLID) === -->
        <g
            transform="translate(150, 32)"
            class="cursor-alias hover:brightness-125 transition-all hover:scale-105"
            style="transform-box: fill-box; transform-origin: top center;"
            on:mouseenter={() => setHover("Racines (Ancrage & Structure)")}
            on:mouseleave={clearHover}
            role="img"
            aria-label="Tree Roots"
        >
            <!-- TRUNK BASE (Wide & Anchor) -->
            <!-- Matches w-24 (96px) of Trunk.svelte -->
            <rect x="-48" y="-20" width="96" height="20" fill="#5D4037" />
            <rect x="-40" y="0" width="80" height="15" fill="#5D4037" />

            <!-- === 5 MAIN ROOTS (REBALANCED & CONTINUOUS) === -->

            <!-- 1. FAR LEFT (Overlapping Steps) -->
            <rect x="-55" y="10" width="15" height="20" fill="#5D4037" />
            <!-- Shifted left -->
            <rect x="-65" y="25" width="15" height="30" fill="#5D4037" />
            <!-- Overlap x: -55..-40 vs -65..-50 -> 5px overlap -->
            <rect x="-80" y="50" width="15" height="40" fill="#5D4037" />
            <rect x="-95" y="80" width="15" height="40" fill="#5D4037" />
            <rect x="-110" y="110" width="12" height="30" fill="#5D4037" />
            <rect x="-120" y="135" width="10" height="30" fill="#5D4037" />
            <!-- Deep Tip -->

            <!-- 2. MID LEFT (Thicker/Structural) -->
            <rect x="-30" y="15" width="22" height="25" fill="#5D4037" />
            <rect x="-35" y="35" width="20" height="40" fill="#5D4037" />
            <rect x="-40" y="70" width="18" height="40" fill="#5D4037" />
            <rect x="-45" y="105" width="15" height="40" fill="#5D4037" />
            <rect x="-48" y="140" width="10" height="30" fill="#5D4037" />
            <!-- Deep Tip -->

            <!-- 3. CENTER (Split Wider/Less Central) -->
            <!-- Left-Center Branch -->
            <rect x="-15" y="15" width="15" height="30" fill="#5D4037" />
            <rect x="-20" y="40" width="12" height="40" fill="#5D4037" />
            <rect x="-22" y="75" width="10" height="40" fill="#5D4037" />
            <rect x="-24" y="110" width="10" height="40" fill="#5D4037" />

            <!-- Right-Center Branch (Gap in middle) -->
            <rect x="5" y="15" width="15" height="30" fill="#5D4037" />
            <rect x="10" y="40" width="12" height="40" fill="#5D4037" />
            <rect x="15" y="75" width="10" height="40" fill="#5D4037" />
            <rect x="18" y="110" width="10" height="40" fill="#5D4037" />

            <!-- Tiny bridge high up -->
            <rect x="-5" y="20" width="10" height="10" fill="#5D4037" />

            <!-- 4. MID RIGHT (Thicker/Structural) -->
            <rect x="10" y="15" width="22" height="25" fill="#5D4037" />
            <rect x="15" y="35" width="20" height="40" fill="#5D4037" />
            <rect x="25" y="70" width="18" height="40" fill="#5D4037" />
            <rect x="35" y="105" width="15" height="40" fill="#5D4037" />
            <rect x="40" y="140" width="10" height="30" fill="#5D4037" />
            <!-- Deep Tip -->

            <!-- 5. FAR RIGHT (Overlapping Steps) -->
            <rect x="40" y="10" width="15" height="20" fill="#5D4037" />
            <!-- Shifted right (was 35) -->
            <rect x="50" y="25" width="15" height="30" fill="#5D4037" />
            <!-- Overlap x: 40..55 vs 50..65 -> 5px overlap -->
            <rect x="65" y="50" width="15" height="40" fill="#5D4037" />
            <rect x="80" y="80" width="15" height="40" fill="#5D4037" />
            <rect x="95" y="110" width="12" height="30" fill="#5D4037" />
            <rect x="105" y="135" width="10" height="30" fill="#5D4037" />
            <!-- Deep Tip -->

            <!-- === TERTIARY BRANCHING (NETWORK) === -->

            <!-- Left Side connections -->
            <rect x="-80" y="60" width="15" height="8" fill="#5D4037" />
            <rect x="-60" y="100" width="10" height="10" fill="#5D4037" />
            <rect x="-95" y="90" width="8" height="20" fill="#5D4037" />

            <!-- Right Side connections -->
            <rect x="65" y="60" width="15" height="8" fill="#5D4037" />
            <rect x="55" y="100" width="10" height="10" fill="#5D4037" />
            <rect x="85" y="90" width="8" height="20" fill="#5D4037" />

            <!-- Mid-Deep Crossings -->
            <rect x="-35" y="90" width="20" height="5" fill="#5D4037" />
            <rect x="15" y="90" width="20" height="5" fill="#5D4037" />

            <!-- === FINE ROOT HAIRS (THE CLOUD) === -->
            <g fill="#5D4037" opacity="0.7">
                <rect x="-135" y="155" width="4" height="4" />
                <rect x="-55" y="165" width="4" height="4" />
                <rect x="-28" y="145" width="4" height="4" />

                <rect x="125" y="155" width="4" height="4" />
                <rect x="45" y="165" width="4" height="4" />
                <rect x="18" y="145" width="4" height="4" />

                <!-- Deep Central Hairs -->
                <rect x="-10" y="130" width="3" height="3" />
                <rect x="5" y="130" width="3" height="3" />
            </g>
        </g>

        <!-- === 2. C4 PLANT ROOTS (LEFT) - PIXEL ART === -->
        <g
            transform="translate(-40, 0)"
            class="cursor-alias hover:brightness-125 transition-all hover:scale-110 origin-center"
            style="transform-box: fill-box;"
            on:click|stopPropagation={() => dispatch("openSymbiosisC4")}
            on:keydown|stopPropagation={(e) =>
                e.key === "Enter" && dispatch("openSymbiosisC4")}
            role="button"
            tabindex="0"
            on:mouseenter={() => setHover("Racines C4 (Endomycorhizes)")}
            on:mouseleave={clearHover}
            aria-label="C4 Roots"
        >
            <rect x="-4" y="-10" width="8" height="10" fill="#689F38" />
            <path
                d="M0,0 V20 H4 V30 H8 V40"
                fill="none"
                stroke="#689F38"
                stroke-width="2"
            />
            <path
                d="M0,0 V15 H-4 V25 H-8 V35"
                fill="none"
                stroke="#689F38"
                stroke-width="2"
            />
        </g>

        <!-- === 3. ARBORESCENT MYCORRHIZAL NETWORK (The Web) === -->
        {#if isActive}
            <g class="network-layer" filter="url(#mycoGlow)">
                <!-- Style: Thin Cyan Lines, Branching like a fractal tree -->

                <!-- Main Artery (Restored) -->
                <path
                    d="M60,80 H10 V60 H-20 V40 H-36"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="2 2"
                    class="flow-anim pointer-events-auto hover:stroke-cyan-200 hover:stroke-[2px] transition-all hover:scale-105"
                    style="transform-box: fill-box; transform-origin: center;"
                    on:mouseenter={() =>
                        setHover("Réseau Mycorhizien (Wood Wide Web)")}
                    on:mouseleave={clearHover}
                    role="img"
                    aria-label="Réseau Mycorhizien"
                >
                </path>
                <!-- Branch A1 (Downwards from Artery) -->
                <path
                    d="M10,60 V100 H0 V120 H-10"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="1 3"
                    opacity="0.6"
                />
                <!-- Branch A2 (Upwards from C4) -->
                <path
                    d="M-20,40 V20 H-10"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="1 3"
                    opacity="0.6"
                />

                <!-- CONNECTION B: Deep Soil Exploration (Left) -->
                <!-- From Tree Deep Root (Restored) -->
                <path
                    d="M-8,120 V130 H-30 V140 H60 V180 H20"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="2 2"
                    class="flow-anim delay-1"
                />
                <!-- Branch B1 (Exploration) -->
                <path
                    d="M60,160 V140 H40"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="1 3"
                    opacity="0.6"
                />
                <!-- Branch B2 (Deep) -->
                <path
                    d="M60,180 V200 H80"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="1 3"
                    opacity="0.6"
                />

                <!-- CONNECTION C: Right Expansion -->
                <path
                    d="M240,90 H280 V130 H320"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="2 2"
                    class="flow-anim delay-2"
                />
                <!-- Branch C1 -->
                <path
                    d="M280,110 H300 V100"
                    fill="none"
                    stroke="#5CD6D6"
                    stroke-width="1"
                    stroke-dasharray="1 3"
                    opacity="0.6"
                />

                <!-- NODES (Fungal Colonies / Spore Banks) -->
                <!-- Small squares at intersections -->
                <g
                    class="nodes pointer-events-auto transition-transform hover:scale-110"
                    style="transform-box: fill-box; transform-origin: center;"
                    fill="#A7FFEB"
                    on:mouseenter={() => setHover("Nœuds d'Échange (Symbiose)")}
                    on:mouseleave={clearHover}
                    role="img"
                    aria-label="Nodes"
                >
                    <rect x="8" y="58" width="4" height="4" />
                    <rect x="-22" y="38" width="4" height="4" />
                    <rect x="58" y="158" width="4" height="4" />
                    <rect x="18" y="178" width="4" height="4" />
                    <rect x="278" y="108" width="4" height="4" />
                </g>

                <!-- PARTICLES (Nutrient Packets) -->
                <!-- Moving along the main arteries -->
                <g
                    fill="#FFD54F"
                    class="pointer-events-auto transition-transform hover:scale-110"
                    style="transform-box: fill-box; transform-origin: center;"
                    on:mouseenter={() => setHover("Flux de Carbone (Sucres)")}
                    on:mouseleave={clearHover}
                    role="img"
                    aria-label="Sugar"
                >
                    <!-- Yellow = Carbon/Sugar -->
                    <rect width="3" height="3">
                        <animateMotion
                            path="M60,80 H10 V60 H-20 V40 H-36"
                            dur="3s"
                            repeatCount="indefinite"
                        />
                    </rect>
                </g>
                <g
                    fill="#81D4FA"
                    class="pointer-events-auto transition-transform hover:scale-110"
                    style="transform-box: fill-box; transform-origin: center;"
                    on:mouseenter={() => setHover("Flux d'Azote & Eau")}
                    on:mouseleave={clearHover}
                    role="img"
                    aria-label="Water"
                >
                    <!-- Blue = Water/Nitrogen -->
                    <rect width="3" height="3">
                        <animateMotion
                            path="M36,40 H20 V60 H-10 V80 H-60"
                            dur="4s"
                            repeatCount="indefinite"
                            rotate="auto"
                        />
                    </rect>
                </g>

                <!-- MUSHROOMS -->
                <!-- Biotrophic (Symbiotic) - Left -->
                <g transform="translate(0, -10)">
                    <rect x="-2" y="0" width="4" height="10" fill="#ECEFF1" />
                    <!-- Stalk -->
                    <rect x="-6" y="-4" width="12" height="4" fill="#D32F2F" />
                    <!-- Cap -->
                    <rect
                        x="-4"
                        y="-2"
                        width="2"
                        height="2"
                        fill="white"
                        opacity="0.5"
                    />
                    <!-- Dot -->
                    <rect
                        x="2"
                        y="-3"
                        width="2"
                        height="2"
                        fill="white"
                        opacity="0.5"
                    />
                    <!-- Dot -->
                </g>

                <!-- Biotrophic (Symbiotic) - Right Deep -->
                <g transform="translate(280, -10) scale(0.8)">
                    <rect x="-2" y="0" width="4" height="10" fill="#ECEFF1" />
                    <rect x="-6" y="-4" width="12" height="4" fill="#4CAF50" />
                    <!-- Green Cap for var. -->
                </g>

                <!-- Saprotrophic (Decomposer) - On Tree Trunk -->
                <g transform="translate(180, -12)">
                    <rect x="0" y="0" width="10" height="4" fill="#FFB74D" />
                    <rect x="2" y="4" width="8" height="3" fill="#FFE0B2" />
                    <rect x="4" y="7" width="4" height="2" fill="#FFF3E0" />
                </g>
            </g>
        {/if}
        <!-- === PROTOTYPE V5 ("COMPLEX") (FAR RIGHT) === -->
    </svg>

    <!-- Dynamic Tooltip (Pixel Art Style) -->
    {#if hoveredInfo}
        <div
            class="absolute -top-6 left-1/2 -translate-x-1/2 bg-black text-white text-[10px] px-2 py-1 border border-white/50 shadow-md font-pixel z-50 pointer-events-none whitespace-nowrap"
        >
            {hoveredInfo}
        </div>
    {/if}
</div>

<style>
    @keyframes flow {
        to {
            stroke-dashoffset: -10;
        }
    }
    .flow-anim {
        animation: flow 2s linear infinite;
    }
    .delay-1 {
        animation-delay: 0.7s;
    }
    .delay-2 {
        animation-delay: 1.4s;
    }
</style>
