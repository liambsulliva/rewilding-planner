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
    align-items: flex-start;
    text-align: left;
    gap: 0.5rem;
    padding: 1rem 3rem;
    margin: 0 3rem;
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
      align-items: center;
    }
  }
</style>