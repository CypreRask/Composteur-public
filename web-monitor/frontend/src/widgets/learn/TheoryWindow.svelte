<script>
    import RetroWindow from "../../components/uikit/RetroWindow.svelte";
    import { createEventDispatcher } from "svelte";

    export let title = "";
    export let content = "";
    export let xp = 0;

    const dispatch = createEventDispatcher();

    // Simple markdown-to-html converter (very basic)
    function parseMarkdown(text) {
        if (!text) return "";
        let html = text
            .replace(
                /^# (.*$)/gim,
                '<h1 class="text-2xl font-bold text-[#C0CA33] mb-4 border-b border-[#558B2F] pb-2">$1</h1>',
            )
            .replace(
                /^### (.*$)/gim,
                '<h3 class="text-lg font-bold text-[#AED581] mt-4 mb-2">$1</h3>',
            )
            .replace(
                /^\* (.*$)/gim,
                '<li class="ml-4 mb-1 list-disc text-gray-300">$1</li>',
            )
            .replace(
                /\*\*(.*)\*\*/gim,
                '<strong class="text-white">$1</strong>',
            )
            .replace(/\n/gim, "<br />");
        return html;
    }
</script>

<div class="h-full w-full flex items-center justify-center p-4">
    <RetroWindow
        {title}
        mode="modal"
        color="blue"
        width="max-w-3xl"
        on:close={() => dispatch("close")}
    >
        <div class="prose prose-invert max-w-none font-sans">
            {@html parseMarkdown(content)}
        </div>

        <div class="mt-8 flex justify-center">
            <button
                class="bg-[#558B2F] hover:bg-[#689F38] text-white font-bold py-3 px-8 rounded border-b-4 border-[#2E3B20] active:border-b-0 active:translate-y-1 transition-all"
                on:click={() => dispatch("complete")}
            >
                J'ai compris (+{xp} XP)
            </button>
        </div>
    </RetroWindow>
</div>
