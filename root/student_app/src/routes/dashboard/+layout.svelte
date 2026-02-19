<section class="dashboard-layout">
  <h2>Dashboard</h2>
  <slot />
</section>

<style>
  .dashboard-layout {
    max-width: 1100px;
    margin: 1rem auto;
    padding: 0 1rem 1rem;
    display: grid;
    gap: 0.8rem;
  }

  h2 {
    margin: 0;
    font-size: 1.3rem;
  }
</style>
