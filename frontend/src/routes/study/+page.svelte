<script lang="ts">
  import { onMount } from 'svelte';
  import { authStore, user } from '$lib/stores/auth';
  import { BookOpen, Calendar, Target, TrendingUp, Brain, Shield, Settings, MessageSquare, ChevronLeft, ChevronRight, Zap } from 'lucide-svelte';
  import StatsCards from '$lib/components/dashboard/StatsCards.svelte';
  import CognitiveLoadMeter from '$lib/components/dashboard/CognitiveLoadMeter.svelte';
  import ScheduleTimeline from '$lib/components/dashboard/ScheduleTimeline.svelte';
  import StudyPlanCard from '$lib/components/dashboard/StudyPlanCard.svelte';
  import UpcomingExams from '$lib/components/dashboard/UpcomingExams.svelte';
  import LearnerTypeBadge from '$lib/components/dashboard/LearnerTypeBadge.svelte';
  import PrivacyStatusBar from '$lib/components/dashboard/PrivacyStatusBar.svelte';

  let userProfile = null;
  let loading = true;
  let mounted = false;

  $: currentUser = $user;
  $: displayName = userProfile?.display_name || currentUser?.user?.email?.split('@')[0] || 'Student';
  $: greeting = new Date().getHours() < 12 ? 'Good morning' : new Date().getHours() < 18 ? 'Good afternoon' : 'Good evening';
  $: today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });

  onMount(async () => {
    mounted = true;
    try {
      if (!currentUser) return;
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/students/profile`, {
        headers: {
          Authorization: `Bearer ${currentUser.session?.access_token}`
        }
      });

      if (response.ok) {
        userProfile = await response.json();
      }
    } catch (error) {
      console.error('Failed to fetch user profile:', error);
    } finally {
      loading = false;
    }
  });
</script>

<svelte:head>
  <title>Study Planning - StudyVault</title>
</svelte:head>

<div class="min-h-screen flex flex-col" style="background: var(--bg)">
  <!-- Header -->
  <header class="w-full px-6 py-4 border-b" style="background: var(--surface); border-color: var(--border);">
    <div class="max-w-6xl mx-auto flex items-center justify-between">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: var(--accent);">
          <BookOpen size={20} style="color: var(--bg);" />
        </div>
        <h1 class="text-2xl font-bold" style="color: var(--text-primary);">Study Planning</h1>
      </div>
      <div class="flex items-center gap-3">
        <PrivacyStatusBar />
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="flex-1 overflow-auto p-6">
    <div class="max-w-4xl mx-auto">
      <!-- Welcome Section -->
      <div class="text-center mb-8">
        <h2 class="text-4xl font-bold mb-4 tracking-tight" style="color: var(--text-primary);">
          Welcome back, <span style="color: var(--accent);">{displayName}</span>
        </h2>
        <p class="text-xl" style="color: var(--text-muted);">
          {greeting} · Let's plan your study sessions
        </p>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="rounded-2xl p-6 text-center" style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card);">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3" style="background: var(--accent);">
            <Target size={24} style="color: var(--bg);" />
          </div>
          <h3 class="text-lg font-semibold mb-2" style="color: var(--text-primary);">Study Goals</h3>
          <p class="text-3xl font-bold" style="color: var(--accent);">12</p>
          <p class="text-sm" style="color: var(--text-muted);">sessions this month</p>
        </div>

        <div class="rounded-2xl p-6 text-center" style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card);">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3" style="background: var(--color-easy);">
            <BookOpen size={24} style="color: white;" />
          </div>
          <h3 class="text-lg font-semibold mb-2" style="color: var(--text-primary);">Completed</h3>
          <p class="text-3xl font-bold" style="color: var(--color-easy);">47</p>
          <p class="text-sm" style="color: var(--text-muted);">sessions completed</p>
        </div>

        <div class="rounded-2xl p-6 text-center" style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card);">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3" style="background: var(--color-medium);">
            <TrendingUp size={24} style="color: white;" />
          </div>
          <h3 class="text-lg font-semibold mb-2" style="color: var(--text-primary);">Focus Time</h3>
          <p class="text-3xl font-bold" style="color: var(--color-medium);">127h</p>
          <p class="text-sm" style="color: var(--text-muted);">total focus time</p>
        </div>

        <div class="rounded-2xl p-6 text-center" style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card);">
          <div class="w-12 h-12 rounded-lg flex items-center justify-center mx-auto mb-3" style="background: var(--color-hard);">
            <Brain size={24} style="color: white;" />
          </div>
          <h3 class="text-lg font-semibold mb-2" style="color: var(--text-primary);">Retention Rate</h3>
          <p class="text-3xl font-bold" style="color: var(--color-hard);">89%</p>
          <p class="text-sm" style="color: var(--text-muted);">average retention</p>
        </div>
      </div>

      <!-- Planning Tools -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Study Schedule -->
        <div class="rounded-2xl p-6" style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card);">
          <div class="flex items-center gap-3 mb-4">
            <Calendar size={20} style="color: var(--accent);" />
            <h3 class="text-xl font-semibold" style="color: var(--text-primary);">Study Schedule</h3>
          </div>
          <div class="space-y-4">
            <div class="flex items-center justify-between p-4 rounded-lg" style="background: var(--surface-hover); border: 1px solid var(--border);">
              <div>
                <p class="text-sm font-medium" style="color: var(--text-primary);">Monday, March 8</p>
                <p class="text-xs" style="color: var(--text-muted);">Data Structures</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-2xl font-bold" style="color: var(--accent);">9:00 AM</span>
                <span class="text-sm" style="color: var(--text-muted);">1h 30m</span>
              </div>
            </div>

            <div class="flex items-center justify-between p-4 rounded-lg" style="background: var(--surface-hover); border: 1px solid var(--border);">
              <div>
                <p class="text-sm font-medium" style="color: var(--text-primary);">Wednesday, March 10</p>
                <p class="text-xs" style="color: var(--text-muted);">Machine Learning</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-2xl font-bold" style="color: var(--accent);">2:00 PM</span>
                <span class="text-sm" style="color: var(--text-muted);">2h</span>
              </div>
            </div>

            <div class="flex items-center justify-between p-4 rounded-lg" style="background: var(--surface-hover); border: 1px solid var(--border);">
              <div>
                <p class="text-sm font-medium" style="color: var(--text-primary);">Friday, March 12</p>
                <p class="text-xs" style="color: var(--text-muted);">Review Session</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-2xl font-bold" style="color: var(--accent);">4:00 PM</span>
                <span class="text-sm" style="color: var(--text-muted);">45m</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Study Tools -->
        <div class="rounded-2xl p-6" style="background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-card);">
          <div class="flex items-center gap-3 mb-4">
            <Zap size={20} style="color: var(--accent);" />
            <h3 class="text-xl font-semibold" style="color: var(--text-primary);">Study Tools</h3>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <button class="flex items-center gap-2 p-3 rounded-lg transition-all duration-200 hover:scale-105" style="background: var(--surface-hover); border: 1px solid var(--border);">
              <Shield size={16} style="color: var(--color-hard);" />
              <span class="text-sm font-medium" style="color: var(--text-primary);">Privacy Vault</span>
            </button>
            <button class="flex items-center gap-2 p-3 rounded-lg transition-all duration-200 hover:scale-105" style="background: var(--surface-hover); border: 1px solid var(--border);">
              <MessageSquare size={16} style="color: var(--accent);" />
              <span class="text-sm font-medium" style="color: var(--text-primary);">AI Assistant</span>
            </button>
            <button class="flex items-center gap-2 p-3 rounded-lg transition-all duration-200 hover:scale-105" style="background: var(--surface-hover); border: 1px solid var(--border);">
              <Settings size={16} style="color: var(--text-muted);" />
              <span class="text-sm font-medium" style="color: var(--text-primary);">Settings</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</div>

<script>
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      element.textContent = Math.floor(current).toString();
    }, 30);
  }

  function setupSlider() {
    const slider = document.querySelector('input[type="range"]') as HTMLInputElement;
    if (slider) {
      function updateSlider() {
        const min = parseFloat(slider.min) || 0;
        const max = parseFloat(slider.max) || 100;
        const val = ((parseFloat(slider.value) - min) / (max - min)) * 100;
        slider.style.setProperty('--val', val + '%');
      }
      slider.addEventListener('input', updateSlider);
      updateSlider();
    }
  }

  function startSession() {
    sessionActive = true;
    elapsedTime = 0;
    
    sessionInterval = setInterval(() => {
      elapsedTime++;
      if (elapsedTime >= sessionDuration * 60) {
        endSession();
      }
    }, 1000);
  }

  function endSession() {
    if (sessionInterval) {
      clearInterval(sessionInterval);
    }
    sessionActive = false;
    
    // Add to history
    const newSession = {
      id: sessionHistory.length + 1,
      date: new Date().toISOString().split('T')[0],
      topic: currentTopic,
      duration: sessionDuration,
      retention: Math.floor(Math.random() * 20) + 75,
      anxiety: Math.floor(Math.random() * 5) + 1
    };
    sessionHistory = [newSession, ...sessionHistory];
  }

  function pauseSession() {
    if (sessionInterval) {
      clearInterval(sessionInterval);
    }
    sessionActive = false;
  }

  function getRetentionColor(value: number) {
    if (value >= 90) return 'var(--success)';
    if (value >= 75) return '#FFB800';
    return 'var(--danger)';
  }

  function getLoadClass(value: number) {
    if (value <= 2) return 'low';
    if (value <= 3) return 'medium';
    return 'high';
  }

  function formatDate(isoDate: string) {
    return new Date(isoDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }

  function formatTime(seconds: number) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  $: progressPercent = (elapsedTime / (sessionDuration * 60)) * 100;
</script>

<svelte:head>
  <title>Study Session - Study Vault</title>
</svelte:head>

{#if loading}
<div class="loading-screen">
  <div class="loading-container">
    <div class="loading-logo">
      <div class="logo-inner">📚</div>
    </div>
    <div class="loading-text">Preparing Study Session</div>
    <div class="loading-progress">
      <div class="progress-bar">
        <div class="progress-fill"></div>
      </div>
    </div>
  </div>
</div>
{/if}

<div class="study-page">
  <div class="page-container">
    <!-- Header -->
    <header class="page-header">
      <div class="header-left">
        <h1 class="page-title">Study Session</h1>
        <p class="page-subtitle">Optimized learning with cognitive tracking{demo ? ' (Demo Mode)' : ''}</p>
      </div>
      <div class="header-actions">
        <a href="/dashboard" class="btn-ghost">Dashboard</a>
        <a href="/deep-work" class="btn-accent">Deep Work Mode</a>
      </div>
    </header>

    <!-- Main Content -->
    <main class="page-main">
      <div class="main-grid">
        <!-- Session Setup Panel -->
        <div class="panel">
          <div class="panel-header">
            <h2 class="panel-title">Session Setup</h2>
            <div class="section-badge">READY</div>
          </div>
          
          <!-- Topic Selection -->
          <div class="field-group">
            <label class="field-label">Study Topic</label>
            <select bind:value={currentTopic} class="field-select">
              {#each availableTopics as topic}
                <option value={topic}>{topic}</option>
              {/each}
            </select>
          </div>

          <!-- Session Type -->
          <div class="field-group">
            <label class="field-label">Session Type</label>
            <div class="session-types">
              <button 
                class="session-type-option" 
                class:selected={sessionType === 'focused'}
                on:click={() => sessionType = 'focused'}
              >
                <div class="session-type-icon">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <circle cx="12" cy="12" r="6"/>
                    <circle cx="12" cy="12" r="2"/>
                  </svg>
                </div>
                <div class="session-type-content">
                  <div class="session-type-label">Focused Study</div>
                  <div class="session-type-desc">Deep concentration on complex topics</div>
                </div>
              </button>
              
              <button 
                class="session-type-option" 
                class:selected={sessionType === 'review'}
                on:click={() => sessionType = 'review'}
              >
                <div class="session-type-icon">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/>
                    <path d="M21 3v5h-5"/>
                    <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>
                    <path d="M8 16H3v5"/>
                  </svg>
                </div>
                <div class="session-type-content">
                  <div class="session-type-label">Review & Reinforce</div>
                  <div class="session-type-desc">Consolidate previous learning</div>
                </div>
              </button>
              
              <button 
                class="session-type-option" 
                class:selected={sessionType === 'practice'}
                on:click={() => sessionType = 'practice'}
              >
                <div class="session-type-icon">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14.4 14.4 9.6 9.6"/>
                    <path d="M18.657 21.485a2 2 0 1 1-2.829-2.828l-1.767 1.768a2 2 0 1 1-2.829-2.829l6.364-6.364a2 2 0 1 1 2.829 2.829l-1.768 1.767a2 2 0 1 1 2.828 2.828z"/>
                    <path d="m21.5 21.5-1.4-1.4"/>
                    <path d="M3.9 3.9 2.5 2.5"/>
                    <path d="M6.404 12.768a2 2 0 1 1-2.829-2.829l1.768-1.767a2 2 0 1 1-2.828-2.829l2.828-2.828a2 2 0 1 1 2.829 2.829l1.767-1.768 a2 2 0 1 1 2.829 2.829z"/>
                  </svg>
                </div>
                <div class="session-type-content">
                  <div class="session-type-label">Practice Problems</div>
                  <div class="session-type-desc">Apply knowledge through exercises</div>
                </div>
              </button>
            </div>
          </div>

          <!-- Duration -->
          <div class="field-group">
            <label class="field-label">Duration (minutes)</label>
            <input type="range" min="15" max="120" step="15" bind:value={sessionDuration} class="field-range" />
            <div class="duration-display">{sessionDuration} min</div>
          </div>

          <!-- Start Button -->
          <div class="session-controls">
            {#if !sessionActive}
              <button class="btn-start" on:click={startSession}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="6 3 20 12 6 21 6 3"/>
                </svg>
                Start Session
              </button>
            {:else}
              <button class="btn-start" on:click={pauseSession}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="6" y="4" width="4" height="16"/>
                  <rect x="14" y="4" width="4" height="16"/>
                </svg>
                Pause Session
              </button>
            {/if}
          </div>
        </div>

        <!-- Recent Sessions Panel -->
        <div class="panel">
          <div class="panel-header">
            <h2 class="panel-title">Recent Sessions</h2>
            <div class="section-badge">{sessionHistory.length} SESSIONS</div>
          </div>
          
          <div class="session-list">
            {#each sessionHistory as session}
              <div class="session-row">
                <div class="session-main">
                  <div class="session-topic">{session.topic}</div>
                  <div class="session-date">{formatDate(session.date)}</div>
                </div>
                <div class="session-meta">
                  <div class="session-duration">{session.duration} min</div>
                  <div class="retention-pill">
                    <div class="retention-bar">
                      <div class="retention-bar-fill" style="width: {session.retention}%"></div>
                    </div>
                    <span>{session.retention}%</span>
                  </div>
                  <div class="load-indicator">
                    <div class="load-dot {getLoadClass(session.anxiety)}"></div>
                    <span>Load {session.anxiety}</span>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>

      <!-- AI Study Tips -->
      <div class="panel tips-panel">
        <div class="panel-header">
          <h2 class="panel-title">AI Study Tips</h2>
          <div class="section-badge">PERSONALIZED</div>
        </div>
        
        <div class="tips-list">
          <div class="tip-row">
            <div class="tip-icon-wrap">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="4"/>
                <path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/>
              </svg>
            </div>
            <div class="tip-content">
              <div class="tip-title">Optimal Timing</div>
              <div class="tip-body">Your retention is highest between 2-4 PM based on historical data</div>
            </div>
          </div>
          
          <div class="tip-row">
            <div class="tip-icon-wrap">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>
              </svg>
            </div>
            <div class="tip-content">
              <div class="tip-title">Cognitive Load</div>
              <div class="tip-body">Take a 5-min break every 25 minutes to maintain optimal performance</div>
            </div>
          </div>
          
          <div class="tip-row">
            <div class="tip-icon-wrap">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" x2="12" y1="20" y2="10"/>
                <line x1="18" x2="18" y1="20" y2="4"/>
                <line x1="6" x2="6" y1="20" y2="16"/>
              </svg>
            </div>
            <div class="tip-content">
              <div class="tip-title">Topic Mastery</div>
              <div class="tip-body">Focus on Data Structures - you're at 78% mastery level</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</div>

<style>
  /* Design Tokens */
  :root {
    --bg:              #0A0A0B;
    --surface:         #111114;
    --surface-hover:   #16161A;
    --border:          rgba(255, 255, 255, 0.08);
    --border-focus:    rgba(200, 255, 0, 0.5);
    --accent:          #C8FF00;
    --accent-dim:      rgba(200, 255, 0, 0.08);
    --accent-glow:     rgba(200, 255, 0, 0.2);
    --violet:          #7C5CFC;
    --danger:          #FF4545;
    --success:         #00FF94;
    --text-primary:    #F2F2F2;
    --text-muted:      #555560;
    --text-placeholder:rgba(255, 255, 255, 0.2);
    --radius-card:     12px;
    --radius-input:    10px;
    --radius-btn:      10px;
    --font-sans:       'Inter', sans-serif;
    --font-mono:       'JetBrains Mono', monospace;
  }

  /* Page Background */
  .study-page {
    background: #0A0A0B;
    background-image: radial-gradient(
      ellipse at 70% 10%, 
      rgba(124,92,252,0.05) 0%, 
      transparent 60%
    );
    min-height: 100vh;
  }

  .page-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 24px;
  }

  /* Header */
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 32px 0;
    border-bottom: 1px solid var(--border);
    padding-bottom: 24px;
    margin-bottom: 32px;
  }

  .page-title {
    font-family: var(--font-sans);
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    margin: 0;
  }

  .page-subtitle {
    font-family: var(--font-sans);
    font-size: 13px;
    color: var(--text-muted);
    margin: 4px 0 0 0;
  }

  .header-actions {
    display: flex;
    gap: 12px;
  }

  .btn-ghost {
    height: 40px;
    padding: 0 20px;
    background: transparent;
    border: 1px solid var(--border);
    border-radius: var(--radius-btn);
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: border-color 0.2s, color 0.2s;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .btn-ghost:hover {
    border-color: rgba(255,255,255,0.18);
    color: var(--text-primary);
  }

  .btn-accent {
    height: 40px;
    padding: 0 20px;
    background: var(--accent);
    border: none;
    border-radius: var(--radius-btn);
    color: #0A0A0B;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: box-shadow 0.2s, transform 0.15s;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .btn-accent:hover {
    box-shadow: 0 0 24px var(--accent-glow);
    transform: translateY(-1px);
  }

  /* Main Layout */
  .page-main {
    margin-bottom: 48px;
  }

  .main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }

  /* Panels */
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-card);
    padding: 28px;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }

  .panel-title {
    font-family: var(--font-sans);
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
  }

  .section-badge {
    font-family: var(--font-mono);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 9999px;
    border: 1px solid rgba(200, 255, 0, 0.3);
    background: rgba(200, 255, 0, 0.06);
    color: var(--accent);
  }

  /* Form Fields */
  .field-group {
    margin-bottom: 24px;
  }

  .field-label {
    font-size: 12px;
    font-weight: 500;
    color: var(--text-muted);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 8px;
    display: block;
  }

  .field-select {
    width: 100%;
    height: 48px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius-input);
    padding: 0 16px;
    color: var(--text-primary);
    font-size: 14px;
    font-family: var(--font-sans);
    appearance: none;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23555560' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 16px center;
    padding-right: 44px;
    outline: none;
  }

  .field-select:focus {
    border-color: var(--border-focus);
    box-shadow: 0 0 0 3px rgba(200,255,0,0.08);
  }

  /* Session Types */
  .session-types {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .session-type-option {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    border-radius: var(--radius-input);
    border: 1px solid var(--border);
    background: transparent;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    margin-bottom: 8px;
  }

  .session-type-option:hover {
    background: rgba(255,255,255,0.02);
    border-color: rgba(255,255,255,0.14);
  }

  .session-type-option.selected {
    border-color: rgba(200, 255, 0, 0.4);
    background: rgba(200, 255, 0, 0.04);
  }

  .session-type-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    flex-shrink: 0;
  }

  .session-type-option.selected .session-type-icon {
    background: var(--accent-dim);
    border-color: rgba(200,255,0,0.3);
    color: var(--accent);
  }

  .session-type-content {
    flex: 1;
  }

  .session-type-label {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }

  .session-type-desc {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 2px;
  }

  .session-type-option.selected .session-type-label {
    color: var(--accent);
  }

  /* Duration Slider */
  .field-range {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 4px;
    background: rgba(255,255,255,0.08);
    border-radius: 9999px;
    outline: none;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
    background: linear-gradient(
      to right,
      var(--accent) 0%,
      var(--accent) var(--val, 45%),
      rgba(255,255,255,0.08) var(--val, 45%),
      rgba(255,255,255,0.08) 100%
    );
  }

  .field-range::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--accent);
    border: 3px solid #0A0A0B;
    box-shadow: 0 0 0 1px var(--accent), 0 0 12px var(--accent-glow);
    cursor: pointer;
    transition: box-shadow 0.2s;
  }

  .field-range::-webkit-slider-thumb:hover {
    box-shadow: 0 0 0 1px var(--accent), 0 0 20px var(--accent-glow);
  }

  .duration-display {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 600;
    color: var(--accent);
    text-align: center;
    margin-top: 10px;
    letter-spacing: 0.02em;
  }

  /* Start Button */
  .session-controls {
    margin-top: 24px;
  }

  .btn-start {
    width: 100%;
    height: 52px;
    background: var(--accent);
    color: #0A0A0B;
    border: none;
    border-radius: var(--radius-btn);
    font-size: 14px;
    font-weight: 700;
    letter-spacing: -0.01em;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.25s, transform 0.15s;
  }

  .btn-start::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg,
      rgba(255,255,255,0.15) 0%,
      rgba(255,255,255,0) 60%);
    pointer-events: none;
  }

  .btn-start:hover {
    box-shadow: 0 0 30px var(--accent-glow), 0 8px 24px rgba(0,0,0,0.3);
    align-items: center;
    justify-content: center;
    color: var(--violet);
    flex-shrink: 0;
  }

  .tip-content {
    flex: 1;
  }

  .tip-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
  }

  .tip-body {
    font-size: 13px;
    color: var(--text-muted);
    line-height: 1.6;
    margin-top: 3px;
  }

  /* Loading Screen */
  .loading-screen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--bg);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .loading-container {
    text-align: center;
  }

  .loading-logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 24px;
    position: relative;
  }

  .logo-inner {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--accent), var(--violet));
    border-radius: var(--radius-card);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--bg);
    font-size: 32px;
    font-weight: 800;
    animation: logoPulse 2s ease-in-out infinite;
  }

  @keyframes logoPulse {
    0%, 100% {
      transform: scale(1);
      box-shadow: 0 0 40px var(--accent-glow);
    }
    50% {
      transform: scale(1.05);
      box-shadow: 0 0 60px var(--accent-glow);
    }
  }

  .loading-text {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 32px;
    background: linear-gradient(135deg, var(--accent), var(--violet));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .loading-progress {
    width: 200px;
    margin: 0 auto;
  }

  .loading-progress .progress-bar {
    height: 2px;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 9999px;
    overflow: hidden;
  }

  .loading-progress .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--violet));
    border-radius: 9999px;
    animation: progressShrink 1s ease-in-out;
  }

  @keyframes progressShrink {
    0% {
      width: 100%;
      opacity: 1;
    }
    100% {
      width: 0%;
      opacity: 0;
    }
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .page-container {
      padding: 0 16px;
    }
    
    .main-grid {
      grid-template-columns: 1fr;
      gap: 16px;
    }
    
    .page-header {
      flex-direction: column;
      gap: 16px;
      align-items: stretch;
    }
    
    .header-actions {
      justify-content: stretch;
    }
    
    .btn-ghost,
    .btn-accent {
      flex: 1;
    }
  }
</style>
