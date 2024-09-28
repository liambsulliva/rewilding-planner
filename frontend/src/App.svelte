<script lang="ts">
  import "./app.css";
  import Grid from './lib/Grid.svelte'
  import Footer from './lib/Footer.svelte';
</script>

<main>
  <h1 class="font-bold">Rewilding Simulation</h1>
  <div class="flex flex-col items-center p-6">
    <Grid />
  </div>
  <Footer />
</main>


<style>
  :root {
    overflow: hidden;
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
