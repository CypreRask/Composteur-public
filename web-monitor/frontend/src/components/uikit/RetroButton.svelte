<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    export let active = false;
    export let color = "gray"; // gray, green, blue, red
    export let label = "BUTTON";
    export let small = false;

    // Color Maps
    const bgColors = {
        gray: active ? "bg-gray-400" : "bg-[#E0E0E0]",
        green: active ? "bg-green-500" : "bg-[#E0E0E0]",
        blue: active ? "bg-blue-500" : "bg-[#E0E0E0]",
        red: active ? "bg-red-500" : "bg-[#E0E0E0]",
    };

    const textColors = {
        gray: active ? "text-white" : "text-black",
        green: active ? "text-white" : "text-green-900", // Dark green text on inactive
        blue: active ? "text-white" : "text-blue-900",
        red: active ? "text-white" : "text-red-900",
    };
</script>

<button
    class="
        border-t-2 border-l-2 border-white border-b-2 border-r-2 border-gray-600
        shadow-sm active:border-t-gray-600 active:border-l-gray-600 active:border-b-white active:border-r-white active:bg-gray-200
        font-bold tracking-wider uppercase transition-none
        {bgColors[color] || 'bg-[#E0E0E0]'} 
        {active
        ? 'border-t-gray-600 border-l-gray-600 border-b-white border-r-white'
        : ''}
        {small ? 'px-2 py-1 text-[10px]' : 'px-4 py-2 text-xs'}
    "
    on:click
>
    <span class={active ? "text-white drop-shadow-sm" : "text-black"}>
        {label}
    </span>
    <slot />
</button>
