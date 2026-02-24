<script>
    import { onMount, createEventDispatcher } from "svelte";
    import { fly, fade, scale } from "svelte/transition";
    const dispatch = createEventDispatcher();

    export let weather = null;
    // Simulation Props
    $: temperature = weather?.main?.temp || 20;

    // --- GAME STATE ---
    let selectedOrganelle = null;

    // Turgor State (3 Levels)
    let turgorState = 80;

    // --- MITOCHONDRIA SIMULATION ENGINE ---
    let mitoState = "idle"; // idle, respiring
    let atpParticles = [];
    let glucoseParticles = [];
    let o2Particles = []; // Oxygen input
    let h2oParticles = []; // Water output
    let respirationRate = 1; // Base rate
    let lastTime = 0;

    // Respiration Logic
    function updateMitochondria(time) {
        if (!time) return;
        const delta = time - lastTime;
        lastTime = time;

        // Rate depends on Temp (Q10 Rule: Rate doubles every 10°C)
        // Q10 ≈ 2 is typical for enzymatic reactions
        const Q10 = 2;
        const T_ref = 20; // Reference temperature
        respirationRate = Math.pow(Q10, (temperature - T_ref) / 10);
        // Clamp to reasonable bounds (0.1x to 4x)
        respirationRate = Math.max(0.1, Math.min(4, respirationRate));

        // Spawn Glucose periodically if Turgid (Photosynthesis active implied)
        if (turgorState > 50 && Math.random() < 0.02 * respirationRate) {
            glucoseParticles.push({
                x: 0, // Starts from chloroplast area
                y: 90,
                targetX: 50,
                targetY: 87,
                life: 100,
            });
        }

        // Spawn O2 (Diffuses in from outside/stomata)
        if (Math.random() < 0.015 * respirationRate) {
            o2Particles.push({
                x: 100, // Enters from right side
                y: 80 + Math.random() * 10,
                targetX: 55,
                targetY: 87,
                life: 80,
            });
        }

        // Process Glucose Particles
        glucoseParticles = glucoseParticles.filter((p) => {
            p.life--;
            const dx = p.targetX - p.x;
            const dy = p.targetY - p.y;
            p.x += dx * 0.05;
            p.y += dy * 0.05;

            if (Math.abs(dx) < 2 && Math.abs(dy) < 2) {
                produceATP();
                return false;
            }
            return p.life > 0;
        });

        // Process O2 Particles
        o2Particles = o2Particles.filter((p) => {
            p.life--;
            const dx = p.targetX - p.x;
            const dy = p.targetY - p.y;
            p.x += dx * 0.04;
            p.y += dy * 0.04;

            // Consumed at mitochondria
            if (Math.abs(dx) < 3 && Math.abs(dy) < 3) {
                return false; // Consumed
            }
            return p.life > 0;
        });

        // Process ATP Particles
        atpParticles = atpParticles.filter((p) => {
            p.life--;
            p.x += p.vx;
            p.y += p.vy;
            return p.life > 0;
        });

        // Process H2O Particles (Output)
        h2oParticles = h2oParticles.filter((p) => {
            p.life--;
            p.x += p.vx;
            p.y += p.vy;
            return p.life > 0;
        });

        // Loop
        requestAnimationFrame(updateMitochondria);
    }

    function produceATP() {
        // Complete respiration event
        mitoState = "respiring";
        setTimeout(() => (mitoState = "idle"), 500 / respirationRate);

        // Spawn ATP Stars (Energy output)
        for (let i = 0; i < 3; i++) {
            atpParticles.push({
                x: 50,
                y: 87,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2 - 1,
                life: 60,
            });
        }

        // Spawn H2O (Water byproduct - final electron acceptor)
        h2oParticles.push({
            x: 50,
            y: 87,
            vx: (Math.random() - 0.5) * 0.5,
            vy: -0.5 - Math.random() * 0.5, // Floats up
            life: 80,
        });
    }

    let showDNA = false;

    // --- NUCLEUS SIMULATION ENGINE ---
    let mrnaParticles = [];
    let ribosomeParticles = []; // Ribosomes doing translation
    let proteinParticles = [];
    let nucleusState = "normal"; // normal, heat_shock, water_stress

    function updateNucleus(time) {
        if (!time) return;

        // 1. Check Environment
        if (temperature > 30) nucleusState = "heat_shock";
        else if (turgorState < 40) nucleusState = "water_stress";
        else nucleusState = "normal";

        // 2. Transcription (Random events based on state)
        if (Math.random() < 0.01) {
            expressGene(nucleusState);
        }

        // 3. Move Particles
        mrnaParticles = mrnaParticles.filter((p) => {
            p.life--;
            p.x += p.vx;
            p.y += p.vy;
            return p.life > 0;
        });

        // Process Ribosomes (they stay in place during translation)
        ribosomeParticles = ribosomeParticles.filter((r) => {
            r.life--;
            r.progress = Math.min(100, r.progress + 2); // Translation progress
            return r.life > 0;
        });

        proteinParticles = proteinParticles.filter((p) => {
            p.life--;
            p.y -= 0.5; // Float up
            return p.life > 0;
        });

        requestAnimationFrame(updateNucleus);
    }

    function expressGene(type) {
        // Spawn mRNA from Nucleus (approx x=75, y=75)
        const mrna = {
            x: 75,
            y: 75,
            vx: -0.5 + Math.random(),
            vy: -0.5 + Math.random(),
            life: 100,
            type: type,
        };
        mrnaParticles.push(mrna);

        // Schedule Ribosome Attachment (delay for mRNA to exit nucleus)
        setTimeout(() => attachRibosome(mrna), 800);
    }

    function attachRibosome(mrna) {
        // Spawn Ribosome at mRNA location
        const ribosome = {
            x: mrna.x + (Math.random() * 10 - 5),
            y: mrna.y + (Math.random() * 10 - 5),
            mrnaType: mrna.type,
            progress: 0, // Translation progress (0-100)
            life: 120,
        };
        ribosomeParticles.push(ribosome);

        // Schedule Protein Production (after translation completes)
        setTimeout(() => produceProtein(ribosome), 1200);
    }

    function produceProtein(ribosome) {
        // Spawn Protein at ribosome location
        const protein = {
            x: ribosome.x + (Math.random() * 5 - 2.5),
            y: ribosome.y,
            type: ribosome.mrnaType,
            life: 150,
        };
        proteinParticles.push(protein);
    }

    onMount(() => {
        requestAnimationFrame(updateMitochondria);
        requestAnimationFrame(updateNucleus);
    });

    // --- BIO-MARKERS ---
    let activeMarker = null;
    const MARKERS = [
        {
            id: "wall",
            x: 5,
            y: 5,
            label: "Paroi Cellulaire",
            text: "L'armure de la cellule ! Une boîte rigide en cellulose.",
        },
        {
            id: "vacuole",
            x: 30,
            y: 30,
            label: "Vacuole",
            text: "Le réservoir d'eau. Pousse sur la paroi pour la rigidité.",
        },
        {
            id: "nucleus",
            x: 75,
            y: 75,
            label: "Noyau",
            text: "Le centre de commande. Contient l'ADN.",
        },
        {
            id: "mito",
            x: 50,
            y: 85,
            label: "Mitochondrie",
            text: "Centrale Électrique : Respiration Cellulaire (Glucose + O2 -> ATP).",
        },
        {
            id: "chloro",
            x: 85,
            y: 20,
            label: "Chloroplaste",
            text: "Usine Solaire : Photosynthèse.",
        },
    ];

    function toggleMarker(marker) {
        if (activeMarker === marker) activeMarker = null;
        else activeMarker = marker;
    }

    // --- LOGIC ---
    function cycleTurgor() {
        if (turgorState >= 80)
            turgorState = 20; // Go to Plasmolysis
        else if (turgorState <= 30)
            turgorState = 50; // Go to Flaccid
        else turgorState = 100; // Go to Turgid

        select("vacuole");
    }

    function toggleNucleus() {
        showDNA = !showDNA;
        select("nucleus");
    }

    // Reactive Descriptions
    $: ORGANELLES = {
        nucleus: {
            name: "NOYAU (ADN)",
            desc: showDNA
                ? "DÉCODAGE EN COURS... L'ADN contient la recette de tout l'arbre !"
                : "Le chef d'orchestre. Cliquez pour voir le Code Génétique.",
            color: "text-pink-400",
        },
        vacuole: {
            name: "VACUOLE (EAU)",
            desc:
                turgorState > 70
                    ? "TURGIDE (Pleine) : La plante est solide ! 😎"
                    : turgorState < 30
                      ? "PLASMOLYSE (Danger) : Manque d'eau critique ! 🥀"
                      : "FLASQUE (Moyen) : Besoin d'eau.",
            color: "text-blue-400",
        },
        mitochondria: {
            name: "MITOCHONDRIE",
            desc: `RESPIRATION : Vitesse ×${respirationRate.toFixed(1)} (Q10). Temp: ${temperature}°C. Consomme du Glucose + O₂ → ATP + CO₂ + H₂O.`,
            color: "text-orange-400",
        },
        wall: {
            name: "PAROI CELLULAIRE",
            desc: "Armure de cellulose rigide.",
            color: "text-green-800",
        },
    };

    function select(org) {
        selectedOrganelle = ORGANELLES[org];
        activeMarker = null;
    }
</script>

<div
    class="w-full h-full relative font-pixel bg-[#81C784] overflow-hidden flex flex-col items-center justify-center p-4 selection:bg-none select-none"
    on:click={() => (activeMarker = null)}
    on:keydown={(e) => e.key === "Escape" && (activeMarker = null)}
    role="presentation"
>
    <!-- HEADER -->
    <div
        class="absolute top-0 left-0 w-full p-2 flex justify-between items-start z-30 pointer-events-none"
    >
        <div class="flex flex-col gap-1 pointer-events-auto">
            <div
                class="bg-black/70 text-white text-xs px-3 py-1 rounded border border-green-800 shadow-md w-fit flex gap-2 items-center"
            >
                <span
                    >Niveau 2 : <span class="text-green-400">STRUCTURAL</span
                    ></span
                >
                <span
                    class="bg-blue-900/50 px-1 rounded border border-blue-500/30 text-[10px] text-blue-200"
                    title="Photosynthèse Standard">TYPE C3</span
                >
            </div>

            <!-- STATE INDICATORS -->
            <div class="flex gap-2 mt-1">
                {#if turgorState < 30}
                    <div
                        class="bg-red-900/80 text-red-200 text-[10px] px-2 py-1 rounded animate-pulse border border-red-500"
                    >
                        ⚠️ DANGER HYDRIQUE
                    </div>
                {/if}
            </div>
        </div>
    </div>

    <!-- MAIN CELL CONTAINER -->
    <div
        class="relative w-[340px] h-[340px] md:scale-125 transition-all duration-1000 ease-in-out"
        style="
            transform: scale(0.95) skewX(2deg);
        "
    >
        <!-- 1. CELL WALL (Rigid Container) -->
        <div
            class="absolute inset-0 border-[16px] border-[#2E7D32] bg-[#4CAF50] shadow-2xl cursor-magnify hover:border-[#388E3C] transition-colors z-0"
            on:click|stopPropagation={() => select("wall")}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && select("wall")}
        ></div>

        <!-- 2. CYTOPLASM (PLASMOLYSIS EFFECT) -->
        <!-- Logic: If turgor is low, scale DOWN the cytoplasm to detach from wall -->
        <div
            class="absolute inset-4 bg-[#A5D6A7]/30 backdrop-blur-[1px] overflow-hidden pointer-events-none transition-all duration-1000 ease-in-out border border-green-800/20"
            style="
                transform: scale({turgorState < 30 ? 0.85 : 1});
                border-radius: {turgorState < 30 ? '40px' : '0px'};
                background-color: {turgorState < 30
                ? 'rgba(165, 214, 167, 0.6)'
                : 'rgba(165, 214, 167, 0.3)'};
             "
        >
            <!-- Floating Particles -->
            {#each Array(15) as _, i}
                <div
                    class="absolute w-1 h-1 bg-white/40 rounded-full animate-float"
                    style="left: {Math.random() * 100}%; top: {Math.random() *
                        100}%; animation-duration: {5 + Math.random() * 10}s"
                ></div>
            {/each}
        </div>

        <!-- 2b. PLASMOLYSIS GAP FILLER (The void) -->
        <!-- Visual trick: showing 'white/yellow' gap between wall and cytoplasm when shrunk -->
        <div
            class="absolute inset-4 -z-10 transition-opacity duration-1000"
            style="background: #FFF9C4; opacity: {turgorState < 30 ? 0.5 : 0};"
        ></div>

        <!-- 3. VACUOLE (Interactive Water Tank) -->
        <div
            class="absolute top-8 left-8 transition-all duration-700 ease-out origin-center border-4 border-[#0288D1]/50 cursor-magnify group z-10"
            style="
                width: {turgorState < 30
                ? 100
                : turgorState > 80
                  ? 220
                  : 180}px; 
                height: {turgorState < 30
                ? 80
                : turgorState > 80
                  ? 200
                  : 150}px; 
                background-color: rgba(79, 195, 247, {turgorState / 150});
                border-radius: {turgorState < 30
                ? '50%'
                : '40% 60% 70% 30% / 40% 50% 60% 50%'};
                transform: translate({turgorState < 30
                ? 30
                : 0}px, {turgorState < 30 ? 30 : 0}px);
             "
            on:click|stopPropagation={cycleTurgor}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && cycleTurgor}
        >
            <div
                class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-[#01579B] text-[10px] uppercase font-bold opacity-80 pointer-events-none"
            >
                {turgorState > 80
                    ? "H₂O MAX"
                    : turgorState < 30
                      ? "VIDE"
                      : "H₂O"}
            </div>

            {#if turgorState < 30}
                <div
                    class="absolute -top-6 left-0 bg-red-500 text-white text-[8px] px-1 rounded animate-bounce"
                >
                    CLIQUEZ POUR ARROSER !
                </div>
            {/if}
        </div>

        <!-- 4. NUCLEUS (Scientific Control Center) -->
        <div
            class="absolute bottom-6 right-8 w-24 h-24 border-4 rounded-full shadow-lg z-20 cursor-magnify hover:scale-110 active:scale-95 transition-transform flex items-center justify-center overflow-visible group"
            class:bg-green-600={nucleusState === "normal"}
            class:border-green-800={nucleusState === "normal"}
            class:bg-red-600={nucleusState === "heat_shock"}
            class:border-red-800={nucleusState === "heat_shock"}
            class:bg-blue-600={nucleusState === "water_stress"}
            class:border-blue-800={nucleusState === "water_stress"}
            on:click|stopPropagation={toggleNucleus}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && toggleNucleus}
        >
            <!-- Pulsing Core -->
            <div
                class="w-16 h-16 rounded-full opacity-50 animate-pulse"
                class:bg-green-400={nucleusState === "normal"}
                class:bg-red-400={nucleusState === "heat_shock"}
                class:bg-blue-400={nucleusState === "water_stress"}
            ></div>

            <!-- DNA VISUAL (Scientific Double Helix) -->
            {#if showDNA}
                <div
                    class="absolute -top-32 -left-32 w-48 h-32 bg-black/90 rounded border border-pink-500 p-2 z-50 pointer-events-none"
                    in:scale
                >
                    <div
                        class="text-[8px] text-pink-300 mb-1 border-b border-pink-800 pb-1 flex justify-between"
                    >
                        <span>🧬 ADN (Séquence)</span>
                        <span class="animate-pulse">LECTURE...</span>
                    </div>
                    <!-- SVG Double Helix Animation -->
                    <div
                        class="relative w-full h-20 overflow-hidden flex items-center justify-center"
                    >
                        <svg
                            viewBox="0 0 100 40"
                            class="w-full h-full text-pink-500"
                        >
                            <!-- Strand 1 -->
                            <path
                                d="M0,20 Q10,0 20,20 T40,20 T60,20 T80,20 T100,20"
                                fill="none"
                                stroke="currentColor"
                                stroke-width="2"
                                class="animate-helix-1"
                            />
                            <!-- Strand 2 -->
                            <path
                                d="M0,20 Q10,40 20,20 T40,20 T60,20 T80,20 T100,20"
                                fill="none"
                                stroke="#4FC3F7"
                                stroke-width="2"
                                class="animate-helix-2"
                            />
                            <!-- Base Pairs -->
                            {#each [10, 30, 50, 70, 90] as x}
                                <line
                                    x1={x}
                                    y1="10"
                                    x2={x}
                                    y2="30"
                                    stroke="white"
                                    stroke-width="1"
                                    stroke-dasharray="2"
                                    opacity="0.5"
                                />
                            {/each}
                        </svg>
                    </div>
                </div>
            {/if}

            <span class="text-white text-[8px] font-bold z-10 drop-shadow-md"
                >ADN</span
            >

            <!-- State Label -->
            <div
                class="absolute -bottom-4 text-[8px] bg-black/50 px-1 rounded text-white whitespace-nowrap"
            >
                {#if nucleusState === "heat_shock"}🔥 STRESS THERMIQUE
                {:else if nucleusState === "water_stress"}💧 STRESS HYDRIQUE
                {:else}✨ NORMAL
                {/if}
            </div>
        </div>

        <!-- PROTEIN SYNTHESIS LAYER -->
        <!-- mRNA (Pink strand) -->
        {#each mrnaParticles as p}
            <div
                class="absolute w-4 h-1 bg-pink-300 rounded-full animate-snake"
                style="left: {p.x}%; top: {p.y}%; transform: rotate({Math.random() *
                    360}deg);"
            ></div>
        {/each}

        <!-- Ribosomes (Translation machinery - small dark circles) -->
        {#each ribosomeParticles as r}
            <div
                class="absolute w-3 h-3 bg-gray-700 rounded-full border border-gray-500 pointer-events-none z-25 flex items-center justify-center"
                style="left: {r.x}%; top: {r.y}%; opacity: {r.life / 120};"
                title="Ribosome (Translation)"
            >
                <div
                    class="w-1 h-1 bg-pink-300 rounded-full animate-pulse"
                ></div>
            </div>
        {/each}

        <!-- Proteins (Final product) -->
        {#each proteinParticles as p}
            <div
                class="absolute text-xs pointer-events-none z-30 animate-pop-in"
                style="left: {p.x}%; top: {p.y}%;"
            >
                {#if p.type === "heat_shock"}🛡️
                {:else if p.type === "water_stress"}🚰
                {:else}🧱
                {/if}
            </div>
        {/each}

        <!-- 5. CHLOROPLASTS (Interactive Zoom) -->
        <div
            class="absolute top-4 right-6 w-20 h-12 bg-[#1B5E20] border-2 border-[#66BB6A] rounded-[50%] rotate-12 z-20 cursor-magnify hover:scale-110 hover:bg-[#2E7D32] transition-all shadow-[0_0_15px_rgba(76,175,80,0.6)] animate-pulse-slow flex items-center justify-center group"
            on:click|stopPropagation={() => dispatch("openChloroplast")}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && dispatch("openChloroplast")}
        >
            <div class="flex gap-[2px]">
                <div class="w-1 h-8 bg-[#388E3C] rounded-full"></div>
                <div class="w-1 h-8 bg-[#388E3C] rounded-full"></div>
                <div class="w-1 h-8 bg-[#388E3C] rounded-full"></div>
            </div>
            <div
                class="absolute -bottom-4 bg-black/80 text-green-300 text-[8px] px-1 rounded opacity-0 group-hover:opacity-100 transition-opacity"
            >
                ENTRER
            </div>
        </div>

        <!-- 6. MITOCHONDRIA (Scientific Simulation) -->
        <div
            class="absolute bottom-4 left-1/2 w-16 h-10 bg-[#E65100] border-2 border-[#FFE0B2] rounded-full z-10 hover:scale-110 transition-transform shadow-lg overflow-visible"
            on:click|stopPropagation={() => select("mitochondria")}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Enter" && select("mitochondria")}
        >
            <!-- Pulsing Cristae (Respiration Visual) -->
            <svg
                viewBox="0 0 40 20"
                class="w-full h-full opacity-80"
                style="animation: pulseCristae {1 /
                    respirationRate}s infinite alternate ease-in-out;"
            >
                <path
                    d="M5,10 C10,5 10,15 15,10 C20,5 20,15 25,10 C30,5 30,15 35,10"
                    fill="none"
                    stroke="#FFE0B2"
                    stroke-width="2"
                />
            </svg>

            <!-- CO2 Bubbles Exiting -->
            {#if mitoState === "respiring"}
                <div
                    class="absolute -right-2 top-0 text-[8px] text-gray-300 font-bold animate-fade-up"
                >
                    CO₂
                </div>
            {/if}
        </div>

        <!-- PARTICLES LAYER (Glucose & ATP) -->
        <!-- GLUCOSE -->
        {#each glucoseParticles as p}
            <div
                class="absolute w-2 h-2 bg-white rotate-45 border border-gray-300 shadow-sm z-0 pointer-events-none"
                style="left: {p.x}%; top: {p.y}%; opacity: {p.life /
                    100}; transition: all 0.1s linear;"
            ></div>
        {/each}

        <!-- ATP -->
        {#each atpParticles as p}
            <div
                class="absolute text-[8px] pointer-events-none z-20"
                style="left: {p.x}%; top: {p.y}%; opacity: {p.life / 60};"
            >
                ⭐
            </div>
        {/each}

        <!-- O2 (Oxygen Input - Blue circles) -->
        {#each o2Particles as p}
            <div
                class="absolute w-2 h-2 bg-blue-400 rounded-full border border-blue-200 pointer-events-none z-0"
                style="left: {p.x}%; top: {p.y}%; opacity: {p.life /
                    80}; transition: all 0.1s linear;"
            ></div>
        {/each}

        <!-- H2O (Water Output - Droplets) -->
        {#each h2oParticles as p}
            <div
                class="absolute text-[10px] pointer-events-none z-20"
                style="left: {p.x}%; top: {p.y}%; opacity: {p.life / 80};"
            >
                💧
            </div>
        {/each}

        <!-- BIO-MARKERS OVERLAY -->
        <!-- Placed ON TOP of organelles via z-index -->
        {#each MARKERS as m}
            <button
                class="absolute w-5 h-5 bg-yellow-400 text-black border border-white rounded-full flex items-center justify-center text-[10px] font-bold shadow-lg hover:scale-110 transition-transform z-40 animate-bounce-slight"
                style="left: {m.x}%; top: {m.y}%; animation-delay: {Math.random()}s"
                on:click|stopPropagation={() => toggleMarker(m)}
            >
                ?
            </button>
        {/each}
    </div>

    <!-- MARKER TOOLTIP POPUP -->
    {#if activeMarker}
        <div
            class="absolute bottom-16 left-1/2 -translate-x-1/2 w-[90%] md:w-[60%] bg-black/90 border-2 border-yellow-400 p-4 rounded-xl shadow-2xl z-50 text-white"
            transition:fly={{ y: 20, duration: 200 }}
        >
            <div class="flex justify-between items-start mb-2">
                <h3 class="text-yellow-400 font-bold text-sm uppercase">
                    {activeMarker.label}
                </h3>
                <button
                    class="text-gray-400 hover:text-white"
                    on:click|stopPropagation={() => (activeMarker = null)}
                    >✖</button
                >
            </div>
            <p class="text-xs text-gray-200 leading-relaxed font-sans">
                {activeMarker.text}
            </p>
        </div>
    {/if}

    <!-- INFO POPUP (Legacy interaction) -->
    <!-- Only show if no marker is active to avoid clutter -->
    {#if selectedOrganelle && !activeMarker}
        <div
            class="absolute bottom-0 left-0 w-full bg-[#1A202C]/95 border-t-4 border-green-600 p-4 text-white z-50 shadow-[0_-5px_20px_rgba(0,0,0,0.5)]"
            transition:fly={{ y: 50, duration: 200 }}
        >
            <div class="flex justify-between items-center mb-2">
                <h3 class="font-bold text-lg {selectedOrganelle.color}">
                    {selectedOrganelle.name}
                </h3>
                <button
                    class="text-gray-400 hover:text-white"
                    on:click={() => (selectedOrganelle = null)}>✖</button
                >
            </div>
            <p class="text-sm text-gray-300 leading-relaxed font-sans">
                {selectedOrganelle.desc}
            </p>
        </div>
    {:else if !selectedOrganelle && !activeMarker}
        <div
            class="absolute bottom-4 text-center pointer-events-none opacity-80"
            in:fade
        >
            <p class="text-xs text-green-900 bg-white/60 px-2 py-1 rounded">
                👇 Cliquez sur les éléments pour interagir, ou sur (?) pour
                comprendre.
            </p>
        </div>
    {/if}
</div>

<style>
    .animate-float {
        animation: float 8s ease-in-out infinite;
    }
    .animate-pulse-slow {
        animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    .animate-vibrate {
        animation: vibrate 0.1s linear infinite;
    }
    .animate-spark {
        animation: spark 0.5s linear infinite;
    }
    .animate-bounce-slight {
        animation: bounceSlight 2s infinite ease-in-out;
    }
    @keyframes bounceSlight {
        0%,
        100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-3px);
        }
    }

    .animate-helix-1 {
        animation: helix 2s linear infinite;
    }
    .animate-helix-2 {
        animation: helix 2s linear infinite reverse;
    }

    @keyframes helix {
        0% {
            transform: translateY(-2px);
        }
        50% {
            transform: translateY(2px);
        }
        100% {
            transform: translateY(-2px);
        }
    }

    @keyframes float {
        0%,
        100% {
            transform: translate(0, 0);
        }
        50% {
            transform: translate(10px, -20px);
        }
    }
    @keyframes pulse {
        0%,
        100% {
            opacity: 1;
            transform: scale(1) rotate(12deg);
        }
        50% {
            opacity: 0.9;
            transform: scale(1.05) rotate(12deg);
        }
    }
    @keyframes vibrate {
        0% {
            transform: translate(0);
        }
        20% {
            transform: translate(-2px, 2px);
        }
        40% {
            transform: translate(-2px, -2px);
        }
        60% {
            transform: translate(2px, 2px);
        }
        80% {
            transform: translate(2px, -2px);
        }
        100% {
            transform: translate(0);
        }
    }
    @keyframes spark {
        0% {
            opacity: 1;
            transform: scale(0) translate(0, 0);
        }
        100% {
            opacity: 0;
            transform: scale(2) translate(10px, -10px);
        }
    }
    @keyframes floatUp {
        0% {
            transform: translateY(0) translateX(-50%);
            opacity: 1;
        }
        100% {
            transform: translateY(-20px) translateX(-50%);
            opacity: 0;
        }
    }
    @keyframes pulseCristae {
        0% {
            transform: scale(0.95);
            opacity: 0.7;
        }
        100% {
            transform: scale(1.05);
            opacity: 1;
        }
    }
    @keyframes fadeUp {
        0% {
            transform: translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateY(-10px);
            opacity: 0;
        }
    }
    @keyframes snake {
        0% {
            transform: scaleX(0);
            opacity: 0;
        }
        50% {
            transform: scaleX(1);
            opacity: 1;
        }
        100% {
            transform: scaleX(0) translate(20px, 20px);
            opacity: 0;
        }
    }
    @keyframes pop-in {
        0% {
            transform: scale(0);
        }
        80% {
            transform: scale(1.2);
        }
        100% {
            transform: scale(1);
        }
    }
</style>
