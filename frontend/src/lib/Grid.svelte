<script lang="ts">
  export const rows = 24; // Arbitrary values
  export const cols = 22;
  export const cellSize = 100;

  let zoomLevel = 1;
  let translateX = 0;
  let translateY = 0;
  let isPanning = false;
  let startX = 0;
  let startY = 0;

  const svgIcons = {
    tree: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M6 7a6 6 0 1 1 11.95.775A6 6 0 0 1 15 19h-2v3h-2v-3H8.5A5.5 5.5 0 0 1 6.191 8.507A6 6 0 0 1 6 7m1.01 3.332A3.502 3.502 0 0 0 8.5 17H15a4 4 0 0 0 1.454-7.728l-.841-.328C15.79 8.304 16 7.672 16 7a4 4 0 1 0-6.4 3.2l-1.2 1.6a6 6 0 0 1-1.39-1.468"/></svg>`,
    water: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 16 16"><path fill="currentColor" d="M12 2a.75.75 0 0 1 .696.471c.148.369.375.636.598.808c.242.185.422.219.456.219a.75.75 0 0 1 0 1.5c-.466 0-.96-.216-1.37-.53q-.196-.15-.38-.344a2.76 2.76 0 0 1-2 .874a2.76 2.76 0 0 1-2-.873a2.76 2.76 0 0 1-2 .873a2.76 2.76 0 0 1-2-.873q-.184.194-.38.345c-.409.314-.903.53-1.37.53a.75.75 0 0 1 0-1.5c.033 0 .214-.034.455-.22c.224-.171.451-.44.599-.808a.75.75 0 0 1 1.392 0c.298.742.84 1.026 1.304 1.026s1.007-.284 1.304-1.027a.75.75 0 0 1 1.392 0c.297.743.84 1.027 1.304 1.027s1.007-.285 1.304-1.027A.75.75 0 0 1 12 2m0 4a.75.75 0 0 1 .696.471c.148.369.375.636.598.808c.242.185.422.219.456.219a.75.75 0 0 1 0 1.5c-.466 0-.96-.216-1.37-.53q-.196-.15-.38-.344a2.76 2.76 0 0 1-2 .874a2.76 2.76 0 0 1-2-.873a2.76 2.76 0 0 1-2 .873a2.76 2.76 0 0 1-2-.873q-.184.194-.38.345c-.409.314-.903.53-1.37.53a.75.75 0 0 1 0-1.5c.033 0 .214-.034.455-.22c.224-.171.451-.44.599-.808a.75.75 0 0 1 1.392 0c.298.742.84 1.026 1.304 1.026s1.007-.284 1.304-1.027a.75.75 0 0 1 1.392 0c.297.743.84 1.027 1.304 1.027s1.007-.285 1.304-1.027A.75.75 0 0 1 12 6m.696 4.471a.75.75 0 0 0-1.392 0c-.297.742-.84 1.027-1.304 1.027s-1.007-.284-1.304-1.027a.75.75 0 0 0-1.392 0c-.298.742-.84 1.027-1.304 1.027s-1.006-.284-1.304-1.027a.75.75 0 0 0-1.392 0c-.148.37-.375.637-.599.81c-.241.185-.422.219-.455.219a.75.75 0 1 0 0 1.5c.467 0 .961-.216 1.37-.53q.196-.15.38-.345a2.76 2.76 0 0 0 2 .873a2.76 2.76 0 0 0 2-.873a2.76 2.76 0 0 0 2 .873a2.76 2.76 0 0 0 2-.874q.184.194.38.344c.41.314.904.53 1.37.53a.75.75 0 0 0 0-1.5c-.034 0-.214-.034-.456-.22a1.9 1.9 0 0 1-.598-.807"/></svg>`,
  }

  // Function to randomly pick an SVG or nothing for each cell
  function randomizeSVG() {
    const num = Math.random();
    if (num > 0.66) return 'tree';
    if (num > 0.33) return 'water';
    return '';
  }

  // Generates grid data
  const gridData = Array(rows * cols).fill(null).map(() => randomizeSVG());

  // Zoom detection logic
  window.addEventListener('wheel', (event) => {
    if (event.ctrlKey) {
      zoomLevel = Math.max(0.5, Math.min(2, zoomLevel - event.deltaY * 0.001));
      event.preventDefault();
    }
  });

  // Mouse down event for panning
  function handleMouseDown(event: MouseEvent) {
    isPanning = true;
    startX = event.clientX - translateX;
    startY = event.clientY - translateY;
  }

  // Mouse move event for panning
  function handleMouseMove(event: MouseEvent) {
    if (!isPanning) return;
    translateX = event.clientX - startX;
    translateY = event.clientY - startY;
  }

  // Mouse up event to stop panning
  function handleMouseUp() {
    isPanning = false;
  }

</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div 
  class="grid-container border border-gray-200 rounded-lg" 
  on:mousedown={handleMouseDown}
  on:mousemove={handleMouseMove} 
  on:mouseup={handleMouseUp} 
  on:mouseleave={handleMouseUp}>
  <div class="grid" style="--rows: {rows}; --cols: {cols}; --cell-size: {cellSize}px; --zoom: {zoomLevel}; transform: translate({translateX}px, {translateY}px) scale({zoomLevel});">
    {#each gridData as name, i}
      <div class="cell">
        {#if name !== ''}
          {@html svgIcons[name]} <!-- Pixel switch -->
        {/if}
      </div>
    {/each}
  </div>
</div>

<style>
  .grid-container {
    width: 50rem;
    height: 32rem;
    overflow: hidden; /* Ensure the grid does not overflow outside its bounds */
    position: relative;
    cursor: grab;
  }

  .grid-container:active {
    cursor: grabbing;
  }

  .grid {
    display: grid;
    grid-template-rows: repeat(var(--rows), calc(var(--cell-size) * var(--zoom)));
    grid-template-columns: repeat(var(--cols), calc(var(--cell-size) * var(--zoom)));
    gap: 1px;
    background-color: #d0d0d0;
    width: fit-content;
    height: fit-content;
    transform-origin: 0 0; /* Allow zooming and panning relative to top left */
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
</style>
