<svelte:head>
  <title>Student App</title>
</svelte:head>

<div class="shell">
  <header>
    <h1>AdaptiveLabs Student App</h1>
  </header>
  <slot />
</div>

<style>
  .shell {
    min-height: 100vh;
    background: linear-gradient(180deg, #f8fbff 0%, #eef3fb 100%);
    color: #0f172a;
  }

  header {
    border-bottom: 1px solid #d7deea;
    background: #ffffff;
    padding: 0.75rem 1rem;
  }

  h1 {
    margin: 0;
    font-size: 1.1rem;
  }
</style>
