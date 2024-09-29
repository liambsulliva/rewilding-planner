<script lang="ts">
  import Submit from './Submit.svelte';
</script>
<div class="stats-box">
    <p>Biodiversity: <strong>0.472</strong></p>
    <p>Carbon: <strong>32.4ppm</strong></p>
    <div class="my-2">
        <Submit />
    </div>
</div>
<style>
  .stats-box {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 1rem;
    border-radius: 8px;
    z-index: 10;
  }
  
  .stats-box p {
    font-family: 'Geist Mono', monospace;
    font-size: 1rem;
  }

  @media (max-width: 1450px) {
    .stats-box {
      flex-direction: row;
      gap: 1rem;
      justify-content: center;
      align-items: center;
      margin: 0 0 1rem 4rem;
      padding: 0 0 1rem 4rem;
    }
  }
</style>