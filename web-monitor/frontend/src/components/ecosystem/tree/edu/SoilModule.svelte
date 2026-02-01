<script>
  import { onMount } from 'svelte';
  
  let activeTab = 'mycelium';
  let animationStep = 0;
  
  onMount(() => {
    const interval = setInterval(() => {
      animationStep = (animationStep + 1) % 4;
    }, 1000);
    return () => clearInterval(interval);
  });

  const tabs = [
    { id: 'mycelium', label: '🍄 Mycélium', color: 'purple' },
    { id: 'cah', label: '⚗️ Complexe Argilo-Humique', color: 'brown' },
    { id: 'rhizosphere', label: '🌱 Rhizosphère', color: 'green' },
    { id: 'mineral', label: '⛏️ Minéralisation', color: 'gray' }
  ];
</script>

<div class="w-full max-w-3xl mx-auto p-4">
  <!-- Header -->
  <div class="text-center mb-6">
    <h2 class="text-2xl font-bold text-[#5d4037] mb-2">🌍 Le Monde du Sol</h2>
    <p class="text-sm text-gray-600">Explore les secrets cachés sous tes pieds</p>
  </div>

  <!-- Tabs -->
  <div class="flex flex-wrap gap-2 mb-6 justify-center">
    {#each tabs as tab}
      <button
        class={`px-4 py-2 rounded-lg font-bold text-xs transition-all ${
          activeTab === tab.id
            ? `bg-${tab.color}-600 text-white shadow-lg`
            : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
        }`}
        style={activeTab === tab.id ? `background-color: var(--${tab.color}-600, #8b5cf6)` : ''}
        on:click={() => activeTab = tab.id}
      >
        {tab.label}
      </button>
    {/each}
  </div>

  <!-- Content -->
  <div class="bg-gradient-to-b from-[#f5f5dc] to-[#e8dcc4] rounded-xl p-6 border-4 border-[#5d4037] shadow-inner">
    
    {#if activeTab === 'mycelium'}
      <div class="space-y-4">
        <div class="flex items-center gap-4 mb-4">
          <div class="text-4xl">🕸️</div>
          <div>
            <h3 class="font-bold text-lg text-purple-800">Le Réseau du Bois</h3>
            <p class="text-xs text-gray-600">Le mycélium connecte les arbres entre eux !</p>
          </div>
        </div>

        <!-- Visual Mycelium Network -->
        <div class="relative h-48 bg-[#3e2723] rounded-lg overflow-hidden border-2 border-purple-400">
          <svg class="absolute inset-0 w-full h-full" viewBox="0 0 400 200">
            <!-- Roots/Tree base -->
            <rect x="180" y="20" width="40" height="60" fill="#5d4037" />
            
            <!-- Mycelium threads -->
            {#each Array(20) as _, i}
              <path
                d={`M${200 + Math.sin(i) * 20} 80 Q${150 + Math.random() * 100} ${100 + Math.random() * 50} ${50 + Math.random() * 300} ${150 + Math.random() * 40}`}
                stroke="rgba(216, 180, 254, 0.6)"
                stroke-width="1"
                fill="none"
                class="animate-pulse"
                style="animation-delay: {i * 0.1}s"
              />
            {/each}
            
            <!-- Connection nodes -->
            {#each Array(8) as _, i}
              <circle
                cx={60 + i * 40}
                cy={140 + Math.sin(i) * 20}
                r="4"
                fill="#d8b4fe"
                class="animate-ping"
                style="animation-duration: 2s; animation-delay: {i * 0.3}s"
              />
            {/each}
            
            <!-- Mushrooms -->
            <g transform="translate(80, 160)">
              <rect x="3" y="0" width="4" height="15" fill="#fef3c7" />
              <path d="M0 5 Q5 -5 10 5 Z" fill="#ef4444" />
            </g>
            <g transform="translate(280, 150)">
              <rect x="4" y="0" width="4" height="20" fill="#fef3c7" />
              <ellipse cx="6" cy="5" rx="10" ry="6" fill="#a855f7" />
            </g>
            <g transform="translate(320, 170)">
              <rect x="3" y="0" width="3" height="12" fill="#fef3c7" />
              <path d="M-2 4 Q3 -8 8 4 Z" fill="#f97316" />
            </g>
          </svg>
          
          <!-- Labels -->
          <div class="absolute top-2 left-2 bg-black/50 text-white text-[10px] px-2 py-1 rounded">
            🌳 Arbre 1
          </div>
          <div class="absolute bottom-2 right-2 bg-black/50 text-white text-[10px] px-2 py-1 rounded">
            🌳 Arbre 2
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 text-xs">
          <div class="bg-white/50 p-3 rounded-lg">
            <strong class="text-purple-700">🍄 Champignons</strong>
            <p class="mt-1 text-gray-700">Décomposent la matière organique et libèrent les nutriments</p>
          </div>
          <div class="bg-white/50 p-3 rounded-lg">
            <strong class="text-purple-700">🕸️ Hyphae</strong>
            <p class="mt-1 text-gray-700">Filaments qui explorent le sol et transportent l'eau et les nutriments</p>
          </div>
        </div>

        <div class="bg-purple-100 border-l-4 border-purple-500 p-3 rounded">
          <p class="text-xs text-purple-800">
            <strong>💡 Le saviez-vous ?</strong> Le mycélium peut s'étendre sur des kilomètres et connecter plusieurs arbres, formant le "Wood Wide Web" !
          </p>
        </div>
      </div>

    {:else if activeTab === 'cah'}
      <div class="space-y-4">
        <div class="flex items-center gap-4 mb-4">
          <div class="text-4xl">⚗️</div>
          <div>
            <h3 class="font-bold text-lg text-amber-800">Le Mariage de l'Argile et de l'Humus</h3>
            <p class="text-xs text-gray-600">La clé d'un sol fertile</p>
          </div>
        </div>

        <!-- CAH Formation Animation -->
        <div class="relative h-40 bg-gradient-to-b from-[#87ceeb] to-[#5d4037] rounded-lg overflow-hidden border-2 border-amber-600">
          <!-- Rain -->
          {#each Array(10) as _, i}
            <div
              class="absolute w-0.5 h-4 bg-blue-400/60"
              style="left: {10 + i * 9}%; top: {animationStep * 20}%;"
            />
          {/each}
          
          <!-- Clay particles -->
          <div class="absolute bottom-8 left-4 flex gap-1">
            {#each Array(6) as _, i}
              <div class="w-4 h-4 bg-amber-700 rounded-sm transform rotate-45" 
                   style="animation: bounce 1s infinite; animation-delay: {i * 0.1}s" />
            {/each}
          </div>
          
          <!-- Humus particles -->
          <div class="absolute bottom-8 right-4 flex gap-1">
            {#each Array(6) as _, i}
              <div class="w-3 h-3 bg-[#2d5016] rounded-full"
                   style="animation: bounce 1s infinite; animation-delay: {i * 0.15}s" />
            {/each}
          </div>
          
          <!-- CAH Formation (center) -->
          <div class="absolute bottom-4 left-1/2 -translate-x-1/2">
            <div class={`w-24 h-16 rounded-lg transition-all duration-500 ${
              animationStep > 1 ? 'bg-gradient-to-br from-amber-700 to-[#2d5016] scale-110' : 'bg-gray-400 scale-100'
            }`}>
              <div class="text-center text-white text-[10px] pt-6 font-bold">
                {animationStep > 2 ? 'CAH ✅' : 'Formation...'}
              </div>
            </div>
          </div>
          
          <!-- Plant -->
          <div class="absolute bottom-16 left-1/2 -translate-x-1/2">
            <div class="text-2xl">🌱</div>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-2 text-xs">
          <div class="bg-amber-100 p-2 rounded text-center">
            <div class="text-xl mb-1">🏔️</div>
            <strong class="text-amber-800">Argile</strong>
            <p class="text-[10px] text-gray-600">Retient l'eau et les nutriments</p>
          </div>
          <div class="bg-green-100 p-2 rounded text-center">
            <div class="text-xl mb-1">🍂</div>
            <strong class="text-green-800">Humus</strong>
            <p class="text-[10px] text-gray-600">Matière organique décomposée</p>
          </div>
          <div class="bg-gradient-to-br from-amber-100 to-green-100 p-2 rounded text-center border-2 border-amber-400">
            <div class="text-xl mb-1">⚗️</div>
            <strong class="text-amber-900">CAH</strong>
            <p class="text-[10px] text-gray-600">Sol structuré et fertile !</p>
          </div>
        </div>

        <div class="bg-amber-50 border-l-4 border-amber-600 p-3 rounded">
          <p class="text-xs text-amber-900">
            <strong>🔬 C'est quoi le CAH ?</strong> C'est un complexe formé par l'association de l'argile (minéral) et de l'humus (organique). C'est la "colle" du sol qui crée une structure stable pour les racines.
          </p>
        </div>
      </div>

    {:else if activeTab === 'rhizosphere'}
      <div class="space-y-4">
        <div class="flex items-center gap-4 mb-4">
          <div class="text-4xl">🌱</div>
          <div>
            <h3 class="font-bold text-lg text-green-800">La Zone Magique des Racines</h3>
            <p class="text-xs text-gray-600">Où la vie du sol est la plus intense</p>
          </div>
        </div>

        <!-- Rhizosphere Cross-section -->
        <div class="relative h-48 bg-gradient-to-b from-[#f5f5dc] to-[#3e2723] rounded-lg overflow-hidden border-2 border-green-500">
          <svg class="absolute inset-0 w-full h-full" viewBox="0 0 400 200">
            <!-- Root hair -->
            <path d="M200 0 Q210 50 205 100 Q200 150 202 200" 
                  stroke="#8b4513" stroke-width="12" fill="none" />
            
            <!-- Root hairs -->
            {#each Array(15) as _, i}
              <line x1={205 - 6 + Math.random() * 12} 
                    y1={30 + i * 10} 
                    x2={180 + Math.random() * 50} 
                    y2={35 + i * 10 + Math.random() * 5}
                    stroke="#a0522d" stroke-width="1" opacity="0.7" />
            {/each}
            
            <!-- Bacteria around root -->
            {#each Array(30) as _, i}
              <circle cx={150 + Math.random() * 100} 
                      cy={50 + Math.random() * 140} 
                      r="2" 
                      fill={Math.random() > 0.5 ? '#22c55e' : '#3b82f6'}
                      opacity="0.8"
                      class="animate-pulse"
                      style="animation-delay: {Math.random()}s" />
            {/each}
            
            <!-- Mycorrhizae -->
            <path d="M200 80 Q150 90 130 110" stroke="#d8b4fe" stroke-width="2" fill="none" stroke-dasharray="4,2" />
            <path d="M205 120 Q250 130 270 140" stroke="#d8b4fe" stroke-width="2" fill="none" stroke-dasharray="4,2" />
            
            <!-- Nutrient exchange arrows -->
            <g class="animate-pulse">
              <path d="M160 60 L170 55 L168 65 Z" fill="#fbbf24" />
              <text x="140" y="50" fill="#fbbf24" font-size="8">Sucre</text>
            </g>
            <g class="animate-pulse" style="animation-delay: 0.5s">
              <path d="M240 140 L230 145 L232 135 Z" fill="#3b82f6" />
              <text x="245" y="155" fill="#3b82f6" font-size="8">P, N, K</text>
            </g>
          </svg>
          
          <!-- Zone label -->
          <div class="absolute top-2 left-1/2 -translate-x-1/2 bg-green-600 text-white text-xs px-3 py-1 rounded-full">
            🎯 Rhizosphère (1-2mm autour de la racine)
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3 text-xs">
          <div class="bg-green-50 p-3 rounded-lg border border-green-200">
            <strong class="text-green-700">🏭 Usine à sucre</strong>
            <p class="mt-1 text-gray-700">La racine libère des sucres (exsudats) qui nourrissent les bactéries</p>
          </div>
          <div class="bg-blue-50 p-3 rounded-lg border border-blue-200">
            <strong class="text-blue-700">🔄 Échange</strong>
            <p class="mt-1 text-gray-700">En échange, les microbes libèrent des nutriments (N, P, K) absorbables</p>
          </div>
        </div>

        <div class="bg-green-100 border-l-4 border-green-500 p-3 rounded">
          <p class="text-xs text-green-900">
            <strong>🤝 Symbiose !</strong> La plante nourrit les microbes, et les microbes nourrissent la plante. C'est une coopération gagnant-gagnant !
          </p>
        </div>
      </div>

    {:else if activeTab === 'mineral'}
      <div class="space-y-4">
        <div class="flex items-center gap-4 mb-4">
          <div class="text-4xl">⛏️</div>
          <div>
            <h3 class="font-bold text-lg text-gray-800">La Minéralisation</h3>
            <p class="text-xs text-gray-600">Transformation de l'organique en minéral</p>
          </div>
        </div>

        <!-- Mineralization Process -->
        <div class="relative bg-gray-100 rounded-lg p-4 border-2 border-gray-400">
          <div class="flex items-center justify-between">
            <!-- Step 1 -->
            <div class="text-center flex-1">
              <div class="text-3xl mb-2">🍂</div>
              <div class="text-xs font-bold text-gray-700">Déchets</div>
              <div class="text-[10px] text-gray-500">Organique</div>
            </div>
            
            <!-- Arrow -->
            <div class="flex flex-col items-center px-2">
              <span class="text-lg">→</span>
              <span class="text-[10px] text-purple-600">🦠 Bactéries</span>
            </div>
            
            <!-- Step 2 -->
            <div class="text-center flex-1">
              <div class="text-3xl mb-2">🪱</div>
              <div class="text-xs font-bold text-amber-700">Humus</div>
              <div class="text-[10px] text-gray-500">Partiellement décomposé</div>
            </div>
            
            <!-- Arrow -->
            <div class="flex flex-col items-center px-2">
              <span class="text-lg">→</span>
              <span class="text-[10px] text-purple-600">🍄 Fungi</span>
            </div>
            
            <!-- Step 3 -->
            <div class="text-center flex-1">
              <div class="text-3xl mb-2">⚗️</div>
              <div class="text-xs font-bold text-blue-700">Nutriments</div>
              <div class="text-[10px] text-gray-500">Minéraux (NO3-, PO4-)</div>
            </div>
            
            <!-- Arrow -->
            <div class="text-lg px-2">→</div>
            
            <!-- Step 4 -->
            <div class="text-center flex-1">
              <div class="text-3xl mb-2">🌱</div>
              <div class="text-xs font-bold text-green-700">Plante</div>
              <div class="text-[10px] text-gray-500">Absorption</div>
            </div>
          </div>
        </div>

        <!-- NPK Display -->
        <div class="grid grid-cols-3 gap-3">
          <div class="bg-blue-50 border-2 border-blue-400 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold text-blue-600">N</div>
            <div class="text-xs font-bold text-blue-800">Azote</div>
            <div class="text-[10px] text-gray-600 mt-1">Feuilles vertes, croissance</div>
            <div class="text-[10px] text-blue-600 mt-1">NO3-, NH4+</div>
          </div>
          <div class="bg-orange-50 border-2 border-orange-400 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold text-orange-600">P</div>
            <div class="text-xs font-bold text-orange-800">Phosphore</div>
            <div class="text-[10px] text-gray-600 mt-1">Racines, fleurs, fruits</div>
            <div class="text-[10px] text-orange-600 mt-1">PO4---</div>
          </div>
          <div class="bg-purple-50 border-2 border-purple-400 rounded-lg p-3 text-center">
            <div class="text-2xl font-bold text-purple-600">K</div>
            <div class="text-xs font-bold text-purple-800">Potassium</div>
            <div class="text-[10px] text-gray-600 mt-1">Résistance, circulation</div>
            <div class="text-[10px] text-purple-600 mt-1">K+</div>
          </div>
        </div>

        <div class="bg-gray-100 border-l-4 border-gray-600 p-3 rounded">
          <p class="text-xs text-gray-800">
            <strong>🔄 Le cycle :</strong> La minéralisation transforme les déchets organiques en nutriments minéraux que les plantes peuvent absorber. Sans elle, plus rien ne pousserait !
          </p>
        </div>
      </div>
    {/if}
  </div>
</div>

<style>
  @keyframes bounce {
    0%, 100% { transform: translateY(0) rotate(45deg); }
    50% { transform: translateY(-5px) rotate(45deg); }
  }
</style>
