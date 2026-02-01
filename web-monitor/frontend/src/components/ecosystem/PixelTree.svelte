<script>
    // A simple yet robust Pixel Art Tree
    // Using a grid of divs for organic shape rather than big squares
</script>

<div
    class="relative w-48 h-80 flex flex-col justify-end items-center group font-pixel select-none pointer-events-none"
>
    <!-- LEAVES (The Crown) -->
    <!-- Layered squares for organic 8-bit look -->
    <div
        class="absolute bottom-32 flex flex-col items-center pointer-events-auto transition-transform duration-500 hover:scale-105 origin-bottom"
    >
        <!-- Top Tier -->
        <div class="w-16 h-8 bg-[#2E7D32] shadow-sm z-30"></div>

        <!-- Middle Tier -->
        <div
            class="w-32 h-16 bg-[#2E7D32] -my-2 z-20 relative flex items-center justify-between px-2"
        >
            <!-- Details / Highlights -->
            <div
                class="w-2 h-2 bg-[#4CAF50] absolute top-2 left-4 opacity-50"
            ></div>
            <div
                class="w-2 h-2 bg-[#1B5E20] absolute bottom-2 right-4 opacity-30"
            ></div>
        </div>

        <!-- Bottom Tier -->
        <div
            class="w-40 h-16 bg-[#2E7D32] -my-2 z-10 relative shadow-[4px_4px_0_rgba(0,0,0,0.2)]"
        >
            <!-- Apples -->
            <div
                class="absolute top-4 left-6 w-3 h-3 bg-[#C62828] border border-[#8E0000] rotate-45 shadow-sm group-hover:animate-bounce"
            ></div>
            <div
                class="absolute bottom-3 right-8 w-3 h-3 bg-[#C62828] border border-[#8E0000] rotate-12 shadow-sm group-hover:animate-bounce"
                style="animation-delay: 0.2s"
            ></div>
            <div
                class="absolute top-8 right-12 w-3 h-3 bg-[#C62828] border border-[#8E0000] -rotate-12 shadow-sm group-hover:animate-bounce"
                style="animation-delay: 0.4s"
            ></div>
        </div>
    </div>

    <!-- TRUNK -->
    <div
        class="w-12 h-36 bg-[#5D4037] border-x-4 border-[#3E2723] relative z-0 flex justify-center"
    >
        <!-- Bark Detail -->
        <div class="w-2 h-8 bg-[#3E2723] opacity-40 mt-4 mr-4"></div>
        <div
            class="absolute bottom-0 w-16 h-4 bg-[#3E2723] -mb-2 rounded-t-none"
        ></div>
        <!-- Roots -->
    </div>
</div>
