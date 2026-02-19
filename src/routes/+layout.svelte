<svelte:head>
    <title>AdaptiveLabs AI</title>
</svelte:head>

<div class="app-shell">
    <header class="layout-banner">Layout is active</header>
    <slot />
</div>

<style>
    .app-shell {
        min-height: 100vh;
    }

    .layout-banner {
        padding: 0.75rem 1rem;
        background: #0f172a;
        color: #f8fafc;
        font-size: 0.9rem;
        font-weight: 600;
    }
</style>
