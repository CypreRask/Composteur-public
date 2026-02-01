<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let title = "WINDOW";
    export let color = "blue"; // blue, green, brown, purple
    export let width = "max-w-lg"; // tailwind max-width class
    export let height = ""; // tailwind height class
    export let mode = "modal"; // "modal" (fixed overlay) or "inline" (relative block)

    // Map logic colors to specific gradients if needed
    const headerColors = {
        blue: "from-blue-800 to-blue-600",
        green: "from-green-800 to-green-600",
        brown: "from-[#5D4037] to-[#8D6E63]",
        purple: "from-purple-800 to-purple-600",
    };

    $: headerGradient = headerColors[color] || headerColors.blue;
    $: isModal = mode === "modal";
</script>

<!-- CONDITIONALLY RENDER WRAPPER BASED ON MODE -->
<div
    class="{isModal
        ? 'fixed inset-0 z-[100] flex items-center justify-center'
        : 'relative w-full h-full'} font-pixel text-[#FFF8E1] {isModal
        ? 'pointer-events-none'
        : ''}"
>
    <!-- Backdrop (Only for Modals) -->
    {#if isModal}
        <div
            class="absolute inset-0 bg-black/80 pointer-events-auto backdrop-blur-sm"
            on:click={() => dispatch("close")}
            on:keydown={(e) => e.key === "Escape" && dispatch("close")}
            role="button"
            tabindex="0"
        ></div>
    {/if}

    <!-- Window Frame -->
    <div
        class="relative bg-[#3E2723] p-1 shadow-[8px_8px_0_rgba(0,0,0,0.5)] {width} {height} {isModal
            ? 'mx-4 pointer-events-auto animate-pop-in'
            : 'w-full'} flex flex-col border-4 border-[#558B2F]"
    >
        <!-- INNER CONTENT -->
        <div class="h-full flex flex-col relative max-h-[90vh]">
            <!-- Close Button (Only for Modals) -->
            {#if isModal}
                <button
                    class="absolute top-2 right-2 bg-[#558B2F] border-2 border-[#7CB342] text-white w-8 h-8 flex items-center justify-center font-bold text-lg leading-none z-50 hover:bg-[#7CB342] transition-colors shadow-[2px_2px_0_rgba(0,0,0,0.3)]"
                    on:click={() => dispatch("close")}
                    aria-label="Close">X</button
                >
            {/if}

            <!-- Scrollable Content -->
            <div class="p-6 overflow-y-auto custom-scrollbar">
                <!-- Optional Title (if passed) - Styled as Header -->
                {#if title && title !== "WINDOW"}
                    <h2
                        class="text-2xl text-[#C0CA33] mb-4 border-b-2 border-[#558B2F] pb-2 font-bold uppercase"
                    >
                        {title}
                    </h2>
                {/if}

                <slot />
            </div>
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
