import { writable } from 'svelte/store';

// --- CONFIGURATION ---
const RANKS = [
    { level: 1, name: "Novice du Tas", minXp: 0, icon: "🌱" },
    { level: 2, name: "Apprenti Ver", minXp: 100, icon: "🪱" },
    { level: 3, name: "Jardinier Averti", minXp: 300, icon: "🌻" },
    { level: 4, name: "Maître Composteur", minXp: 600, icon: "🎓" },
    { level: 5, name: "Shaman du Sol", minXp: 1000, icon: "🧙‍♂️" }
];

// Load from localStorage
const storedXp = typeof localStorage !== 'undefined' ? parseInt(localStorage.getItem('compost_xp') || '0') : 0;

export const xp = writable(storedXp);
export const showLevelUp = writable(false);
export const lastXpGain = writable({ amount: 0, label: '', id: 0 });

// --- ACTIONS ---
export function addXp(amount, label = "Action") {
    xp.update(current => {
        const next = current + amount;
        if (typeof localStorage !== 'undefined') localStorage.setItem('compost_xp', next.toString());

        // Check Level Up
        const oldRank = getRank(current);
        const newRank = getRank(next);

        if (newRank.level > oldRank.level) {
            showLevelUp.set(true);
            setTimeout(() => showLevelUp.set(false), 5000);
        }

        // Show floating text trigger (can be subscribed to by logic)
        lastXpGain.set({ amount, label, id: Date.now() });

        return next;
    });
}

// --- GETTERS ---
export function getRank(currentXp) {
    return RANKS.slice().reverse().find(r => currentXp >= r.minXp) || RANKS[0];
}

export function getNextRank(currentXp) {
    return RANKS.find(r => r.minXp > currentXp) || null;
}

export function getProgress(currentXp) {
    const rank = getRank(currentXp);
    const next = getNextRank(currentXp);
    if (!next) return 100;

    const range = next.minXp - rank.minXp;
    const current = currentXp - rank.minXp;
    return Math.min(100, Math.floor((current / range) * 100));
}
