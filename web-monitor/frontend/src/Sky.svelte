<script>
    export let weatherData = null;

    // --- LOGIQUE ASTRONOMIQUE (RÉINTEGRATION) ---
    
    // 1. Calcul de la Phase de Lune (Approximation)
    function getMoonPhase() {
        const d = new Date();
        let year = d.getFullYear();
        let month = d.getMonth() + 1;
        let day = d.getDate();
        
        if (month < 3) { year--; month += 12; }
        
        const a = Math.floor(year / 100);
        const b = 2 - a + Math.floor(a / 4);
        const jd = Math.floor(365.25 * (year + 4716)) + Math.floor(30.6001 * (month + 1)) + day + b - 1524.5;
        const daysSinceNew = (jd - 2451550.1) / 29.53058867;
        const phase = daysSinceNew - Math.floor(daysSinceNew);
        return phase; // 0 = New, 0.5 = Full
    }

    const moonPhase = getMoonPhase();
    
    // Type d'affichage Lune (Pixel Art Logic)
    let moonType = 'full';
    if(moonPhase < 0.1 || moonPhase > 0.9) moonType = 'new';
    else if(moonPhase < 0.25) moonType = 'crescent-waxing';
    else if(moonPhase < 0.4) moonType = 'quarter-waxing';
    else if(moonPhase < 0.6) moonType = 'full';
    else if(moonPhase < 0.75) moonType = 'quarter-waning';
    else moonType = 'crescent-waning';


    // 2. Position du Soleil / Lune (Cycle Jour)
    let sunX = 0; let sunY = 500; // Hors écran
    let moonX = 0; let moonY = 500;
    let skyGradient = 'bg-[#4FC3F7]'; // Default Day
    let isNight = false;

    $: if (weatherData && weatherData.sys) {
        const now = Date.now() / 1000;
        const sunrise = weatherData.sys.sunrise;
        const sunset = weatherData.sys.sunset;
        const dayDuration = sunset - sunrise;
        
        // CYCLE
        if (now >= sunrise && now <= sunset) {
            // JOUR
            isNight = false;
            const progress = (now - sunrise) / dayDuration; 
            
            // Trajectoire Solaire (Parabole)
            sunX = 10 + (progress * 80); 
            // 0 -> 1 -> 0 pour la hauteur
            const height = 4 * (progress - (progress * progress)); 
            sunY = 80 - (height * 70); // Plus le chiffre est bas, plus c'est haut (top css)
            
            moonY = 200; // Lune cachée
            
            // Ciel
            if(progress < 0.1 || progress > 0.9) skyGradient = 'bg-[#FF7043]'; // Aube/Crepuscule Orange
            else skyGradient = 'bg-[#4FC3F7]'; // Bleu Jour

        } else {
            // NUIT
            isNight = true;
            sunY = 200; // Soleil caché
            
            // Lune haute
            moonX = 80; 
            moonY = 20; 
            
            skyGradient = 'bg-[#0D1B2A]'; // Bleu Nuit Profond
        }
    } else {
        // Fallback si pas de data (simule jour)
        sunX = 50; sunY = 20;
    }

    // --- GENERATION PROCEDURALE (Oiseaux & Nuages) ---
    
    // Densité nuageuse basée sur API (defaut 20%)
    $: cloudCover = weatherData?.clouds?.all ?? 20; 
    
    // On génère 10 nuages potentiels, mais on n'affiche que ceux nécessaires
    // Vitesse ralentie : 100s à 200s (C'est très lent, zen)
    const cloudsPool = Array.from({ length: 8 }).map((_, i) => ({
        top: Math.random() * 50 + 5,
        width: Math.random() * 80 + 40,
        speed: Math.random() * 100 + 100, // 100s min -> très lent
        delay: Math.random() * -200, // Start random cycle
        opacity: Math.random() * 0.4 + 0.6 // Transparence variable
    }));
    
    // Filtrage réactif : Plus il fait moche, plus on en montre
    $: activeClouds = cloudsPool.slice(0, Math.ceil((cloudCover / 100) * 8));

    const birds = Array.from({ length: 3 }).map((_, i) => ({
        top: Math.random() * 30 + 10,
        speed: Math.random() * 10 + 20,
        delay: Math.random() * -20
    }));

</script>

<div class="h-full w-full relative transition-colors duration-2000 overflow-hidden border-b-4 border-terra-deep {skyGradient} font-pixel">
    
    <!-- HEADER -->
    <div class="absolute top-4 left-4 text-white drop-shadow-md z-30">
        <h1 class="text-xl md:text-2xl text-yellow-300 drop-shadow-[2px_2px_0_rgba(0,0,0,1)] uppercase">SmartCompost</h1>
        <p class="text-[8px] mt-1 text-white/90 uppercase tracking-widest bg-black/20 p-1 inline-block">
             {#if weatherData && weatherData.weather}
               {weatherData.name}: {weatherData.weather[0].description} {weatherData.main.temp.toFixed(1)}°C
             {:else}
               Systeme Offline...
             {/if}
        </p>
    </div>

    <!-- SOLEIL (Pixel Art) -->
    <div class="absolute w-16 h-16 bg-yellow-400 border-4 border-black/10 shadow-[4px_4px_0_rgba(0,0,0,0.2)] transition-all duration-1000 linear z-10"
         style="left: {sunX}%; top: {sunY}%;">
        <div class="absolute top-2 left-2 w-4 h-4 bg-yellow-200"></div>
    </div>

    <!-- LUNE (Pixel Art Dynamique) -->
    <div class="absolute w-12 h-12 bg-white border-4 border-black/10 shadow-[4px_4px_0_rgba(0,255,255,0.1)] transition-all duration-1000 linear z-10"
         style="left: {isNight ? 80 : 50}%; top: {moonY}%;">
         <!-- Phases (Masque noir pixelisé) -->
         {#if moonType === 'crescent-waxing'}
            <div class="absolute inset-0 bg-[#0D1B2A] w-1/2"></div>
         {:else if moonType === 'new'}
            <div class="absolute inset-0 bg-[#0D1B2A] opacity-90"></div>
         {/if}
         <!-- Cratères -->
         <div class="absolute top-2 left-3 w-2 h-2 bg-gray-300"></div>
         <div class="absolute bottom-2 right-3 w-2 h-2 bg-gray-300"></div>
    </div>

    <!-- ETOILES (Si Nuit) -->
    {#if isNight}
        {#each Array(20) as _, i}
            <div class="absolute w-1 h-1 bg-white animate-pulse" 
                 style="left: {Math.random()*100}%; top: {Math.random()*60}%; animation-delay: {Math.random()}s"></div>
        {/each}
    {/if}


    <!-- OISEAUX (Animés - Battement d'ailes) -->
    <!-- On ne les affiche pas la nuit -->
    {#if !isNight}
        {#each birds as bird}
            <div class="absolute w-8 h-8 animate-fly z-20"
                style="top: {bird.top}%; --duration: {bird.speed}s; --delay: {bird.delay}s">
                
                <!-- Sprite Animé via CSS -->
                <div class="w-full h-full animate-wing-flap">
                    <!-- Frame 1: Ailes Hautes -->
                    <div class="wing-up absolute inset-0">
                         <div class="absolute top-2 left-0 w-1 h-1 bg-black"></div>
                         <div class="absolute top-3 left-1 w-1 h-1 bg-black"></div>
                         <div class="absolute top-4 left-2 w-4 h-2 bg-black"></div> <!-- Corps -->
                         <div class="absolute top-3 right-1 w-1 h-1 bg-black"></div>
                         <div class="absolute top-2 right-0 w-1 h-1 bg-black"></div>
                    </div>
                </div>
            </div>
        {/each}
    {/if}

    <!-- NUAGES (Rectangles) -->
    {#each activeClouds as cloud}
        <div class="absolute h-8 bg-white border-b-4 border-r-4 border-gray-300 animate-drift z-10"
             style="
                top: {cloud.top}%; 
                width: {cloud.width}px;
                opacity: {cloud.opacity};
                --duration: {cloud.speed}s;
                --delay: {cloud.delay}s;
             ">
             <div class="absolute bottom-full left-4 w-1/2 h-4 bg-white"></div>
        </div>
    {/each}

</div>

<style>
    @keyframes drift {
        from { transform: translateX(-150px); }
        to { transform: translateX(110vw); }
    }
    .animate-drift {
        animation: drift var(--duration) linear infinite;
        animation-delay: var(--delay);
    }

    @keyframes fly {
        from { transform: translateX(-50px); }
        to { transform: translateX(110vw); }
    }
    .animate-fly {
        animation: fly var(--duration) linear infinite;
        animation-delay: var(--delay);
    }

    /* Animation Sprite Battement d'ailes */
    @keyframes wingFlap {
        0%, 100% { transform: translateY(0) scaleY(1); } /* Ailes Hautes */
        50% { transform: translateY(2px) scaleY(-0.5); } /* Ailes Basses (Flip vertical pour effet simple) */
    }
    .animate-wing-flap {
        animation: wingFlap 0.4s steps(2) infinite; /* steps(2) pour effet saccadé 8-bit */
    }
</style>
