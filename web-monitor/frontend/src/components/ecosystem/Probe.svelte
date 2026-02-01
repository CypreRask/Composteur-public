<script>
    export let humidity = 0; // 0 to 100

    // Status Logic
    $: status = humidity > 80 ? "WET" : humidity < 30 ? "DRY" : "OK";
    $: statusColor =
        status === "WET"
            ? "text-blue-400"
            : status === "DRY"
              ? "text-yellow-400"
              : "text-green-400";
</script>

<!-- METAL PROBE (Spike) -->
<div
    class="absolute left-4 top-1/2 -translate-y-1/2 flex flex-col items-center z-20 group cursor-help font-pixel"
>
    <!-- HEAD (Digital Display) -->
    <div
        class="w-10 h-8 bg-[#212121] border-2 border-[#424242] shadow-lg relative flex items-center justify-center"
    >
        <!-- Screen -->
        <div
            class="w-8 h-5 bg-[#1b5e20] opacity-80 border border-[#2e7d32] flex items-center justify-center overflow-hidden"
        >
            <span class="text-[8px] font-bold text-[#b2ff59] animate-pulse">
                {Math.round(humidity)}%
            </span>
        </div>

        <!-- Status LED -->
        <div
            class="absolute -top-1 right-[-2px] w-2 h-2 border border-black {status ===
            'DRY'
                ? 'bg-red-500 animate-flash'
                : 'bg-green-500'}"
        ></div>
    </div>

    <!-- STEM (Metal Spike going down) -->
    <div
        class="w-1 h-32 bg-gradient-to-t from-[#BDBDBD] to-[#757575] border-x border-[#616161]"
    ></div>

    <!-- TOOLTIP REMOVED to avoid overlap with global Compost tooltip -->
</div>

<style>
    @keyframes flash {
        0%,
        100% {
            opacity: 1;
        }
        50% {
            opacity: 0.2;
        }
    }
    .animate-flash {
        animation: flash 1s infinite;
    }
</style>
