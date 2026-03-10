<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  
  let subject = '';
  let hours = 0;
  let step = 1;
  let loading = false;
  let survivalPlan = null;
  
  // Form data - Step 1
  let knownUnits = [];
  let unknownUnits = [];
  let highMarkUnits = '';
  let studyHours = 4;
  let studyLocation = 'home';
  
  // Double exam detection
  let isDoubleExam = false;
  let exam2 = null;
  
  onMount(() => {
    const params = new URLSearchParams($page.url.search);
    subject = params.get('subject') || '';
    hours = parseInt(params.get('hours')) || 0;
    
    // Check for double exam scenario
    checkDoubleExam();
  });
  
  function checkDoubleExam() {
    // This would check if there are multiple exams on the same day
    // For now, simulate with demo data
    const today = new Date();
    const mockExams = [
      { subject: subject, time: '9:00 AM', date: today },
      { subject: 'Mathematics', time: '2:00 PM', date: today }
    ];
    
    if (mockExams.length > 1) {
      isDoubleExam = true;
      exam2 = mockExams[1];
    }
  }
  
  function handleUnitToggle(unit, type) {
    if (type === 'known') {
      if (knownUnits.includes(unit)) {
        knownUnits = knownUnits.filter(u => u !== unit);
      } else {
        knownUnits.push(unit);
        unknownUnits = unknownUnits.filter(u => u !== unit);
      }
    } else {
      if (unknownUnits.includes(unit)) {
        unknownUnits = unknownUnits.filter(u => u !== unit);
      } else {
        unknownUnits.push(unit);
        knownUnits = knownUnits.filter(u => u !== unit);
      }
    }
  }
  
  async function buildSurvivalPlan() {
    loading = true;
    
    // Simulate API call - in production would call backend
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Generate survival plan
    survivalPlan = generatePlan();
    step = 2;
    loading = false;
  }
  
  function generatePlan() {
    const bedtime = new Date();
    bedtime.setHours(1, 0, 0, 0); // Never plan past 1am
    
    const now = new Date();
    const availableMinutes = studyHours * 60;
    
    if (isDoubleExam) {
      return {
        hardTruth: `You have two exams today. This is not ideal. The goal is damage control - maximize marks on ${subject} in the morning, then recover before Mathematics.`,
        focusOn: [subject],
        triage: ['Mathematics'],
        tonight: [
          `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}pm — ${subject} review (40 min)`,
          `Read your notes once. Write 5 key points from memory.`,
          `${(now.getHours() + 1)}:${String(now.getMinutes()).padStart(2, '0')}pm — Sleep (8 hours minimum)`,
          `No midnight cramming. Sleep is your best tool.`
        ],
        examTechnique: [
          `${subject}: Answer known questions first, skip unknown, return if time`,
          `Between exams: 45 min recovery. No studying Mathematics immediately`,
          `Mathematics: Focus on basics, don't panic about complex problems`
        ],
        realisticOutcome: `Likely: 60-75% in ${subject}, 40-55% in Mathematics`,
        bestCase: `If ${subject} favors strong topics: 80%+ in ${subject}`,
        worstCase: `If both exams favor weak topics: 50-60% overall`
      };
    }
    
    return {
      hardTruth: `You cannot cover all topics properly in ${hours} hours. The goal is to maximize marks, not to understand everything. Reviewing known material is 4x more effective than learning new material under stress.`,
      focusOn: knownUnits.length > 0 ? knownUnits : ['Unit 1', 'Unit 2'],
      triage: unknownUnits.length > 0 ? unknownUnits : ['Complex topics'],
      tonight: [
        `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}pm — ${knownUnits[0] || 'Unit 1'} review (40 min)`,
        `Read your notes once. Write 5 key points from memory.`,
        `${(now.getHours() + 1)}:${String(now.getMinutes()).padStart(2, '0')}pm — Practice problems (30 min)`,
        `Focus on patterns, not perfect solutions.`,
        `${(now.getHours() + 2)}:${String(now.getMinutes()).padStart(2, '0')}pm — Quick scan of ${unknownUnits[0] || 'one unknown topic'} (10 min)`,
        `One definition, one formula. Move on.`,
        `${(now.getHours() + 2.5)}:${String(now.getMinutes()).padStart(2, '0')}pm — Sleep`,
        `Never plan past 1am. Sleep is non-negotiable.`
      ],
      examTechnique: [
        `Read all questions first. Answer known units first.`,
        `Partial marks exist for unknowns - never leave blank.`,
        `Show your work. Process marks count.`,
        `If stuck, move on. Return with fresh eyes.`
      ],
      realisticOutcome: `Likely: ${Math.min(85, 45 + knownUnits.length * 10)}-${Math.min(95, 55 + knownUnits.length * 10)} marks`,
      bestCase: `If exam favors strong topics: ${Math.min(100, 65 + knownUnits.length * 8)}+`,
      worstCase: `If exam favors weak topics: ${Math.max(30, 35 + knownUnits.length * 5)}-${Math.max(45, 40 + knownUnits.length * 5)}`
    };
  }
  
  function goToDashboard() {
    window.location.href = '/dashboard';
  }
</script>

<div class="crisis-page">
  <!-- Back link -->
  <a href="/dashboard" class="back-link">← Dashboard</a>
  
  {#if isDoubleExam}
    <!-- Double Exam Scenario -->
    <div class="crisis-container">
      <h1 class="crisis-title">You have two exams today</h1>
      <div class="exam-info">
        <div class="exam-item">
          <strong>{subject}</strong> at 9:00 AM
        </div>
        <div class="exam-item">
          <strong>{exam2.subject}</strong> at {exam2.time}
        </div>
      </div>
      
      <div class="strategy-box">
        <h2>Tonight: Focus ONLY on {subject}</h2>
        <p>Do not touch {exam2.subject}. Split attention tonight helps neither subject.</p>
        
        <h3>Between exams:</h3>
        <p>45 min recovery after {subject} finishes. Do not open {exam2.subject} notes immediately.</p>
        
        <h3>Then:</h3>
        <p>2 hours {exam2.subject} only before the afternoon exam.</p>
      </div>
      
      <button class="crisis-btn" on:click={buildSurvivalPlan}>
        Build My Survival Plan
      </button>
    </div>
  {:else if step === 1}
    <!-- Step 1: Triage Input -->
    <div class="crisis-container">
      <h1 class="crisis-title">{subject} exam in {hours} hours</h1>
      <p class="crisis-subtitle">Let's be realistic about what is possible</p>
      
      <div class="form-section">
        <h2>Which units have you seen before, even once?</h2>
        <div class="units-grid">
          {#each ['Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5', 'Unit 6', 'Unit 7', 'Unit 8'] as unit}
            <label class="unit-checkbox">
              <input 
                type="checkbox" 
                checked={knownUnits.includes(unit)}
                on:change={() => handleUnitToggle(unit, 'known')}
              />
              <span class="checkmark"></span>
              {unit}
            </label>
          {/each}
        </div>
      </div>
      
      <div class="form-section">
        <h2>Which units carry the most marks? (optional)</h2>
        <input 
          type="text" 
          bind:value={highMarkUnits} 
          placeholder="e.g., Unit 3, Unit 5"
          class="text-input"
        />
      </div>
      
      <div class="form-section">
        <h2>How many hours can you actually study tonight?</h2>
        <div class="slider-container">
          <input 
            type="range" 
            min="1" 
            max="10" 
            bind:value={studyHours}
            class="slider"
          />
          <span class="slider-value">{studyHours} hours</span>
        </div>
      </div>
      
      <div class="form-section">
        <h2>Where are you studying?</h2>
        <div class="radio-group">
          <label class="radio-option">
            <input type="radio" bind:group={studyLocation} value="home" />
            <span class="radio-dot"></span>
            Alone at home
          </label>
          <label class="radio-option">
            <input type="radio" bind:group={studyLocation} value="library" />
            <span class="radio-dot"></span>
            Library
          </label>
          <label class="radio-option">
            <input type="radio" bind:group={studyLocation} value="others" />
            <span class="radio-dot"></span>
            With others nearby
          </label>
        </div>
      </div>
      
      <button class="crisis-btn" on:click={buildSurvivalPlan} disabled={loading}>
        {#if loading}
          Building plan...
        {:else}
          Build my survival plan
        {/if}
      </button>
    </div>
  {:else if step === 2 && survivalPlan}
    <!-- Step 2: Survival Plan Output -->
    <div class="plan-container">
      <div class="plan-section">
        <h1>HARD TRUTH</h1>
        <p class="hard-truth">{survivalPlan.hardTruth}</p>
      </div>
      
      <div class="plan-section">
        <h1>FOCUS ON THESE</h1>
        <ul class="focus-list">
          {#each survivalPlan.focusOn as unit}
            <li>{unit}</li>
          {/each}
        </ul>
        <p class="strategy-note">Reviewing known material is 4x more effective than learning new material under stress and time pressure.</p>
      </div>
      
      <div class="plan-section">
        <h1>TRIAGE THESE</h1>
        <ul class="triage-list">
          {#each survivalPlan.triage as unit}
            <li>{unit}</li>
          {/each}
        </ul>
        <p class="strategy-note">10 minutes each maximum. One definition, one formula. Move on.</p>
      </div>
      
      <div class="plan-section">
        <h1>TONIGHT</h1>
        <ul class="tonight-list">
          {#each survivalPlan.tonight as item}
            <li>{item}</li>
          {/each}
        </ul>
      </div>
      
      <div class="plan-section">
        <h1>EXAM TECHNIQUE</h1>
        <ul class="technique-list">
          {#each survivalPlan.examTechnique as technique}
            <li>{technique}</li>
          {/each}
        </ul>
      </div>
      
      <div class="plan-section">
        <h1>REALISTIC OUTCOME</h1>
        <p class="outcome">{survivalPlan.realisticOutcome}</p>
        {#if survivalPlan.bestCase}
          <p class="outcome best">If exam favors strong topics: {survivalPlan.bestCase}</p>
        {/if}
        {#if survivalPlan.worstCase}
          <p class="outcome worst">If exam favors weak topics: {survivalPlan.worstCase}</p>
        {/if}
      </div>
      
      <button class="dashboard-btn" on:click={goToDashboard}>
        Back to Dashboard
      </button>
    </div>
  {/if}
</div>

<style>
  .crisis-page {
    min-height: 100vh;
    background: var(--bg);
    color: var(--text-primary);
    font-family: var(--font-sans);
    padding: 20px;
  }
  
  .back-link {
    color: var(--text-muted);
    text-decoration: none;
    font-size: 14px;
    margin-bottom: 40px;
    display: inline-block;
  }
  
  .crisis-container, .plan-container {
    max-width: 600px;
    margin: 0 auto;
  }
  
  .crisis-title {
    font-size: 32px;
    font-weight: 700;
    margin: 0 0 12px 0;
    color: #ef4444;
  }
  
  .crisis-subtitle {
    font-size: 16px;
    color: var(--text-muted);
    margin: 0 0 40px 0;
  }
  
  .exam-info {
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: var(--radius-card);
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .exam-item {
    font-size: 18px;
    margin: 8px 0;
  }
  
  .strategy-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 24px;
    margin-bottom: 30px;
  }
  
  .strategy-box h2 {
    color: var(--accent);
    margin: 0 0 12px 0;
  }
  
  .strategy-box h3 {
    color: var(--text-primary);
    margin: 20px 0 8px 0;
  }
  
  .strategy-box p {
    color: var(--text-muted);
    margin: 0 0 16px 0;
  }
  
  .form-section {
    margin-bottom: 32px;
  }
  
  .form-section h2 {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 16px 0;
    color: var(--text-primary);
  }
  
  .units-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 12px;
  }
  
  .unit-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 12px;
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    transition: all 0.2s ease;
  }
  
  .unit-checkbox:hover {
    border-color: var(--accent);
  }
  
  .unit-checkbox input[type="checkbox"] {
    display: none;
  }
  
  .checkmark {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  
  .unit-checkbox input:checked ~ .checkmark {
    background: var(--accent);
    border-color: var(--accent);
  }
  
  .unit-checkbox input:checked ~ .checkmark::after {
    content: '✓';
    color: #000;
    font-size: 10px;
    font-weight: bold;
  }
  
  .text-input {
    width: 100%;
    padding: 12px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    color: var(--text-primary);
    font-size: 14px;
  }
  
  .slider-container {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .slider {
    flex: 1;
    -webkit-appearance: none;
    height: 6px;
    border-radius: 3px;
    background: var(--border);
    outline: none;
  }
  
  .slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--accent);
    cursor: pointer;
  }
  
  .slider-value {
    color: var(--accent);
    font-weight: 600;
    min-width: 60px;
  }
  
  .radio-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .radio-option {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 12px;
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    transition: all 0.2s ease;
  }
  
  .radio-option:hover {
    border-color: var(--accent);
  }
  
  .radio-option input[type="radio"] {
    display: none;
  }
  
  .radio-dot {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  }
  
  .radio-option input:checked ~ .radio-dot {
    background: var(--accent);
    border-color: var(--accent);
  }
  
  .radio-option input:checked ~ .radio-dot::after {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #000;
  }
  
  .crisis-btn, .dashboard-btn {
    width: 100%;
    padding: 16px;
    background: #ef4444;
    color: white;
    border: none;
    border-radius: var(--radius-input);
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .crisis-btn:hover:not(:disabled), .dashboard-btn:hover {
    filter: brightness(1.1);
  }
  
  .crisis-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .dashboard-btn {
    background: var(--accent);
    color: #000;
    margin-top: 40px;
  }
  
  .plan-section {
    margin-bottom: 40px;
  }
  
  .plan-section h1 {
    font-size: 24px;
    font-weight: 700;
    margin: 0 0 16px 0;
    color: var(--accent);
  }
  
  .hard-truth {
    font-size: 16px;
    line-height: 1.6;
    color: var(--text-primary);
    font-style: italic;
  }
  
  .focus-list, .triage-list, .tonight-list, .technique-list {
    margin: 0 0 16px 0;
    padding-left: 20px;
  }
  
  .focus-list li, .triage-list li, .tonight-list li, .technique-list li {
    margin-bottom: 8px;
    color: var(--text-primary);
  }
  
  .strategy-note {
    font-size: 14px;
    color: var(--text-muted);
    font-style: italic;
    margin: 0;
  }
  
  .outcome {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 8px 0;
  }
  
  .outcome.best {
    color: var(--accent);
  }
  
  .outcome.worst {
    color: #f97316;
  }
  
  @media (max-width: 640px) {
    .crisis-page {
      padding: 16px;
    }
    
    .crisis-title {
      font-size: 24px;
    }
    
    .units-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
