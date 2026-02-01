<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let title = "WIDGET";
    export let color = "blue"; // blue, green, brown
</script>

<div
    class="fixed inset-0 z-[100] flex items-center justify-center pointer-events-none"
>
    <!-- Backdrop Blur -->
    <div
        class="absolute inset-0 bg-black/50 backdrop-blur-sm pointer-events-auto"
        on:click={() => dispatch("close")}
    ></div>

    <!-- Window Frame -->
    <div
        class="relative bg-[#E0E0E0] border-t-4 border-l-4 border-white border-b-4 border-r-4 border-gray-600 shadow-2xl w-full max-w-lg mx-4 pointer-events-auto animate-pop-in font-pixel text-black"
    >
        <!-- Title Bar -->
        <div
            class="bg-{color}-800 text-white px-2 py-1 flex justify-between items-center bg-gradient-to-r from-blue-800 to-blue-600"
        >
            <span
                class="font-bold tracking-widest uppercase text-sm drop-shadow-md"
                >{title}</span
            >
            <button
                class="w-6 h-6 bg-red-500 border-2 border-white hover:bg-red-400 active:border-gray-500 flex items-center justify-center shadow-inner"
                on:click={() => dispatch("close")}
            >
                ✕
            </button>
        </div>

        <!-- Content Area -->
        <div
            class="p-4 bg-gray-100 min-h-[200px] border-2 border-gray-400 inset-shadow"
        >
            <slot />
        </div>

        <!-- Status Bar (Retro) -->
        <div
            class="px-2 py-1 text-[10px] text-gray-500 border-t border-gray-400 flex justify-between"
        >
            <span>READY.</span>
            <span>MEM: 64KB</span>
        </div>
    </div>
</div>

<style>
    @keyframes popIn {
        0% {
            transform: scale(0.9);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    .animate-pop-in {
        animation: popIn 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
</style>
