<script>
    import { createEventDispatcher } from "svelte";

    export let lastTab = "monitor";

    const dispatch = createEventDispatcher();

    const portals = [
        {
            id: "monitor",
            title: "Immersif",
            desc: "Scene vivante + capteurs en temps reel",
            icon: "🎮",
            accent: "bg-emerald-900/70 border-emerald-400",
            glow: "shadow-[0_0_25px_rgba(16,185,129,0.35)]",
        },
        {
            id: "data",
            title: "Donnees",
            desc: "Graphes, historiques et predictions",
            icon: "📊",
            accent: "bg-blue-900/70 border-blue-400",
            glow: "shadow-[0_0_25px_rgba(59,130,246,0.35)]",
        },
        {
            id: "learn",
            title: "Apprendre",
            desc: "Jeux, diaporamas et mini-labos",
            icon: "🧪",
            accent: "bg-purple-900/70 border-purple-400",
            glow: "shadow-[0_0_25px_rgba(168,85,247,0.35)]",
        },
    ];
</script>

<div class="intro-screen min-h-screen w-full flex items-center justify-center bg-[#0b1116] text-white relative overflow-hidden">
    <!-- Decorative layers -->
    <div class="intro-grid absolute inset-0 opacity-30"></div>
    <div class="intro-vignette absolute inset-0"></div>
    <div class="intro-stars absolute inset-0 opacity-50"></div>

    <div class="relative z-10 w-full max-w-6xl px-6 py-12 text-center">
        <div class="inline-flex items-center gap-3 px-4 py-2 bg-black/40 border border-white/10 rounded-full text-[10px] uppercase tracking-[0.3em] text-emerald-200">
            SmartCompost // V2
        </div>

        <h1 class="mt-6 text-4xl md:text-6xl font-pixel text-emerald-300 drop-shadow-[3px_3px_0_rgba(0,0,0,1)]">
            BioCycle Pixel
        </h1>
        <p class="mt-3 text-sm md:text-base text-emerald-100/80 max-w-2xl mx-auto">
            Un composteur vivant, ludique et scientifique. Choisis ton portail.
        </p>

        <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
            {#each portals as portal}
                <button
                    class="portal-card relative group border-4 {portal.accent} {portal.glow} px-6 py-8 rounded-none transition-transform hover:-translate-y-1 hover:scale-[1.02] active:translate-y-0"
                    on:click={() => dispatch("start", { tab: portal.id })}
                >
                    <div class="text-5xl mb-4">{portal.icon}</div>
                    <div class="text-xl font-bold font-pixel text-white">{portal.title}</div>
                    <div class="mt-2 text-xs text-white/70">{portal.desc}</div>

                    {#if portal.id === lastTab}
                        <div class="absolute -top-3 right-3 text-[9px] px-2 py-0.5 bg-black/70 border border-white/20 uppercase tracking-widest">
                            Reprendre
                        </div>
                    {/if}

                    <div class="portal-scanline absolute inset-0 opacity-0 group-hover:opacity-20 pointer-events-none"></div>
                </button>
            {/each}
        </div>

        <div class="mt-10 flex flex-col md:flex-row items-center justify-center gap-3 text-[10px] text-white/60">
            <div class="px-3 py-1 border border-white/10 bg-black/40">Astuce: Mode LABO pour simuler les cycles</div>
            <div class="px-3 py-1 border border-white/10 bg-black/40">Astuce: Toggle Expert dans Apprendre</div>
        </div>
    </div>
</div>

<style>
    .intro-grid {
        background-image:
            linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: 24px 24px;
    }

    .intro-vignette {
        background: radial-gradient(circle at 50% 30%, rgba(16,185,129,0.15), transparent 60%);
    }

    .intro-stars {
        background-image: radial-gradient(rgba(255,255,255,0.25) 1px, transparent 1px);
        background-size: 80px 80px;
    }

    .portal-scanline {
        background: repeating-linear-gradient(
            to bottom,
            rgba(255,255,255,0.2),
            rgba(255,255,255,0.2) 2px,
            transparent 2px,
            transparent 6px
        );
    }
</style>
