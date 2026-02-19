<script>
	let { roadmap = [] } = $props();

	let streakDays = $derived.by(() => {
		if (!roadmap || roadmap.length === 0) return 0;
		
		let streak = 0;
		for (const dayPlan of roadmap) {
			if (dayPlan && dayPlan.length > 0) {
				streak++;
			} else {
				break;
			}
		}
		return streak;
	});

	let totalStudyDays = $derived.by(() => {
		if (!roadmap) return 0;
		return roadmap.filter(day => day && day.length > 0).length;
	});

	let completionPercentage = $derived.by(() => {
		if (!roadmap || roadmap.length === 0) return 0;
		return Math.round((totalStudyDays / roadmap.length) * 100);
	});
</script>

<div class="streak-counter">
	<div class="streak-display">
		<span class="streak-number">{streakDays}</span>
		<span class="streak-label">Day Streak</span>
	</div>

	<div class="stats">
		<div class="stat-item">
			<span class="stat-value">{totalStudyDays}</span>
			<span class="stat-label">Total Study Days</span>
		</div>
		<div class="stat-item">
			<span class="stat-value">{completionPercentage}%</span>
			<span class="stat-label">Completion</span>
		</div>
	</div>

	<div class="progress-bar">
		<div class="progress-fill" style="width: {completionPercentage}%"></div>
	</div>
</div>

<style>
	.streak-counter {
		font-family: sans-serif;
		text-align: center;
	}

	.streak-display {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-bottom: 1.5rem;
	}

	.streak-number {
		font-size: 3rem;
		font-weight: bold;
		color: #4a90d9;
		line-height: 1;
	}

	.streak-label {
		font-size: 0.875rem;
		color: #666;
		text-transform: uppercase;
		letter-spacing: 1px;
	}

	.stats {
		display: flex;
		justify-content: space-around;
		margin-bottom: 1rem;
	}

	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.stat-value {
		font-size: 1.5rem;
		font-weight: bold;
		color: #333;
	}

	.stat-label {
		font-size: 0.75rem;
		color: #666;
	}

	.progress-bar {
		height: 8px;
		background: #e0e0e0;
		border-radius: 4px;
		overflow: hidden;
	}

	.progress-fill {
		height: 100%;
		background: linear-gradient(90deg, #4a90d9, #67b26f);
		transition: width 0.3s ease;
	}
</style>
