<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    const GAMES = [
        {
            id: "microscope",
            title: "Microscope",
            icon: "🔬",
            desc: "Explorer la vie invisible",
            color: "bg-blue-900 border-blue-600",
            type: "TOOL",
        },
        {
            id: "sorter",
            title: "Le Trieur Fou",
            icon: "♻️",
            desc: "Arcade : Trie les déchets !",
            color: "bg-green-900 border-green-600",
            type: "GAME",
        },
        {
            id: "cycle",
            title: "Architecte du Sol",
            icon: "🏗️",
            desc: "Construis ton écosystème",
            color: "bg-yellow-900 border-yellow-600",
            type: "GAME",
        },
        {
            id: "chemistry",
            title: "Labo Chimie",
            icon: "⚗️",
            desc: "Pizzles Moléculaires (C/N)",
            color: "bg-purple-900 border-purple-600",
            type: "GAME",
        },
        {
            id: "foodweb",
            title: "Le Festin du Sol",
            icon: "🕸️",
            desc: "Chaîne Trophique (Relier)",
            color: "bg-orange-900 border-orange-600",
            type: "GAME",
        },
        {
            id: "quiz",
            title: "Quiz Final",
            icon: "🎓",
            desc: "Certification & Diplôme",
            color: "bg-gray-800 border-gray-500",
            type: "QUIZ",
        },
    ];
</script>

<div class="h-full flex flex-col items-center justify-center space-y-8 p-4">
    <header class="text-center space-y-2">
        <h2 class="text-4xl text-[#C0CA33] drop-shadow-md">COMPOST ARCADE</h2>
        <p class="text-sm text-gray-400">Choisis ton activité</p>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
        {#each GAMES as game}
            <button
                class="relative group h-64 flex flex-col items-center justify-center p-6 border-4 {game.color} rounded-lg hover:scale-105 hover:-translate-y-2 transition-all shadow-xl bg-opacity-80 backdrop-blur-sm"
                on:click={() => dispatch("select", game.id)}
            >
                <div
                    class="text-6xl mb-4 group-hover:scale-110 transition-transform duration-300"
                >
                    {game.icon}
                </div>
                <h3 class="text-xl font-bold text-white mb-2">{game.title}</h3>
                <p class="text-xs text-center text-gray-300 mb-4">
                    {game.desc}
                </p>

                {#if game.type !== "TOOL"}
                    <span
                        class="absolute top-2 right-2 px-2 py-0.5 text-[10px] font-bold bg-black/50 rounded border border-white/20"
                    >
                        {game.type}
                    </span>
                {/if}

                <!-- Scanline effect on hover -->
                <div
                    class="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-10 pointer-events-none transition-opacity"
                ></div>
            </button>
        {/each}
    </div>
</div>
