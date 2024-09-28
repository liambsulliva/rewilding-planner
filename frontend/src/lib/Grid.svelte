<script lang="ts">
    export let name = 'heart';
    export const rows = 534; // Arb values
    export const cols = 586;
    export const cellSize = 1;
    let zoomLevel = 1;  // Track zoom level

    const svgIcons = {
      heart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>`,
      star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>`,
      circle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>`
    };

    $: svg = svgIcons[name] || '';

    // Zoom detection logic
    window.addEventListener('wheel', (event) => {
      if (event.ctrlKey) {
        zoomLevel = Math.max(0.5, Math.min(2, zoomLevel - event.deltaY * 0.001));
        event.preventDefault();
      }
    });
</script>

<div class="grid" style="--rows: {rows}; --cols: {cols}; --cell-size: {cellSize}px; --zoom: {zoomLevel};">
    {#each Array(rows * cols) as _, i}
      <div class="cell">
        {@html zoomLevel > 1 ? svg : '<div class="pixel"></div>'} <!-- Pixel switch -->
      </div>
    {/each}
</div>

<style>
  .grid {
    display: grid;
    grid-template-rows: repeat(var(--rows), calc(var(--cell-size) * var(--zoom)));
    grid-template-columns: repeat(var(--cols), calc(var(--cell-size) * var(--zoom)));
    gap: 1px;
    background-color: #333;
    width: fit-content;
    transform: scale(var(--zoom));
    transform-origin: 0 0;
  }

  .cell {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px;
  }

  .cell :global(svg) {
    width: 100%;
    height: 100%;
  }

  .pixel {
    width: 100%;
    height: 100%;
    background-color: #999;
  }
</style>