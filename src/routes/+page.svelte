<script>
    import FeedbackPanel from "$lib/components/FeedbackPanel.svelte";

    const API_URL = "http://localhost:8000/api/v1/optimize-personal-roadmap";

    let days = 14;
    let velocity = "Medium";
    let topicsJson = `[
  { "id": "topic-1", "name": "Linear Algebra", "weight": 3 },
  { "id": "topic-2", "name": "Calculus", "weight": 2 },
  { "id": "topic-3", "name": "Python", "weight": 2 }
]`;
    let loading = false;
    let error = "";
    let roadmap = [];
    let selectedArmIndex = null;
    let runMetadata = null;

    async function optimizeRoadmap() {
        error = "";
        loading = true;

        try {
            const topics = JSON.parse(topicsJson);
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ topics, days, velocity }),
            });

            if (!response.ok) {
                throw new Error(
                    `Request failed with status ${response.status}`,
                );
            }

            const data = await response.json();
            roadmap = data.roadmap ?? [];
            runMetadata = data.metadata ?? null;
            selectedArmIndex = runMetadata?.arm_index ?? null;
        } catch (e) {
            error = e instanceof Error ? e.message : "Unknown error";
            roadmap = [];
            runMetadata = null;
            selectedArmIndex = null;
        } finally {
            loading = false;
        }
    }
</script>

<main>
    <h1>AdaptiveLabs AI Roadmap Optimizer</h1>
    <p>Frontend (5173) -> FastAPI GA (8000)</p>

    <label>
        Days Remaining
        <input type="number" min="1" bind:value={days} />
    </label>

    <label>
        Velocity
        <select bind:value={velocity}>
            <option value="Slow">Slow</option>
            <option value="Medium">Medium</option>
            <option value="Fast">Fast</option>
        </select>
    </label>

    <label>
        Topics (JSON)
        <textarea rows="8" bind:value={topicsJson}></textarea>
    </label>

    <button on:click={optimizeRoadmap} disabled={loading}>
        {loading ? "Optimizing..." : "Generate Roadmap"}
    </button>

    {#if error}
        <p class="error">{error}</p>
    {/if}

    {#if roadmap.length > 0}
        <h2>Generated Roadmap</h2>
        <pre>{JSON.stringify(roadmap, null, 2)}</pre>

        {#if runMetadata}
            <h3>AI Configuration Used</h3>
            <pre>{JSON.stringify(runMetadata, null, 2)}</pre>
        {/if}
    {/if}

    <FeedbackPanel armIndex={selectedArmIndex} />
</main>

<style>
    :global(body) {
        margin: 0;
        font-family:
            ui-sans-serif,
            system-ui,
            -apple-system,
            Segoe UI,
            Roboto,
            Helvetica,
            Arial,
            sans-serif;
        background: #f4f6fb;
    }

    main {
        max-width: 900px;
        margin: 2rem auto;
        padding: 1rem;
        display: grid;
        gap: 1rem;
    }

    label {
        display: grid;
        gap: 0.4rem;
    }

    input,
    select,
    textarea,
    button {
        font: inherit;
        padding: 0.6rem;
    }

    textarea {
        font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }

    button {
        width: fit-content;
        cursor: pointer;
    }

    .error {
        color: #b00020;
        font-weight: 600;
    }

    pre {
        background: #111827;
        color: #f9fafb;
        padding: 1rem;
        border-radius: 0.4rem;
        overflow: auto;
    }
</style>
