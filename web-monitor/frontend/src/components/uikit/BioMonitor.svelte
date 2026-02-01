<script>
    export let latest = {};
    export let heuristic = {};

    // Determine Biological State & Adjectives
    let bioState = "SYMBIOSIS";
    let message = "Colonie stable.";

    // Simple narrative helpers
    let tempAdj = "Normal";
    let humAdj = "Normal";
    let gasTrend = "Stable ➡";

    // French mapping for technical states
    const stateLabels = {
        SYMBIOSIS: "Symbiose (Optimale) 🌱",
        HYPOXIA: "Hypoxie (Manque d'air) 💨",
        STRESS: "Stress Thermique 🔥",
        DORMANCY: "Dormance (Froid) ❄️",
        HUNGER: "Faim (Carence) 🍽️",
        WAITING: "Analyse...",
    };

    $: {
        if (!latest || !heuristic) {
            bioState = "WAITING";
            message = "Analyse en cours...";
        } else {
            const temp = latest.temp_scd || 0;
            const hum = latest.hum_scd || 0;
            const ch4 = latest.mq4 || 0;
            const score = heuristic.score || 50;

            // Temp Narrative
            if (temp < 20) tempAdj = "Froid ❄️";
            else if (temp < 45) tempAdj = "Tiède 🌡️";
            else if (temp < 65) tempAdj = "Chaud 🔥";
            else tempAdj = "Brûlant ⚠️";

            // Hum Narrative
            if (hum < 40) humAdj = "Sec 🌵";
            else if (hum > 70) humAdj = "Trop Humide 💧";
            else humAdj = "Idéal 💧";

            // Gas Trend
            if (ch4 > 200) gasTrend = "Anormal (Méthane) ↗";
            else if (temp > 40) gasTrend = "Actif (CO2) ↗";
            else gasTrend = "Calme ➡";

            // Global State
            if (ch4 > 200) {
                bioState = "HYPOXIA";
                message = "Le composteur manque d'air.";
            } else if (temp > 65) {
                bioState = "STRESS";
                message = "Activité bactérienne intense (Surchauffe).";
            } else if (score < 40) {
                bioState = "HUNGER";
                message = "Le régime est déséquilibré.";
            } else {
                bioState = "SYMBIOSIS";
                message = "L'écosystème est en pleine forme.";
            }
        }
    }
</script>

<div
    class="w-full h-full flex flex-col items-center justify-center p-8 bg-[#2d1b18] border-8 border-[#558B2F]"
>
    <!-- MAIN STATUS (Big Text) -->
    <div class="text-center mb-8 mt-4 relative z-50">
        <h2
            class="text-3xl md:text-5xl font-black text-[#C0CA33] mb-4 uppercase tracking-wider drop-shadow-md leading-snug max-w-4xl mx-auto"
        >
            {message}
        </h2>
        <div
            class="inline-flex items-center gap-2 bg-[#3E2723] px-4 py-2 rounded-full border border-[#5d4037] shadow-sm relative"
        >
            <span
                class="text-[#8d6e63] text-sm font-mono uppercase tracking-widest"
                >État :</span
            >
            <span class="text-[#FFF8E1] font-bold uppercase"
                >{stateLabels[bioState] || bioState}</span
            >
            <div class="group relative ml-2 cursor-help">
                <span
                    class="text-[#C0CA33] font-bold border border-[#C0CA33] rounded-full w-5 h-5 flex items-center justify-center text-xs"
                    >?</span
                >
                <!-- Tooltip opening DOWN now to avoid being cut off top -->
                <div
                    class="absolute top-full left-1/2 -translate-x-1/2 mt-2 w-64 bg-[#2d1b18] border border-[#C0CA33] p-3 text-xs text-[#FFF8E1] hidden group-hover:block z-[100] shadow-xl text-left"
                >
                    <strong>Diagnostic :</strong><br />
                    Ceci est l'état de santé global de la colonie bactérienne, calculé
                    à partir de la température et des gaz.
                </div>
            </div>
        </div>
    </div>

    <!-- METRICS SUMMARY (Grid) -->
    <div
        class="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-5xl px-4 relative z-0"
    >
        <!-- TEMP CARD -->
        <div
            class="bg-[#3E2723] p-5 border-2 border-[#558B2F] shadow-[4px_4px_0_rgba(0,0,0,0.5)] flex items-center justify-between group hover:border-[#C0CA33] transition-colors"
        >
            <div>
                <div
                    class="text-[#8d6e63] text-xs font-bold uppercase mb-1 tracking-wider group-hover:text-[#C0CA33]"
                >
                    Température
                </div>
                <div class="text-3xl text-[#FFF8E1] font-bold font-mono">
                    {latest?.temp_scd?.toFixed(1) || "--"}°C
                </div>
            </div>
            <div
                class="text-lg text-[#C0CA33] font-bold bg-[#1a100e] px-3 py-1 rounded border border-[#C0CA33]/30"
            >
                {tempAdj}
            </div>
        </div>

        <!-- HUM CARD -->
        <div
            class="bg-[#3E2723] p-5 border-2 border-[#558B2F] shadow-[4px_4px_0_rgba(0,0,0,0.5)] flex items-center justify-between group hover:border-[#06b6d4] transition-colors"
        >
            <div>
                <div
                    class="text-[#8d6e63] text-xs font-bold uppercase mb-1 tracking-wider group-hover:text-[#06b6d4]"
                >
                    Humidité
                </div>
                <div class="text-3xl text-[#FFF8E1] font-bold font-mono">
                    {latest?.hum_scd?.toFixed(0) || "--"}%
                </div>
            </div>
            <div
                class="text-lg text-[#06b6d4] font-bold bg-[#1a100e] px-3 py-1 rounded border border-[#06b6d4]/30"
            >
                {humAdj}
            </div>
        </div>

        <!-- GAS CARD -->
        <div
            class="bg-[#3E2723] p-5 border-2 border-[#558B2F] shadow-[4px_4px_0_rgba(0,0,0,0.5)] flex items-center justify-between group hover:border-[#22c55e] transition-colors"
        >
            <div>
                <div
                    class="text-[#8d6e63] text-xs font-bold uppercase mb-1 tracking-wider group-hover:text-[#22c55e]"
                >
                    Activité des Gaz
                </div>
                <div class="text-3xl text-[#FFF8E1] font-bold font-mono">
                    CO2 / NH3
                </div>
            </div>
            <div
                class="text-lg text-[#22c55e] font-bold bg-[#1a100e] px-3 py-1 rounded border border-[#22c55e]/30"
            >
                {gasTrend}
            </div>
        </div>

        <!-- PH CARD -->
        <div
            class="bg-[#3E2723] p-5 border-2 border-[#558B2F] shadow-[4px_4px_0_rgba(0,0,0,0.5)] flex items-center justify-between group hover:border-orange-500 transition-colors"
        >
            <div>
                <div
                    class="text-[#8d6e63] text-xs font-bold uppercase mb-1 tracking-wider group-hover:text-orange-500"
                >
                    Acidité (pH)
                </div>
                <div class="text-3xl text-[#FFF8E1] font-bold font-mono">
                    {latest?.soil_ph?.toFixed(1) || "7.0"}
                </div>
            </div>
            <div
                class="text-lg text-orange-500 font-bold bg-[#1a100e] px-3 py-1 rounded border border-orange-500/30"
            >
                {latest?.soil_ph < 6
                    ? "Acide"
                    : latest?.soil_ph > 8
                      ? "Basique"
                      : "Neutre"}
            </div>
        </div>
    </div>

    <!-- CALL TO ACTION (Expert Mode) -->
    <div class="mt-12 animate-bounce">
        <div
            class="text-[#8d6e63] text-xs mb-2 uppercase tracking-wide font-bold"
        >
            Pour plus de détails :
        </div>
        <div
            class="bg-[#558B2F] text-[#2d1b18] px-6 py-2 font-bold text-lg uppercase shadow-[4px_4px_0_rgba(0,0,0,0.5)] border-2 border-[#1a100e] inline-block hover:scale-105 transition-transform cursor-pointer"
        >
            ⬇ Vue Scientifique ⬇
        </div>
    </div>
</div>

<style>
    /* No custom animations needed for this clean text view */
    /* But if we kept the bounce on the footer: */
    @keyframes bounce {
        0%,
        100% {
            transform: translateY(-3%);
        }
        50% {
            transform: translateY(0);
        }
    }
</style>
