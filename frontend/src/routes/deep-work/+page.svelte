<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import { user } from "$lib/stores/auth";
    import { Brain, Play, Pause, Square, Bell, Globe, Mail, Music, Clock, TrendingUp, Target, Zap } from "lucide-svelte";

    // ── State ──────────────────────────────────────────────
    let mounted        = false;
    let loading        = true;
    let sessionActive  = false;
    let isPaused       = false;
    let elapsed        = 0;
    let distractionsBlocked = 0;
    let timer: ReturnType<typeof setInterval>;
    let distractTimer: ReturnType<typeof setInterval>;

    // ── Setup ──────────────────────────────────────────────
    let sessionDuration = 90;
    let currentProject  = "Research Paper on ML Algorithms";

    const projects = [
        "Research Paper on ML Algorithms",
        "Thesis Literature Review",
        "Algorithm Implementation",
        "Data Analysis Project",
        "Code Refactoring",
        "System Architecture Design",
    ];

    // ── Toggles ────────────────────────────────────────────
    let blockNotifications = true;
    let blockSocial        = true;
    let blockEmail         = true;
    let enableMusic        = false;

    // ── History ────────────────────────────────────────────
    interface DeepSession {
        id: number; date: string; project: string;
        duration: number; intensity: number; fatigue: number;
    }

    let history: DeepSession[] = [
        { id:1, date:"2026-02-24", project:"Algorithm Implementation", duration:90,  intensity:88, fatigue:4 },
        { id:2, date:"2026-02-23", project:"Research Paper",           duration:120, intensity:92, fatigue:5 },
        { id:3, date:"2026-02-22", project:"Data Analysis",            duration:75,  intensity:78, fatigue:3 },
        { id:4, date:"2026-02-21", project:"Code Refactoring",         duration:60,  intensity:85, fatigue:2 },
        { id:5, date:"2026-02-20", project:"System Design",            duration:105, intensity:90, fatigue:4 },
    ];

    // ── Computed ───────────────────────────────────────────
    $: progress     = Math.min((elapsed / (sessionDuration * 60)) * 100, 100);
    $: remaining    = Math.max(sessionDuration * 60 - elapsed, 0);
    $: remainingFmt = formatTime(remaining);
    $: elapsedFmt   = formatTime(elapsed);

    // SVG ring math
    const R = 54; const C = 2 * Math.PI * R;
    $: ringFill = `${(progress / 100) * C} ${C}`;

    // ── Helpers ────────────────────────────────────────────
    function formatTime(s: number): string {
        const h   = Math.floor(s / 3600);
        const m   = Math.floor((s % 3600) / 60);
        const sec = s % 60;
        if (h > 0) return `${h}:${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
        return `${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
    }

    function formatDate(iso: string): string {
        return new Date(iso).toLocaleDateString("en-US", { month:"short", day:"numeric" });
    }

    function intensityColor(v: number): string {
        if (v >= 90) return "#a3e635";
        if (v >= 75) return "#f59e0b";
        return "#f87171";
    }

    function fatigueColor(v: number): string {
        if (v <= 2) return "#34d399";
        if (v <= 4) return "#f59e0b";
        return "#f87171";
    }

    // ── Controls ───────────────────────────────────────────
    function startSession() {
        sessionActive = true; isPaused = false;
        elapsed = 0; distractionsBlocked = 0;
        timer = setInterval(() => {
            elapsed++;
            if (elapsed >= sessionDuration * 60) endSession();
        }, 1000);
        distractTimer = setInterval(() => {
            if (Math.random() < 0.012) distractionsBlocked++;
        }, 1000);
    }

    function pauseSession() {
        isPaused = !isPaused;
        if (isPaused) { clearInterval(timer); clearInterval(distractTimer); }
        else {
            timer         = setInterval(() => { elapsed++; }, 1000);
            distractTimer = setInterval(() => { if (Math.random() < 0.012) distractionsBlocked++; }, 1000);
        }
    }

    function endSession() {
        clearInterval(timer); clearInterval(distractTimer);
        history = [{
            id:        history.length + 1,
            date:      new Date().toISOString().split("T")[0],
            project:   currentProject,
            duration:  sessionDuration,
            intensity: Math.floor(Math.random() * 20) + 75,
            fatigue:   Math.floor(Math.random() * 5)  + 1,
        }, ...history];
        sessionActive = false; isPaused = false; elapsed = 0;
    }

    // ── Tips ───────────────────────────────────────────────
    const tips = [
        { icon: TrendingUp, title: "Peak Focus Time",      body: "Your deep work sessions are most productive between 9–11 AM." },
        { icon: Target,     title: "Optimal Duration",     body: "90-minute sessions show 23% higher completion rates for you." },
        { icon: Globe,      title: "Distraction Patterns", body: "Social media distractions peak at 3 PM — schedule breaks accordingly." },
        { icon: Music,      title: "Focus Music",          body: "Lo-fi beats increase your focus duration by ~15%." },
    ];

    onMount(() => { setTimeout(() => { loading = false; mounted = true; }, 900); });
    onDestroy(() => { clearInterval(timer); clearInterval(distractTimer); });
</script>

<svelte:head><title>Deep Work — StudyVault</title></svelte:head>

<!-- ── Loading overlay ── -->
{#if loading}
    <div class="loading-overlay">
        <div class="loading-inner">
            <div class="loading-icon"><Brain size={28} strokeWidth={1.5} /></div>
            <p class="loading-text">Entering Deep Work Mode</p>
            <div class="loading-bar"><div class="loading-fill" /></div>
        </div>
    </div>
{/if}

<div class="page" class:mounted>

    <!-- ── Header ── -->
    <header class="page-header">
        <div class="header-left">
            <div class="header-icon"><Brain size={14} strokeWidth={2} /></div>
            <div>
                <h1 class="page-title">Deep Work</h1>
                <p class="page-sub">Distraction-free focused work sessions</p>
            </div>
        </div>
        <div class="header-actions">
            <a href="/dashboard" class="ghost-btn">Dashboard</a>
            <a href="/sessions" class="accent-btn">Study Sessions</a>
        </div>
    </header>

    <div class="divider" />

    <!-- ── Main grid ── -->
    <div class="main-grid">

        <!-- LEFT: Timer + Setup -->
        <div class="left-col">

            <!-- Timer card -->
            <div class="timer-card" class:active={sessionActive && !isPaused}>
                <div class="ring-wrap">
                    <svg viewBox="0 0 140 140" class="ring-svg">
                        <circle cx="70" cy="70" r={R} fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="8" />
                        <circle
                            cx="70" cy="70" r={R}
                            fill="none"
                            stroke={sessionActive ? "#a3e635" : "rgba(255,255,255,0.1)"}
                            stroke-width="8"
                            stroke-linecap="round"
                            stroke-dasharray={ringFill}
                            transform="rotate(-90 70 70)"
                            style="transition:stroke-dasharray 1s linear,stroke 300ms ease;filter:drop-shadow(0 0 7px rgba(163,230,53,0.55))"
                        />
                    </svg>
                    <div class="ring-center">
                        <span class="ring-time">{sessionActive ? remainingFmt : formatTime(sessionDuration * 60)}</span>
                        <span class="ring-sub">{sessionActive ? (isPaused ? "paused" : "remaining") : `${sessionDuration} min`}</span>
                    </div>
                </div>

                <!-- Status row -->
                <div class="status-row">
                    <div class="status-item">
                        <span class="status-val" style="color:{sessionActive ? '#a3e635' : 'rgba(255,255,255,0.25)'}">{elapsedFmt}</span>
                        <span class="status-key">elapsed</span>
                    </div>
                    <div class="status-div" />
                    <div class="status-item">
                        <span class="status-val" style="color:{sessionActive ? '#38bdf8' : 'rgba(255,255,255,0.25)'}">{distractionsBlocked}</span>
                        <span class="status-key">blocked</span>
                    </div>
                    <div class="status-div" />
                    <div class="status-item">
                        <span class="status-val" style="color:{sessionActive && !isPaused ? '#a3e635' : 'rgba(255,255,255,0.25)'}">
                            {sessionActive ? (isPaused ? "PAUSED" : "LIVE") : "IDLE"}
                        </span>
                        <span class="status-key">state</span>
                    </div>
                </div>

                {#if sessionActive && !isPaused}<div class="card-glow" />{/if}
            </div>

            <!-- Setup card -->
            <div class="setup-card">

                <div class="field">
                    <label class="field-label">Project</label>
                    <select bind:value={currentProject} class="field-select">
                        {#each projects as p}<option value={p}>{p}</option>{/each}
                    </select>
                </div>

                <div class="field">
                    <label class="field-label">Duration</label>
                    <div class="dur-tabs">
                        {#each [60, 90, 120] as d}
                            <button class="dur-tab" class:active={sessionDuration === d} on:click={() => sessionDuration = d}>{d} min</button>
                        {/each}
                    </div>
                </div>

                <div class="field">
                    <label class="field-label">Focus Settings</label>
                    <div class="toggles">
                        {#each [
                            { Icon: Bell,  label: "Block Notifications", key: "blockNotifications", val: blockNotifications },
                            { Icon: Globe, label: "Block Social Media",  key: "blockSocial",        val: blockSocial        },
                            { Icon: Mail,  label: "Block Email",         key: "blockEmail",         val: blockEmail         },
                            { Icon: Music, label: "Enable Focus Music",  key: "enableMusic",        val: enableMusic        },
                        ] as t}
                            <div class="toggle-row" on:click={() => {
                                if      (t.key === "blockNotifications") blockNotifications = !blockNotifications;
                                else if (t.key === "blockSocial")        blockSocial = !blockSocial;
                                else if (t.key === "blockEmail")         blockEmail = !blockEmail;
                                else                                      enableMusic = !enableMusic;
                            }}>
                                <div class="toggle-left">
                                    <div class="t-icon" class:on={t.val}>
                                        <svelte:component this={t.Icon} size={12} strokeWidth={2} />
                                    </div>
                                    <span class="t-label">{t.label}</span>
                                </div>
                                <div class="switch" class:on={t.val}><div class="switch-thumb" /></div>
                            </div>
                        {/each}
                    </div>
                </div>

                <div class="controls">
                    {#if !sessionActive}
                        <button class="start-btn" on:click={startSession}>
                            <Play size={14} strokeWidth={2.5} /> Start Deep Work
                        </button>
                    {:else}
                        <button class="secondary-btn" on:click={pauseSession}>
                            {#if isPaused}<Play size={14} strokeWidth={2.5} />Resume
                            {:else}<Pause size={14} strokeWidth={2.5} />Pause{/if}
                        </button>
                        <button class="danger-btn" on:click={endSession}>
                            <Square size={13} strokeWidth={2.5} />End
                        </button>
                    {/if}
                </div>
            </div>
        </div>

        <!-- RIGHT: History + Tips -->
        <div class="right-col">

            <div class="card">
                <div class="card-head">
                    <div class="section-header">
                        <span class="section-dot" />
                        <h2 class="section-title">Deep Work History</h2>
                    </div>
                    <span class="count-chip">{history.length} sessions</span>
                </div>

                <div class="history-list">
                    {#each history as s, i}
                        <div class="history-row" style="animation-delay:{i*55}ms">
                            <div class="h-info">
                                <p class="h-project">{s.project}</p>
                                <p class="h-meta"><Clock size={9} strokeWidth={2} />{formatDate(s.date)} · {s.duration} min</p>
                            </div>
                            <div class="h-stats">
                                <div class="h-stat">
                                    <span class="h-val" style="color:{intensityColor(s.intensity)}">{s.intensity}%</span>
                                    <div class="mini-bar"><div class="mini-fill" style="width:{s.intensity}%;background:{intensityColor(s.intensity)}" /></div>
                                    <span class="h-key">intensity</span>
                                </div>
                                <div class="fatigue-chip" style="color:{fatigueColor(s.fatigue)};background:{fatigueColor(s.fatigue)}18">
                                    Fatigue {s.fatigue}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            <div class="card">
                <div class="card-head">
                    <div class="section-header">
                        <span class="section-dot" />
                        <h2 class="section-title">AI Insights</h2>
                    </div>
                    <span class="ai-chip">optimized</span>
                </div>

                <div class="tips-list">
                    {#each tips as t, i}
                        <div class="tip-row" style="animation-delay:{i*60}ms">
                            <div class="tip-icon"><svelte:component this={t.icon} size={13} strokeWidth={1.8} /></div>
                            <div>
                                <p class="tip-title">{t.title}</p>
                                <p class="tip-body">{t.body}</p>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Geist:wght@400;500;600;700&display=swap");

    /* Loading */
    .loading-overlay {
        position: fixed; inset: 0; z-index: 9999;
        background: #0a0a0b;
        display: flex; align-items: center; justify-content: center;
        animation: fade-out 300ms ease 850ms forwards;
    }
    .loading-inner { display: flex; flex-direction: column; align-items: center; gap: 16px; }
    .loading-icon {
        width: 64px; height: 64px; border-radius: 16px;
        background: rgba(163,230,53,0.1); border: 1px solid rgba(163,230,53,0.2);
        color: #a3e635;
        display: flex; align-items: center; justify-content: center;
        animation: icon-pulse 1.5s ease-in-out infinite;
    }
    .loading-text {
        font-family: "Geist", system-ui, sans-serif;
        font-size: 14px; font-weight: 600;
        color: rgba(255,255,255,0.4); margin: 0;
    }
    .loading-bar { width: 160px; height: 2px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
    .loading-fill {
        height: 100%;
        background: linear-gradient(90deg, #a3e635, #38bdf8);
        border-radius: 2px;
        animation: bar-shrink 900ms ease-in-out forwards;
    }

    /* Page */
    .page {
        font-family: "Geist", system-ui, sans-serif;
        display: flex; flex-direction: column; gap: 20px;
        padding: 28px 32px 48px;
        max-width: 1100px; width: 100%;
        opacity: 0; transform: translateY(6px);
        transition: opacity 300ms ease, transform 300ms ease;
    }
    .page.mounted { opacity: 1; transform: translateY(0); }

    /* Header */
    .page-header { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
    .header-left { display: flex; align-items: center; gap: 12px; }
    .header-icon {
        width: 34px; height: 34px; border-radius: 9px;
        background: rgba(163,230,53,0.1); color: #a3e635;
        display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    }
    .page-title { font-size: 20px; font-weight: 700; color: rgba(255,255,255,0.92); letter-spacing: -0.4px; margin: 0; line-height: 1.1; }
    .page-sub   { font-size: 11px; color: rgba(255,255,255,0.28); margin: 2px 0 0; }
    .header-actions { display: flex; gap: 8px; }

    .ghost-btn {
        padding: 7px 14px; background: transparent;
        border: 1px solid rgba(255,255,255,0.08); border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 500;
        color: rgba(255,255,255,0.4); cursor: pointer; text-decoration: none;
        display: inline-flex; align-items: center;
        transition: border-color 150ms, color 150ms;
    }
    .ghost-btn:hover { border-color: rgba(255,255,255,0.14); color: rgba(255,255,255,0.7); }

    .accent-btn {
        padding: 7px 14px; background: #a3e635; border: none; border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 700;
        color: #000; cursor: pointer; text-decoration: none;
        display: inline-flex; align-items: center;
        transition: filter 150ms;
    }
    .accent-btn:hover { filter: brightness(1.1); }

    .divider { height: 1px; background: rgba(255,255,255,0.05); flex-shrink: 0; }

    /* Grid */
    .main-grid { display: grid; grid-template-columns: 340px 1fr; gap: 16px; align-items: start; }
    .left-col, .right-col { display: flex; flex-direction: column; gap: 16px; }

    /* Timer card */
    .timer-card {
        position: relative; background: #0e0e10;
        border: 1px solid rgba(255,255,255,0.07); border-radius: 14px;
        padding: 28px 20px 22px;
        display: flex; flex-direction: column; align-items: center; gap: 20px;
        overflow: hidden;
        transition: border-color 300ms, box-shadow 300ms;
    }
    .timer-card.active {
        border-color: rgba(163,230,53,0.25);
        box-shadow: 0 0 0 1px rgba(163,230,53,0.1), 0 16px 40px rgba(163,230,53,0.07);
    }

    .ring-wrap { position: relative; width: 140px; height: 140px; }
    .ring-svg  { width: 100%; height: 100%; }
    .ring-center {
        position: absolute; inset: 0;
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;
    }
    .ring-time {
        font-family: "Barlow Condensed", sans-serif;
        font-size: 26px; font-weight: 800; color: #fff;
        letter-spacing: -1px; line-height: 1; font-variant-numeric: tabular-nums;
    }
    .ring-sub { font-size: 9px; color: rgba(255,255,255,0.22); letter-spacing: 0.05em; }

    .status-row {
        display: flex; align-items: center; width: 100%;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.06); border-radius: 9px; overflow: hidden;
    }
    .status-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 10px 8px; }
    .status-val {
        font-family: "Barlow Condensed", sans-serif;
        font-size: 16px; font-weight: 700; letter-spacing: -0.5px; line-height: 1;
    }
    .status-key { font-size: 8px; color: rgba(255,255,255,0.2); letter-spacing: 0.06em; text-transform: uppercase; }
    .status-div { width: 1px; height: 28px; background: rgba(255,255,255,0.06); flex-shrink: 0; }

    .card-glow {
        position: absolute; top: -30px; right: -30px;
        width: 120px; height: 120px; border-radius: 50%;
        background: radial-gradient(circle, rgba(163,230,53,0.15), transparent 70%);
        pointer-events: none;
        animation: glow-pulse 2s ease-in-out infinite;
    }

    /* Setup card */
    .setup-card {
        background: #0e0e10; border: 1px solid rgba(255,255,255,0.07); border-radius: 12px;
        padding: 18px; display: flex; flex-direction: column; gap: 16px;
    }
    .field { display: flex; flex-direction: column; gap: 8px; }
    .field-label { font-size: 9px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(255,255,255,0.25); }

    .field-select {
        width: 100%; height: 38px;
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 8px;
        padding: 0 32px 0 12px; color: rgba(255,255,255,0.8);
        font-family: "Geist", system-ui, sans-serif; font-size: 12px;
        appearance: none; cursor: pointer; outline: none;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='rgba(255,255,255,0.3)' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
        background-repeat: no-repeat; background-position: right 12px center;
        transition: border-color 150ms;
    }
    .field-select:focus { border-color: rgba(163,230,53,0.4); }

    .dur-tabs { display: flex; gap: 6px; }
    .dur-tab {
        flex: 1; height: 36px;
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 7px;
        font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 600;
        color: rgba(255,255,255,0.35); cursor: pointer; transition: all 150ms;
    }
    .dur-tab:hover { color: rgba(255,255,255,0.6); border-color: rgba(255,255,255,0.12); }
    .dur-tab.active { background: rgba(163,230,53,0.1); border-color: rgba(163,230,53,0.35); color: #a3e635; }

    .toggles { display: flex; flex-direction: column; }
    .toggle-row {
        display: flex; align-items: center; justify-content: space-between;
        padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.04); cursor: pointer;
    }
    .toggle-row:last-child { border-bottom: none; }
    .toggle-left { display: flex; align-items: center; gap: 8px; }
    .t-icon {
        width: 22px; height: 22px; border-radius: 5px;
        background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.3);
        display: flex; align-items: center; justify-content: center;
        transition: background 200ms, color 200ms;
    }
    .t-icon.on { background: rgba(163,230,53,0.1); color: #a3e635; }
    .t-label { font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.6); }

    .switch {
        width: 32px; height: 18px; border-radius: 9px;
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08);
        position: relative; transition: background 200ms, border-color 200ms; flex-shrink: 0;
    }
    .switch.on { background: rgba(163,230,53,0.2); border-color: rgba(163,230,53,0.4); }
    .switch-thumb {
        position: absolute; top: 2px; left: 2px;
        width: 12px; height: 12px; border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transition: transform 200ms, background 200ms;
    }
    .switch.on .switch-thumb { transform: translateX(14px); background: #a3e635; }

    .controls { display: flex; gap: 8px; }
    .start-btn {
        flex: 1; height: 44px; display: flex; align-items: center; justify-content: center; gap: 7px;
        background: #a3e635; color: #000; border: none; border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif; font-size: 13px; font-weight: 700; cursor: pointer;
        transition: filter 150ms, transform 150ms;
    }
    .start-btn:hover  { filter: brightness(1.1); }
    .start-btn:active { transform: scale(0.97); }
    .secondary-btn {
        flex: 1; height: 44px; display: flex; align-items: center; justify-content: center; gap: 7px;
        background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.7);
        border: 1px solid rgba(255,255,255,0.1); border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 600; cursor: pointer;
        transition: background 150ms;
    }
    .secondary-btn:hover { background: rgba(255,255,255,0.08); }
    .danger-btn {
        height: 44px; padding: 0 14px; display: flex; align-items: center; gap: 6px;
        background: rgba(248,113,113,0.07); color: #f87171;
        border: 1px solid rgba(248,113,113,0.2); border-radius: 8px;
        font-family: "Geist", system-ui, sans-serif; font-size: 12px; font-weight: 600; cursor: pointer;
        transition: background 150ms;
    }
    .danger-btn:hover { background: rgba(248,113,113,0.12); }

    /* Card */
    .card {
        background: #0e0e10; border: 1px solid rgba(255,255,255,0.07); border-radius: 12px;
        padding: 16px; display: flex; flex-direction: column; gap: 12px;
    }
    .card-head { display: flex; align-items: center; justify-content: space-between; }
    .section-header { display: flex; align-items: center; gap: 7px; }
    .section-dot { width: 5px; height: 5px; border-radius: 50%; background: #a3e635; flex-shrink: 0; }
    .section-title { font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(255,255,255,0.28); margin: 0; }
    .count-chip  { font-size: 9px; color: rgba(255,255,255,0.2); letter-spacing: 0.04em; }
    .ai-chip { font-size: 9px; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: #a3e635; background: rgba(163,230,53,0.07); padding: 2px 7px; border-radius: 4px; }

    /* History */
    .history-list { display: flex; flex-direction: column; gap: 2px; }
    .history-row {
        display: flex; align-items: center; justify-content: space-between; gap: 12px;
        padding: 10px 8px; border-radius: 7px; border: 1px solid transparent;
        opacity: 0; animation: rise 280ms cubic-bezier(0.22,1,0.36,1) forwards;
        transition: background 150ms, border-color 150ms;
    }
    .history-row:hover { background: rgba(255,255,255,0.03); border-color: rgba(255,255,255,0.06); }
    .h-info { display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; }
    .h-project { font-size: 12px; font-weight: 500; color: rgba(255,255,255,0.8); margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .h-meta { display: flex; align-items: center; gap: 4px; font-size: 10px; color: rgba(255,255,255,0.2); margin: 0; }
    .h-stats { display: flex; flex-direction: column; align-items: flex-end; gap: 5px; flex-shrink: 0; }
    .h-stat  { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; }
    .h-val { font-family: "Barlow Condensed", sans-serif; font-size: 17px; font-weight: 700; line-height: 1; }
    .mini-bar { width: 48px; height: 2px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }
    .mini-fill { height: 100%; border-radius: 2px; transition: width 600ms ease; }
    .h-key { font-size: 9px; color: rgba(255,255,255,0.2); }
    .fatigue-chip { font-size: 9px; font-weight: 600; letter-spacing: 0.05em; padding: 2px 6px; border-radius: 4px; }

    /* Tips */
    .tips-list { display: flex; flex-direction: column; gap: 2px; }
    .tip-row {
        display: flex; align-items: flex-start; gap: 10px;
        padding: 10px 8px; border-radius: 7px;
        opacity: 0; animation: rise 280ms cubic-bezier(0.22,1,0.36,1) forwards;
        transition: background 150ms;
    }
    .tip-row:hover { background: rgba(255,255,255,0.02); }
    .tip-icon { width: 28px; height: 28px; border-radius: 7px; background: rgba(163,230,53,0.07); color: #a3e635; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }
    .tip-title { font-size: 12px; font-weight: 600; color: rgba(255,255,255,0.75); margin: 0; }
    .tip-body  { font-size: 11px; color: rgba(255,255,255,0.28); margin: 2px 0 0; line-height: 1.5; }

    /* Keyframes */
    @keyframes rise { from { opacity:0; transform:translateY(5px); } to { opacity:1; transform:translateY(0); } }
    @keyframes glow-pulse { 0%,100% { opacity:.6; transform:scale(1); } 50% { opacity:1; transform:scale(1.15); } }
    @keyframes fade-out { to { opacity:0; pointer-events:none; } }
    @keyframes icon-pulse { 0%,100% { box-shadow:0 0 0 0 rgba(163,230,53,.3); } 50% { box-shadow:0 0 24px 6px rgba(163,230,53,.15); } }
    @keyframes bar-shrink { from { width:100%; } to { width:0%; } }

    @media (max-width: 860px) {
        .main-grid { grid-template-columns: 1fr; }
        .page { padding: 20px 16px 40px; }
    }
</style>