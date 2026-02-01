<script>
    import { onMount, onDestroy } from "svelte";

    export let temp = 20;
    // svelte-ignore unused-export-let
    export let humidity = 50;

    let canvas;
    let ctx;
    let animationId;

    // Simulation State
    let particles = [];
    let showInfo = false; // Toggle for Analysis Panel

    class Microbe {
        constructor(w, h, type) {
            this.x = Math.random() * w;
            this.y = Math.random() * h;
            this.type = type; // 'bacteria', 'fungi', 'actinomycetes'

            // Movement vectors
            this.angle = Math.random() * Math.PI * 2;
            const speed = type === "bacteria" ? 0.5 : 0.1;
            this.vx = Math.cos(this.angle) * speed;
            this.vy = Math.sin(this.angle) * speed;

            this.size = type === "bacteria" ? 1 : 2;

            // Retro Colors
            if (type === "bacteria")
                this.color = "#4CAF50"; // Green
            else if (type === "fungi")
                this.color = "#FFF9C4"; // White/Yellow
            else this.color = "#FF7043"; // Orange

            this.timer = Math.random() * 100;
        }

        update(w, h, temp) {
            this.timer++;

            // Random twitch movement
            if (Math.random() < 0.05) {
                this.angle += Math.random() - 0.5;
                const speed = this.type === "bacteria" ? 0.5 : 0.1;
                this.vx = Math.cos(this.angle) * speed;
                this.vy = Math.sin(this.angle) * speed;
            }

            // Temperature Multiplier
            const tempFactor = Math.max(0.5, temp / 20);
            this.x += this.vx * tempFactor;
            this.y += this.vy * tempFactor;

            // Wrap around
            if (this.x < 0) this.x = w;
            if (this.x > w) this.x = 0;
            if (this.y < 0) this.y = h;
            if (this.y > h) this.y = 0;
        }

        draw(ctx) {
            ctx.fillStyle = this.color;
            // Draw square for pixel art look
            ctx.fillRect(
                Math.floor(this.x),
                Math.floor(this.y),
                this.size,
                this.size,
            );

            // Draw tail/filament for fungi
            if (this.type === "fungi") {
                ctx.fillStyle = "rgba(255, 249, 196, 0.3)";
                ctx.fillRect(
                    Math.floor(this.x - this.vx * 5),
                    Math.floor(this.y - this.vy * 5),
                    1,
                    1,
                );
            }
        }
    }

    function initSimulation() {
        if (!canvas) return;
        const w = canvas.width;
        const h = canvas.height;
        particles = [];

        const isHot = temp > 45;

        // Spawn Logic
        // Hot -> More Thermophiles (Actinomycetes)
        // Cold -> Mesophiles (Bacteria, Fungi)

        const count = 80;

        for (let i = 0; i < count; i++) {
            let type = "bacteria";
            const r = Math.random();

            if (isHot) {
                // Thermophilic profile
                if (r > 0.6) type = "actinomycetes";
                else type = "bacteria";
            } else {
                // Mesophilic profile
                if (r > 0.8) type = "fungi";
                else if (r > 0.9) type = "actinomycetes";
                else type = "bacteria";
            }

            particles.push(new Microbe(w, h, type));
        }
    }

    function loop() {
        if (!ctx) return;
        const w = canvas.width;
        const h = canvas.height;

        // Clear with slight trail effect (Dark Humus Background)
        ctx.fillStyle = "rgba(26, 16, 14, 0.2)";
        ctx.fillRect(0, 0, w, h);

        particles.forEach((p) => {
            p.update(w, h, temp);
            p.draw(ctx);
        });

        // Vignette / Overlay effect baked in canvas?
        // Let's do it via CSS overlay for performance

        animationId = requestAnimationFrame(loop);
    }

    onMount(() => {
        ctx = canvas.getContext("2d");
        // Low resolution for true pixel art zoom effect
        canvas.width = 160;
        canvas.height = 120;

        // Disable smoothing
        ctx.imageSmoothingEnabled = false;

        initSimulation();
        loop();
    });

    onDestroy(() => {
        cancelAnimationFrame(animationId);
    });

    // React to props changes (Re-init if temp class changes significantly?)
    let oldTempClass = "cold";
    $: {
        const newTempClass = temp > 45 ? "hot" : "cold";
        if (newTempClass !== oldTempClass) {
            oldTempClass = newTempClass;
            initSimulation();
        }
    }
</script>

<div
    class="w-full h-full relative bg-[#1A100E] overflow-hidden group cursor-help"
    on:click={() => (showInfo = !showInfo)}
    on:keydown={(e) => e.key === "Enter" && (showInfo = !showInfo)}
    tabindex="0"
    role="button"
    aria-label="Toggle Microscope Info"
>
    <!-- SCAN LINES -->
    <div
        class="absolute inset-0 z-20 pointer-events-none bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPjxyZWN0IHdpZHRoPSI0IiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAiIG9wYWNpdHk9IjAuMSIvPjwvc3ZnPg==')] opacity-50"
    ></div>

    <!-- CANVAS -->
    <canvas
        bind:this={canvas}
        class="w-full h-full image-pixelated scale-[2] origin-center opacity-80"
        class:blur-sm={showInfo}
    ></canvas>

    <!-- HUD OVERLAY (Microscope Lens UI) -->
    <div
        class="absolute inset-0 z-30 pointer-events-none border-[20px] border-black/80 rounded-full scale-110 transition-all"
        class:border-black={showInfo}
    ></div>

    <!-- CROSSHAIR -->
    {#if !showInfo}
        <div
            class="absolute inset-0 z-30 pointer-events-none flex items-center justify-center"
        >
            <div class="w-4 h-4 border border-white/20 opacity-50"></div>
            <div class="absolute w-[100%] h-[1px] bg-white/10"></div>
            <div class="absolute h-[100%] w-[1px] bg-white/10"></div>
        </div>
    {/if}

    <!-- INFO TAG (Always visible unless info open) -->
    {#if !showInfo}
        <div
            class="absolute bottom-2 right-2 z-40 text-[8px] font-pixel text-green-500 bg-black/80 px-2 py-1 border border-green-800 rounded animate-pulse"
        >
            [CLIQUEZ POUR ANALYSE]
        </div>
    {/if}

    <!-- ANALYSIS / BESTIARY OVERLAY -->
    {#if showInfo}
        <div
            class="absolute inset-4 z-50 bg-black/90 border-2 border-green-600 p-2 text-green-400 font-pixel text-[10px] flex flex-col gap-2 overflow-y-auto shadow-lg"
        >
            <h3 class="bg-green-900 text-white px-1 text-center font-bold">
                SYSTÈME D'ANALYSE
            </h3>

            <!-- CONTEXT -->
            <div class="border-b border-green-800 pb-2">
                <p class="text-white mb-1">> CAPTEUR ACTIVE</p>
                <p class="opacity-80 leading-tight">
                    Le boîtier bleu contient des sondes mesurant l'activité
                    métabolique de ces organismes.
                </p>
            </div>

            <!-- THE BEASTIES -->
            <div>
                <p class="text-white mb-1">
                    > POPULATION ({temp > 45 ? "THERMOPHILE" : "MÉSOPHILE"})
                </p>
                <ul class="flex flex-col gap-2 mt-1">
                    {#if temp > 45}
                        <!-- THERMO -->
                        <li class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-[#FF7043]"></div>
                            <div>
                                <span class="text-orange-300 font-bold"
                                    >Actinomycètes</span
                                >
                                <p class="opacity-70 text-[8px]">
                                    Dégradent la matière dure (bois) à haute
                                    température.
                                </p>
                            </div>
                        </li>
                        <li class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-[#4CAF50]"></div>
                            <div>
                                <span class="text-green-300 font-bold"
                                    >Bacillus spp.</span
                                >
                                <p class="opacity-70 text-[8px]">
                                    Bactéries résistantes à la chaleur.
                                </p>
                            </div>
                        </li>
                    {:else}
                        <!-- MESO -->
                        <li class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-[#4CAF50]"></div>
                            <div>
                                <span class="text-green-300 font-bold"
                                    >Bactéries Mésophiles</span
                                >
                                <p class="opacity-70 text-[8px]">
                                    Démarrent la décomposition des déchets mous.
                                </p>
                            </div>
                        </li>
                        <li class="flex items-center gap-2">
                            <div class="w-2 h-2 bg-[#FFF9C4]"></div>
                            <div>
                                <span class="text-yellow-100 font-bold"
                                    >Champignons</span
                                >
                                <p class="opacity-70 text-[8px]">
                                    Tissent du mycélium pour lier la matière.
                                </p>
                            </div>
                        </li>
                    {/if}
                </ul>
            </div>
        </div>
    {/if}
</div>

<style>
    .image-pixelated {
        image-rendering: pixelated;
    }
</style>
