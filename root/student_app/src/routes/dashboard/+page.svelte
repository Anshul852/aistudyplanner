<script>
  import AIAdvisor from "$lib/components/dashboard/AIAdvisor.svelte";
  import AISettings from "$lib/components/dashboard/AISettings.svelte";
  import AnxietyHeatmap from "$lib/components/dashboard/AnxietyHeatmap.svelte";
  import DayView from "$lib/components/dashboard/DayView.svelte";
  import EnrollmentCard from "$lib/components/dashboard/EnrollmentCard.svelte";
  import EnrollmentModal from "$lib/components/dashboard/EnrollmentModal.svelte";
  import FocusTimer from "$lib/components/dashboard/FocusTimer.svelte";
  import SessionSummary from "$lib/components/dashboard/SessionSummary.svelte";
  import StreakCounter from "$lib/components/dashboard/StreakCounter.svelte";
  import StyleEditor from "$lib/components/dashboard/StyleEditor.svelte";
  import Syllabus from "$lib/components/dashboard/Syllabus.svelte";
  import SyllabusTimeline from "$lib/components/dashboard/SyllabusTimeline.svelte";
  import SyncStatus from "$lib/components/dashboard/SyncStatus.svelte";
  import ThemeCustomizer from "$lib/components/dashboard/ThemeCustomizer.svelte";
</script>

<div class="grid">
  <AIAdvisor />
  <AISettings />
  <AnxietyHeatmap />
  <DayView />
  <EnrollmentCard />
  <EnrollmentModal />
  <FocusTimer />
  <SessionSummary />
  <StreakCounter />
  <StyleEditor />
  <Syllabus />
  <SyllabusTimeline />
  <SyncStatus />
  <ThemeCustomizer />
</div>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.8rem;
  }
</style>
