<script>
    export let temp = 20; // Celsius

    // Rotation Logic (0°C = -120deg, 80°C = 120deg)
    $: rotation = Math.min(120, Math.max(-120, (temp - 40) * 3));

    $: isHot = temp > 50;
    $: isCold = temp < 10;
</script>

<!-- DIAL THERMOMETER -->
<div
    class="absolute right-4 top-1/2 -translate-y-1/2 flex flex-col items-center z-20 group cursor-help font-pixel"
>
    <!-- DIAL FACE (Round... but pixelated circle via CSS) -->
    <div
        class="w-12 h-12 bg-white rounded-full border-4 border-[#BDBDBD] shadow-xl relative flex items-center justify-center"
    >
        <!-- Ticks -->
        <div
            class="absolute inset-0 rounded-full border border-gray-300 opacity-50"
        ></div>

        <!-- Zones (Colored Arcs - CSS Conic Gradient) -->
        <div
            class="absolute inset-1 rounded-full opacity-30"
            style="background: conic-gradient(
                from 180deg,
                blue 0deg 60deg,    /* Cold 0-20 */
                green 60deg 180deg, /* Active 20-60 */
                red 180deg 240deg   /* Hot 60-80 */
             );"
        ></div>

        <!-- NEEDLE -->
        <div
            class="absolute w-[2px] h-[45%] bg-red-600 origin-bottom bottom-1/2 transition-transform duration-1000 ease-out"
            style="transform: rotate({rotation}deg)"
        ></div>

        <!-- Center Cap -->
        <div class="w-1 h-1 bg-black rounded-full z-10"></div>
    </div>

    <!-- STEM (Metal Spike going down) -->
    <div
        class="w-1 h-32 bg-gradient-to-t from-[#BDBDBD] to-[#757575] border-x border-[#616161] -mt-1 relative z-[-1]"
    ></div>

    <!-- TOOLTIP REMOVED to avoid overlap with global Compost tooltip -->
</div>
