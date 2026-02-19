<script>
    export let armIndex = null;

    const FEEDBACK_URL = "http://localhost:8000/api/v1/feedback";

    let submitting = false;
    let feedbackMessage = "";
    let feedbackError = "";

    async function sendFeedback(reward) {
        feedbackMessage = "";
        feedbackError = "";

        if (armIndex === null || armIndex === undefined) {
            feedbackError = "Generate a roadmap first so we can score the selected AI arm.";
            return;
        }

        submitting = true;
        try {
            const response = await fetch(FEEDBACK_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ arm_index: armIndex, reward }),
            });

            if (!response.ok) {
                throw new Error(`Feedback failed with status ${response.status}`);
            }

            feedbackMessage = "Feedback sent. Bandit updated.";
        } catch (e) {
            feedbackError = e instanceof Error ? e.message : "Unknown feedback error";
        } finally {
            submitting = false;
        }
    }
</script>

<section class="feedback-card">
    <h3>Roadmap Feedback</h3>
    <p>Rate the generated roadmap to train the Thompson Sampling bandit.</p>

    <div class="feedback-actions">
        <button disabled={submitting} on:click={() => sendFeedback(1.0)}>Helpful</button>
        <button disabled={submitting} on:click={() => sendFeedback(0.0)}>Not helpful</button>
    </div>

    {#if feedbackMessage}
        <p class="ok">{feedbackMessage}</p>
    {/if}

    {#if feedbackError}
        <p class="error">{feedbackError}</p>
    {/if}
</section>

<style>
    .feedback-card {
        border: 1px solid #d6deea;
        border-radius: 0.5rem;
        background: #ffffff;
        padding: 1rem;
        display: grid;
        gap: 0.5rem;
    }

    .feedback-card h3 {
        margin: 0;
    }

    .feedback-card p {
        margin: 0;
    }

    .feedback-actions {
        display: flex;
        gap: 0.5rem;
    }

    .feedback-actions button {
        width: auto;
    }

    .ok {
        color: #166534;
        font-weight: 600;
    }

    .error {
        color: #b00020;
        font-weight: 600;
    }
</style>
