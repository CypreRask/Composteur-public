<script>
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";
    import { addXp } from "../../lib/progression.js";
    import { onMount } from "svelte";
    import { fly, fade, scale } from "svelte/transition";

    // --- QUESTION POOL ---
    const QUESTIONS = [
        {
            q: "Quel est le ratio C/N idéal ?",
            a: ["10", "30", "100"],
            correct: 1,
            info: "Il faut 30 parts de Carbone pour 1 part d'Azote.",
        },
        {
            q: "Qui mange les feuilles mortes en premier ?",
            a: ["Les Vers", "Les Bactéries", "Les Oiseaux"],
            correct: 1,
            info: "Bactéries et Champignons sont les pionniers.",
        },
        {
            q: "Quelle température tue les pathogènes ?",
            a: ["30°C", "60°C", "100°C"],
            correct: 1,
            info: "La phase thermophile assainit le compost.",
        },
        {
            q: "L'odeur d'oeuf pourri indique...",
            a: ["Trop d'Air", "Manque d'Air", "Bons légumes"],
            correct: 1,
            info: "C'est l'anaérobie (Manque d'Oxygène) qui pue.",
        },
        {
            q: "Que faut-il ajouter si c'est trop sec ?",
            a: ["Verts ou Eau", "Bruns", "Carton"],
            correct: 0,
            info: "Les Verts (Azotés) sont humides.",
        },
        {
            q: "Le 'Thé de Compost' c'est...",
            a: ["Une boisson", "Un engrais liquide", "Sale"],
            correct: 1,
            info: "Un jus concentré en nutriments (Jus de percolation).",
        },
        {
            q: "Un Collembole ça...",
            a: ["Vole", "Saute", "Nage"],
            correct: 1,
            info: "Il a un ressort sous le ventre (la furca) !",
        },
        {
            q: "Peut-on composter des agrumes ?",
            a: ["Jamais", "Oui, en petits morceaux", "Seulement le citron"],
            correct: 1,
            info: "En quantité raisonnable, ça passe très bien.",
        },
        {
            q: "Les vers de terre aiment...",
            a: ["La lumière", "Le noir et l'humidité", "Le feu"],
            correct: 1,
            info: "Ils respirent par la peau, donc il leur faut de l'eau !",
        },
        {
            q: "La phase de maturation sert à...",
            a: ["Refroidir", "Stabiliser", "Rien"],
            correct: 1,
            info: "Le compost se transforme en Humus stable.",
        },
    ];

    // Pick 5 random questions
    let quizSet = [];
    let currentIndex = 0;
    let score = 0;
    let showResult = false;
    let currentFeedback = null; // Correct/Incorrect msg
    let finished = false;

    function startQuiz() {
        quizSet = QUESTIONS.sort(() => 0.5 - Math.random()).slice(0, 5);
        currentIndex = 0;
        score = 0;
        finished = false;
        showResult = false;
    }

    onMount(startQuiz);

    function answer(index) {
        const q = quizSet[currentIndex];
        const isCorrect = index === q.correct;

        if (isCorrect) score++;

        currentFeedback = {
            correct: isCorrect,
            msg: isCorrect ? "EXACT !" : "RATE...",
            info: q.info,
        };

        // Auto advance
        setTimeout(() => {
            currentFeedback = null;
            if (currentIndex < quizSet.length - 1) {
                currentIndex++;
            } else {
                finish();
            }
        }, 3000); // 3s reading time
    }

    function finish() {
        finished = true;
        if (score >= 4) {
            addXp(200, "Diplômé !");
        } else {
            addXp(10, "Participation");
        }
    }

    // --- CERTIFICATE GENERATION ---
    let canvas;

    function downloadCertificate() {
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const W = 800;
        const H = 600;
        canvas.width = W;
        canvas.height = H;

        // Background
        ctx.fillStyle = "#FFF8E1";
        ctx.fillRect(0, 0, W, H);

        // Border
        ctx.strokeStyle = "#5D4037";
        ctx.lineWidth = 20;
        ctx.strokeRect(20, 20, W - 40, H - 40);
        ctx.strokeStyle = "#8D6E63";
        ctx.lineWidth = 5;
        ctx.strokeRect(35, 35, W - 70, H - 70);

        // Text
        ctx.textAlign = "center";
        ctx.fillStyle = "#3E2723";

        // Title
        ctx.font = "bold 60px serif";
        ctx.fillText("DIPLÔME", W / 2, 120);

        ctx.font = "italic 30px serif";
        ctx.fillText("Décerné au Composteur", W / 2, 180);

        // Rank
        ctx.font = "bold 50px monospace"; // Pixel font simulation
        ctx.fillStyle = "#558B2F";
        ctx.fillText(score >= 4 ? "MAÎTRE SHAMAN" : "APPRENTI VER", W / 2, 280);

        // Score
        ctx.fillStyle = "#3E2723";
        ctx.font = "30px sans-serif";
        ctx.fillText(`Score Spirituel: ${score} / 5`, W / 2, 350);
        ctx.font = "italic 20px serif";
        ctx.fillText(
            "Pour avoir maîtrisé les secrets du sol vivant.",
            W / 2,
            400,
        );

        // Date
        ctx.fillStyle = "#000";
        ctx.font = "20px serif";
        ctx.textAlign = "left";
        ctx.fillText(`Fait le ${new Date().toLocaleDateString()}`, 100, 500);

        // Seal (Simple Circle)
        ctx.fillStyle = "#C62828";
        ctx.beginPath();
        ctx.arc(W - 120, 480, 50, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#FFF";
        ctx.font = "12px sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("CERTIFIE", W - 120, 480);
        ctx.fillText("COMPOST", W - 120, 495);

        // Trigger Download
        const link = document.createElement("a");
        link.download = `Diplome_Compost_${new Date().toISOString().split("T")[0]}.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
    }
</script>

<div class="h-full relative font-pixel">
    <RetroWindow
        title="Examen de Certification"
        mode="inline"
        height="h-full"
        width="w-full"
    >
        {#if !finished}
            <!-- QUESTION VIEW -->
            <div
                class="h-full flex flex-col p-4 items-center justify-between"
                in:fade
            >
                <!-- PROGRESS -->
                <div class="w-full h-2 bg-gray-700 rounded-full mb-4">
                    <div
                        class="h-full bg-[#C0CA33] transition-all duration-300"
                        style="width: {(currentIndex / quizSet.length) * 100}%"
                    ></div>
                </div>

                <!-- QUESTION CARD -->
                <div
                    class="bg-[#2E3B20] p-6 rounded-xl border-4 border-[#558B2F] shadow-lg text-center w-full max-w-md relative"
                >
                    <div
                        class="text-4xl absolute -top-6 left-1/2 -translate-x-1/2 bg-[#1A202C] px-2 border-2 border-[#558B2F] rounded-full"
                    >
                        ❓
                    </div>
                    <h3
                        class="text-lg text-white mt-4 min-h-[60px] flex items-center justify-center"
                    >
                        {quizSet[currentIndex]?.q}
                    </h3>

                    <!-- FEEDBACK OVERLAY -->
                    {#if currentFeedback}
                        <div
                            class="absolute inset-0 z-20 flex flex-col items-center justify-center bg-black/95 rounded-lg p-4"
                            transition:fly={{ y: 10 }}
                        >
                            <div
                                class="text-3xl mb-2 {currentFeedback.correct
                                    ? 'text-green-400'
                                    : 'text-red-400'}"
                            >
                                {currentFeedback.msg}
                            </div>
                            <p class="text-sm text-gray-300 italic">
                                {currentFeedback.info}
                            </p>
                        </div>
                    {/if}
                </div>

                <!-- ANSWERS -->
                <div class="grid gap-4 w-full max-w-md mt-6">
                    {#each quizSet[currentIndex]?.a || [] as ans, i}
                        <button
                            class="bg-[#1A202C] border-2 border-gray-600 text-gray-200 p-4 rounded hover:bg-[#3E2723] hover:border-[#FFA000] active:scale-95 transition-all text-left flex items-center gap-4 group"
                            on:click={() => !currentFeedback && answer(i)}
                            disabled={!!currentFeedback}
                        >
                            <span
                                class="w-8 h-8 rounded-full border border-gray-500 flex items-center justify-center font-bold group-hover:bg-[#FFA000] group-hover:text-black"
                            >
                                {["A", "B", "C"][i]}
                            </span>
                            <span>{ans}</span>
                        </button>
                    {/each}
                </div>

                <div class="text-xs text-gray-500 mt-4">
                    Question {currentIndex + 1} / {quizSet.length}
                </div>
            </div>
        {:else}
            <!-- CERTIFICATE VIEW -->
            <div
                class="h-full flex flex-col items-center justify-center p-4 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4IiBoZWlnaHQ9IjgiPgo8cmVjdCB3aWR0aD0iOCIgaGVpZ2h0PSI4IiBmaWxsPSIjRkZGNVjlIi8+PC9zdmc+')] bg-repeat"
                in:scale
            >
                <div
                    class="bg-[#FFF8E1] text-black p-8 border-[10px] border-double border-[#5D4037] shadow-2xl max-w-lg w-full text-center relative rotate-1"
                >
                    <!-- Wax Seal -->
                    <div
                        class="absolute bottom-4 right-4 w-20 h-20 bg-red-800 rounded-full border-4 border-red-900 shadow-inner flex items-center justify-center text-white font-serif italic text-xs rotate-[-15deg]"
                    >
                        Certifié<br />Conforme
                    </div>

                    <h1
                        class="font-serif text-4xl mb-2 text-[#3E2723] uppercase tracking-widest border-b-2 border-black pb-2"
                    >
                        Diplôme
                    </h1>

                    <p class="font-serif italic text-lg mb-6">
                        Décerné au Composteur
                    </p>

                    <div
                        class="text-3xl font-bold font-pixel text-[#558B2F] mb-6"
                    >
                        {score >= 4 ? "MAÎTRE SHAMAN" : "APPRENTI VER"}
                    </div>

                    <p class="mb-4 text-sm">
                        A obtenu le score de <strong>{score} / 5</strong>
                        <br />à l'examen national du sol.
                    </p>

                    {#if score < 4}
                        <div
                            class="text-red-600 font-bold text-xs uppercase mb-4"
                        >
                            Recalé (Min 4/5)
                        </div>
                    {/if}

                    <div
                        class="mt-8 border-t border-black pt-4 flex justify-between text-xs font-serif"
                    >
                        <span>Date: {new Date().toLocaleDateString()}</span>
                        <span>Signature: ________________</span>
                    </div>
                </div>

                <div class="mt-8 flex gap-4">
                    <button
                        class="px-6 py-2 bg-[#558B2F] text-white border-2 border-[#33691E] hover:scale-105 transition-transform shadow-lg"
                        on:click={startQuiz}
                    >
                        {score >= 4
                            ? "Refaire pour le fun"
                            : "Retenter sa chance"}
                    </button>
                    {#if score >= 4}
                        <button
                            class="px-6 py-2 bg-[#FBC02D] text-black border-2 border-[#F57F17] hover:scale-105 transition-transform shadow-lg animate-pulse flex items-center gap-2"
                            on:click={downloadCertificate}
                        >
                            <span>💾</span> Télécharger le Diplôme
                        </button>
                    {/if}
                </div>
                <!-- Hidden Canvas -->
                <canvas bind:this={canvas} class="hidden"></canvas>
            </div>
        {/if}
    </RetroWindow>
</div>
