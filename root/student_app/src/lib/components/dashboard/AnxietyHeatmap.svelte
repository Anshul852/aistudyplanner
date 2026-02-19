<script>
	let { roadmap = [] } = $props();

	function getDayIntensity(dayPlan) {
		if (!dayPlan || dayPlan.length === 0) return 0;
		return dayPlan.reduce((sum, topic) => sum + (topic.weight || topic.weight || 1), 0);
	}

	function getIntensityColor(intensity) {
		if (intensity === 0) return '#e8f5e9';
		if (intensity <= 3) return '#fff3e0';
		if (intensity <= 6) return '#ffe0b2';
		if (intensity <= 9) return '#ffb74d';
		return '#ff8a65';
	}
</script>

<div class="heatmap">
	<div class="heatmap-grid">
		{#each roadmap as dayPlan, index}
			<div 
				class="day-cell" 
				style="background-color: {getIntensityColor(getDayIntensity(dayPlan))}"
			>
				<span class="day-label">Day {index + 1}</span>
				<span class="intensity-value">{getDayIntensity(dayPlan)}</span>
			</div>
		{/each}
	</div>
	
	<div class="legend">
		<span class="legend-item">
			<span class="legend-color" style="background: #e8f5e9"></span> Rest
		</span>
		<span class="legend-item">
			<span class="legend-color" style="background: #fff3e0"></span> Light
		</span>
		<span class="legend-item">
			<span class="legend-color" style="background: #ffe0b2"></span> Moderate
		</span>
		<span class="legend-item">
			<span class="legend-color" style="background: #ffb74d"></span> Heavy
		</span>
		<span class="legend-item">
			<span class="legend-color" style="background: #ff8a65"></span> Intense
		</span>
	</div>
</div>

<style>
	.heatmap {
		font-family: sans-serif;
	}

	.heatmap-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
		gap: 8px;
		margin-bottom: 1rem;
	}

	.day-cell {
		padding: 1rem;
		border-radius: 4px;
		text-align: center;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 60px;
		transition: transform 0.2s;
	}

	.day-cell:hover {
		transform: scale(1.05);
	}

	.day-label {
		font-size: 0.75rem;
		font-weight: bold;
		color: #333;
	}

	.intensity-value {
		font-size: 1.25rem;
		font-weight: bold;
		color: #333;
	}

	.legend {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		justify-content: center;
		margin-top: 1rem;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: 4px;
		font-size: 0.75rem;
	}

	.legend-color {
		width: 16px;
		height: 16px;
		border-radius: 2px;
	}
</style>
