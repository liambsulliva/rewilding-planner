<script lang="ts">
  import { onMount } from 'svelte';

  export const rows = 640;
  export const cols = 640;
  export const cellSize = 100;

  let zoomLevel = 1;
  let translateX = 0;
  let translateY = 0;
  let isPanning = false;
  let startX = 0;
  let startY = 0;
  const bufferCells = 10;
  
  const viewportWidth = 50 * 16;
  const viewportHeight = 32 * 16;

  const svgIcons = {
    tree: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M6 7a6 6 0 1 1 11.95.775A6 6 0 0 1 15 19h-2v3h-2v-3H8.5A5.5 5.5 0 0 1 6.191 8.507A6 6 0 0 1 6 7m1.01 3.332A3.502 3.502 0 0 0 8.5 17H15a4 4 0 0 0 1.454-7.728l-.841-.328C15.79 8.304 16 7.672 16 7a4 4 0 1 0-6.4 3.2l-1.2 1.6a6 6 0 0 1-1.39-1.468"/></svg>`,
    water: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 16 16"><path fill="currentColor" d="M12 2a.75.75 0 0 1 .696.471c.148.369.375.636.598.808c.242.185.422.219.456.219a.75.75 0 0 1 0 1.5c-.466 0-.96-.216-1.37-.53q-.196-.15-.38-.344a2.76 2.76 0 0 1-2 .874a2.76 2.76 0 0 1-2-.873a2.76 2.76 0 0 1-2 .873a2.76 2.76 0 0 1-2-.873q-.184.194-.38.345c-.409.314-.903.53-1.37.53a.75.75 0 0 1 0-1.5c.033 0 .214-.034.455-.22c.224-.171.451-.44.599-.808a.75.75 0 0 1 1.392 0c.298.742.84 1.026 1.304 1.026s1.007-.284 1.304-1.027a.75.75 0 0 1 1.392 0c.297.743.84 1.027 1.304 1.027s1.007-.285 1.304-1.027A.75.75 0 0 1 12 2m0 4a.75.75 0 0 1 .696.471c.148.369.375.636.598.808c.242.185.422.219.456.219a.75.75 0 0 1 0 1.5c-.466 0-.96-.216-1.37-.53q-.196-.15-.38-.344a2.76 2.76 0 0 1-2 .874a2.76 2.76 0 0 1-2-.873a2.76 2.76 0 0 1-2 .873a2.76 2.76 0 0 1-2-.873q-.184.194-.38.345c-.409.314-.903.53-1.37.53a.75.75 0 0 1 0-1.5c.033 0 .214-.034.455-.22c.224-.171.451-.44.599-.808a.75.75 0 0 1 1.392 0c.298.742.84 1.026 1.304 1.026s1.007-.284 1.304-1.027a.75.75 0 0 1 1.392 0c.297.743.84 1.027 1.304 1.027s1.007-.285 1.304-1.027A.75.75 0 0 1 12 6m.696 4.471a.75.75 0 0 0-1.392 0c-.297.742-.84 1.027-1.304 1.027s-1.007-.284-1.304-1.027a.75.75 0 0 0-1.392 0c-.298.742-.84 1.027-1.304 1.027s-1.006-.284-1.304-1.027a.75.75 0 0 0-1.392 0c-.148.37-.375.637-.599.81c-.241.185-.422.219-.455.219a.75.75 0 1 0 0 1.5c.467 0 .961-.216 1.37-.53q.196-.15.38-.345a2.76 2.76 0 0 0 2 .873a2.76 2.76 0 0 0 2-.873a2.76 2.76 0 0 0 2 .873a2.76 2.76 0 0 0 2-.874q.184.194.38.344c.41.314.904.53 1.37.53a.75.75 0 0 0 0-1.5c-.034 0-.214-.034-.456-.22a1.9 1.9 0 0 1-.598-.807"/></svg>`,
    animal1: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M7.75 19a2.75 2.75 0 0 1-2.745-2.582L5 16.25V15a3 3 0 1 1 2.562-4.56a4.5 4.5 0 0 1 1.68-.432L9.5 10h4l.248.007l.245.02l.127.017l.11-.167l.131-.178l-1.777-1.777c-.7-.7-.773-1.788-.22-2.57l.103-.134l.117-.128c.74-.74 1.918-.78 2.705-.117l.127.117l5.412 5.413a4 4 0 0 1-2.642 6.824l-.225.004l-.182-.007l-.026.064a2.75 2.75 0 0 1-2.138 1.588l-.192.019l-.174.005zm6.605-12.849a.502.502 0 0 0-.768.641l.058.07l2.808 2.808l-.638.642q-.316.317-.523.696l-.097.192l-.266.584l-.618-.173a3 3 0 0 0-.604-.104l-.208-.007H9.5c-.7 0-1.343.24-1.853.64l-.143.12l-.165.16l-.093.1l-.111.134l-.121.167l-.042.064q-.062.095-.115.196l-.058.112l-.062.137l-.034.084l-.051.142l-.055.184a3 3 0 0 0-.062.297l-.011.083l-.018.189l-.006.191v1.75c0 .648.492 1.18 1.122 1.244l.128.006h4.251v-.246a1.25 1.25 0 0 0-1.121-1.244l-.128-.006h-1a.75.75 0 0 1-.102-1.494l.102-.006h1a2.75 2.75 0 0 1 2.745 2.582l.005.168l-.001.246h1.749c.591 0 1.094-.414 1.218-.975l.02-.122l.1-.84l.822.198a2.5 2.5 0 0 0 2.48-4.067l-.122-.13zM5 10.501a1.5 1.5 0 0 0-.145 2.992l.145.006l.114-.005l.005-.025q.053-.224.126-.438l.097-.255l.106-.236l.057-.113l.13-.234l.088-.14l.145-.21l.074-.098l.108-.134l.129-.147l.15-.157c-.21-.4-.59-.69-1.037-.778l-.151-.022z"/></svg>`,
    animal2: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 16 16"><path fill="currentColor" d="M7.343 3.988c-1.856 0-3.032 1.316-3.484 2.808l-.06.2H2.497a.5.5 0 0 0-.5.5c0 .685.19 1.328.522 1.813c.117.17.256.327.415.458l-.299.725a1.094 1.094 0 0 0 1.012 1.51H4.72c.424 0 .81-.244.99-.628l.304-.645a10.7 10.7 0 0 0 2.746 0l.303.645c.18.384.567.629.99.629h1.063a1.093 1.093 0 0 0 1.012-1.512l-.202-.49h.965c.617 0 1.112-.524 1.112-1.132v-.62c0-.94-.734-1.75-1.69-1.75h-1.464c-.534-1.385-1.793-2.51-3.506-2.51m4.244 5.013L11.154 7.5h1.159c.357 0 .69.314.69.75v.62a.14.14 0 0 1-.041.097c-.028.028-.055.035-.071.035zm-.655 1.214l.271.657a.094.094 0 0 1-.087.13h-1.062a.09.09 0 0 1-.086-.054l-.189-.401q.582-.134 1.153-.332m-5.937.332l-.19.401a.09.09 0 0 1-.085.055H3.647a.094.094 0 0 1-.087-.13l.272-.66q.575.2 1.163.335M3.496 7.996l-.202.67a2.1 2.1 0 0 1-.25-.67zm1.32-.91c.367-1.211 1.243-2.098 2.527-2.098c1.304 0 2.29.91 2.65 2.095l.63 2.181a9.75 9.75 0 0 1-6.467.003z"/></svg>`,
    animal3: `<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="currentColor" d="M15.493 3.507a1.65 1.65 0 0 0-1.5 1.643V10a.75.75 0 0 1-.75.75c-1.443 0-2.457.588-3.206 1.488c-.773.928-1.276 2.206-1.591 3.557c-.313 1.343-.427 2.696-.461 3.722a22 22 0 0 0-.012.983h7.02v-.75a2.25 2.25 0 0 0-2.249-2.25h-1.25a.75.75 0 0 1 0-1.5h1.25a3.75 3.75 0 0 1 3.748 3.75v.75h.75a.75.75 0 0 0 .75-.75v-10A.75.75 0 0 1 18.74 9h.506a1.25 1.25 0 0 0 1.062-1.909l-.62-1a1.25 1.25 0 0 0-1.061-.591h-2.386a.75.75 0 0 1-.75-.75zM6.473 20.5c-.002-.284 0-.634.013-1.033c.036-1.083.157-2.542.5-4.012c.34-1.462.915-2.996 1.899-4.177c.872-1.047 2.055-1.801 3.61-1.985V5.15A3.15 3.15 0 0 1 15.641 2c.746 0 1.35.604 1.35 1.35V4h1.636c.95 0 1.834.492 2.335 1.3l.62 1c1.092 1.763-.084 4.02-2.093 4.19v9.26A2.25 2.25 0 0 1 17.242 22H5.795a3.797 3.797 0 0 1-2.775-6.39l1.135-1.217a3.06 3.06 0 0 0-.073-4.248L2.969 9.03a.75.75 0 0 1 1.06-1.06l1.114 1.114a4.56 4.56 0 0 1 .11 6.333l-1.136 1.216a2.3 2.3 0 0 0 1.68 3.867z"/></svg>`
  }

  // Function to randomly pick an SVG or nothing for each cell
  function randomizeSVG() {
    const num = Math.random();
    if (num > 0.66) return 'tree';
    if (num > 0.33) return 'water';
    if (num > 0.32) return 'animal1';
    if (num > 0.31) return 'animal2';
    if (num > 0.30) return 'animal3';
    return '';
  }

  // Generates grid data
  let gridContainer: HTMLDivElement;

  // Generate memoized grid data
  const gridData: string[][] = Array(rows).fill(null).map(() => 
    Array(cols).fill(null).map(() => randomizeSVG())
  );

  let visibleCells: { row: number, col: number, svg: string }[] = [];

  // Zoom detection logic
  window.addEventListener('wheel', (event) => {
    if (event.ctrlKey) {
      zoomLevel = Math.max(0.5, Math.min(2, zoomLevel - event.deltaY * 0.001));
      event.preventDefault();
      updateVisibleCells();
    }
  });

  function areAdjacentCellsNotTrees(row: number, col: number): boolean {
  const adjacentOffsets = [-1, 0, 1];
  for (let dx of adjacentOffsets) {
    for (let dy of adjacentOffsets) {
      const adjRow = row + dy;
      const adjCol = col + dx;
      if (adjRow >= 0 && adjRow < rows && adjCol >= 0 && adjCol < cols) {
        if (gridData[adjRow][adjCol] === 'tree') {
          return false;
        }
      }
    }
  }
  return true;
}

function cutDownTree(row: number, col: number) {
  if (gridData[row][col] === 'tree') {
    gridData[row][col] = ''; // Remove the tree

    // Check if adjacent cells are empty
    if (areAdjacentCellsNotTrees(row, col)) {
      // 10% chance to spawn an animal
      if (Math.random() < 0.33) {
        const animals = ['animal1', 'animal2', 'animal3'];
        const randomAnimal = animals[Math.floor(Math.random() * animals.length)];
        gridData[row][col] = randomAnimal; // Place the animal
      }
    }
    updateVisibleCells(); // Refresh the visible grid
  }
}

  function updateVisibleCells() {
    const cellWidth = cellSize * zoomLevel;
    const cellHeight = cellSize * zoomLevel;

    const startCol = Math.max(0, Math.floor(-translateX / cellWidth) - bufferCells);
    const endCol = Math.min(cols - 1, Math.ceil((viewportWidth - translateX) / cellWidth));
    const startRow = Math.max(0, Math.floor(-translateY / cellHeight) - bufferCells);
    const endRow = Math.min(rows - 1, Math.ceil((viewportHeight - translateY) / cellHeight));

    visibleCells = [];
    for (let row = startRow; row <= endRow; row++) {
      for (let col = startCol; col <= endCol; col++) {
        visibleCells.push({ row, col, svg: gridData[row][col] });
      }
    }
  }

  function handleMouseClick(row: number, col: number) {
  // Prevents panning behavior when clicking
  isPanning = false;
  cutDownTree(row, col);
}

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
    updateVisibleCells();
  }

  // Mouse up event to stop panning
  function handleMouseUp() {
    isPanning = false;
  }

  onMount(() => {
    updateVisibleCells();
  });

</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div 
  bind:this={gridContainer}
  class="grid-container border border-neutral-200 dark:border-neutral-500 rounded-lg" 
  on:mousedown={handleMouseDown}
  on:mousemove={handleMouseMove} 
  on:mouseup={handleMouseUp} 
  on:mouseleave={handleMouseUp}>

  <div class="grid" style="--rows: {rows}; --cols: {cols}; --cell-size: {cellSize}px; --zoom: {zoomLevel}; transform: translate({translateX}px, {translateY}px) scale({zoomLevel});">
    {#each visibleCells as { row, col, svg }}
      <button
        class="cell {svg}" 
        style="grid-row: {row + 1}; grid-column: {col + 1};"
        on:click={() => handleMouseClick(row, col)} 
      >
        {#if svg !== ''}
          {@html svgIcons[svg]}
        {/if}
  </button>
    {/each}
  </div>
</div>

<style>
  .grid-container {
    width: 50rem;
    height: 32rem;
    max-width: calc(var(--cols) * (var(--cell-size) + 1px) - 1px);
    max-height: calc(var(--rows) * (var(--cell-size) + 1px) - 1px);
    overflow: hidden; /* Ensure the grid does not overflow outside its bounds */
    position: relative;
    cursor: grab;
  }

  .grid-container:active {
    cursor: grabbing;
  }

  .grid {
  display: grid;
  grid-template-rows: repeat(var(--rows), var(--cell-size));
  grid-template-columns: repeat(var(--cols), var(--cell-size));
  gap: 1px;
  background-color: #d0d0d0;
  width: calc(var(--cols) * (var(--cell-size) + 1px) - 1px);
  height: calc(var(--rows) * (var(--cell-size) + 1px) - 1px);
  transform-origin: 0 0;
}

.cell {
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
}

@media (prefers-color-scheme: dark) {
  .cell {
    background-color: #151515;
  }
}

  .cell :global(svg) {
    width: 100%;
    height: 100%;
  }
</style>
