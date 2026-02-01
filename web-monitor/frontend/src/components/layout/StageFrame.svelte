<script>
    // StageFrame simplifié - Retour à une approche fiable
    export let overlayActive = false;
</script>

<div class="stage-shell">
    <div class="stage-frame">
        <slot />
    </div>
    
    {#if overlayActive}
        <div class="stage-overlay">
            <slot name="overlay" />
        </div>
    {/if}
</div>

<style>
    .stage-shell {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    .stage-frame {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    .stage-overlay {
        position: fixed;
        inset: 0;
        z-index: 9999;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
    }
</style>
