<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';

  onMount(() => {
    // Redirect to dashboard
    goto('/dashboard');
  });
</script>

<svelte:head>
  <title>StudyVault - AI-Powered Study Assistant</title>
</svelte:head>

<div class="min-h-screen bg-bg-primary flex items-center justify-center">
  <div class="text-center">
    <div class="w-8 h-8 rounded-lg bg-lime-500 flex items-center justify-center mx-auto mb-4">
      <div class="w-4 h-4 bg-black rounded-sm"></div>
    </div>
    <h1 class="text-white text-xl font-semibold mb-2">StudyVault</h1>
    <p class="text-gray-400 text-sm">Redirecting to dashboard...</p>
  </div>
</div>
