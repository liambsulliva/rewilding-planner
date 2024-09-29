<script lang="ts">
  import "./app.css";
  import '@fontsource/geist-sans/700.css';
  import '@fontsource/geist-mono/700.css';
  import Grid from './lib/Grid.svelte'
  import Footer from './lib/Footer.svelte';
  import Stats from './lib/Stats.svelte';
</script>

<main>
  <h1 class="header font-bold">Rewilding Simulation</h1>
  <div class="relative flex flex-col items-center p-6">
    <Grid />
    <div style="max-width: calc(100vw - 2rem);" class="absolute top-6 right-20">
      <Stats />
    </div>
  </div>
  <Footer />
</main>


<style>
  :root {
    overflow: hidden;
  }
  .header {
    font-family: 'Geist Sans', Helvetica, sans-serif;
  }
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
