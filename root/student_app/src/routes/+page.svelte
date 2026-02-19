<script>
  const OPTIMIZE_URL = "http://localhost:8000/api/v1/optimize-personal-roadmap";
  const FEEDBACK_URL = "http://localhost:8000/api/v1/feedback";

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
  let armIndex = null;

  async function optimizeRoadmap() {
    loading = true;
    error = "";
    roadmap = [];

    try {
      const topics = JSON.parse(topicsJson);
      const response = await fetch(OPTIMIZE_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topics, days, velocity })
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      roadmap = data.roadmap ?? [];
      armIndex = data.metadata?.arm_index ?? null;
    } catch (e) {
      error = e instanceof Error ? e.message : "Unknown optimization error";
    } finally {
      loading = false;
    }
  }

  async function sendFeedback(reward) {
    if (armIndex === null || armIndex === undefined) {
      error = "Generate a roadmap before sending feedback.";
      return;
    }

    error = "";
    try {
      const response = await fetch(FEEDBACK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ arm_index: armIndex, reward })
      });

      if (!response.ok) {
        throw new Error(`Feedback failed with status ${response.status}`);
      }
    } catch (e) {
      error = e instanceof Error ? e.message : "Unknown feedback error";
    }
  }
</script>

<main>
  <p class="hint">Primary route: <code>student_app/src/routes/+page.svelte</code></p>

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
    Topics JSON
    <textarea rows="8" bind:value={topicsJson}></textarea>
  </label>

  <button on:click={optimizeRoadmap} disabled={loading}>
    {loading ? "Optimizing..." : "Generate Roadmap"}
  </button>

  <div class="feedback">
    <button on:click={() => sendFeedback(1.0)}>Helpful</button>
    <button on:click={() => sendFeedback(0.0)}>Not Helpful</button>
  </div>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  {#if roadmap.length > 0}
    <h2>Roadmap</h2>
    <pre>{JSON.stringify(roadmap, null, 2)}</pre>
  {/if}

  <p><a href="/dashboard">Open Dashboard Components</a></p>
</main>

<style>
  main {
    max-width: 860px;
    margin: 1rem auto;
    padding: 1rem;
    display: grid;
    gap: 0.8rem;
  }

  label {
    display: grid;
    gap: 0.35rem;
  }

  input,
  select,
  textarea,
  button {
    font: inherit;
    padding: 0.55rem;
  }

  .feedback {
    display: flex;
    gap: 0.5rem;
  }

  .error {
    color: #b00020;
    font-weight: 600;
  }

  pre {
    margin: 0;
    padding: 0.75rem;
    border-radius: 10px;
    background: #0f172a;
    color: #f8fafc;
    overflow: auto;
  }

  .hint {
    margin: 0;
    color: #334155;
  }
</style>
