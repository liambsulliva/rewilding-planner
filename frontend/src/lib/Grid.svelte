<script lang="ts">
    export let name: IconName = 'heart';
    export let rows = 3;
    export let cols = 3;
    export let cellSize = 100;
    type IconName = 'heart' | 'star' | 'circle';

    interface svgIcons {
      [key: string]: string;
    }
  
    const svgIcons = {
      heart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
      </svg>`,
      star: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
      </svg>`,
      circle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
      </svg>`
    };
  
    $: svg = svgIcons[name] || '';
  </script>
  
  <div class="grid" style="--rows: {rows}; --cols: {cols}; --cell-size: {cellSize}px;">
    {#each Array(rows * cols) as _, i}
      <div class="cell">
        {@html svg}
      </div>
    {/each}
  </div>
  
  <style>
    .grid {
      display: grid;
      grid-template-rows: repeat(var(--rows), var(--cell-size));
      grid-template-columns: repeat(var(--cols), var(--cell-size));
      gap: 1px;
      background-color: #333;
      width: fit-content;
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