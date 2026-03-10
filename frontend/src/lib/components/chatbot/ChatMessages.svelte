<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Copy, ThumbsUp, ThumbsDown, RefreshCw, Edit3 } from 'lucide-svelte';
  import type { Message } from '$lib/stores/chatStore';

  export let messages: Message[] = [];

  const dispatch = createEventDispatcher();

  // Handle message actions
  function handleCopy(content: string) {
    navigator.clipboard.writeText(content);
  }

  function handleThumbsUp(messageId: string) {
    dispatch('feedback', { messageId, type: 'positive' });
  }

  function handleThumbsDown(messageId: string) {
    dispatch('feedback', { messageId, type: 'negative' });
  }

  function handleRegenerate(messageId: string) {
    dispatch('regenerate', { messageId });
  }

  function handleEdit(messageId: string, content: string) {
    dispatch('edit', { messageId, content });
  }

  // Format timestamp
  function formatTimestamp(timestamp: number): string {
    const now = Date.now();
    const diff = now - timestamp;
    
    if (diff < 60000) return 'just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    if (diff < 604800000) return `${Math.floor(diff / 86400000)}d ago`;
    
    return new Date(timestamp).toLocaleDateString();
  }

  // Render markdown-like content (basic implementation)
  function renderContent(content: string): string {
    // Basic markdown rendering
    return content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="inline-code">$1</code>')
      .replace(/\n/g, '<br>');
  }

  // Check if message is streaming
  $: isStreaming = messages.some(m => m.isStreaming);
</script>

<div class="messages-list">
  {#each messages as message (message.id)}
    <div class="message" class:bot={message.role === 'assistant'} class:user={message.role === 'user'}>
      {#if message.role === 'assistant'}
        <div class="message-avatar">
          {message.metadata?.connectorId === 'gemini' ? '✦' : 
           message.metadata?.connectorId === 'chatgpt' ? '🤖' :
           message.metadata?.connectorId === 'claude' ? '◆' : '🧠'}
        </div>
        <div class="message-content">
          <div class="message-text" class:streaming={message.isStreaming}>
            {@html renderContent(message.content)}
            {#if message.isStreaming}
              <span class="streaming-cursor">|</span>
            {/if}
          </div>
          <div class="message-timestamp">
            {formatTimestamp(message.timestamp)}
          </div>
          <div class="message-actions">
            <button 
              class="message-action-btn" 
              on:click={() => handleCopy(message.content)}
              title="Copy"
            >
              <Copy size={14} />
            </button>
            <button 
              class="message-action-btn" 
              on:click={() => handleThumbsUp(message.id)}
              title="Good response"
            >
              <ThumbsUp size={14} />
            </button>
            <button 
              class="message-action-btn" 
              on:click={() => handleThumbsDown(message.id)}
              title="Bad response"
            >
              <ThumbsDown size={14} />
            </button>
            {#if message.role === 'assistant'}
              <button 
                class="message-action-btn" 
                on:click={() => handleRegenerate(message.id)}
                title="Regenerate"
              >
                <RefreshCw size={14} />
              </button>
            {/if}
          </div>
        </div>
      {:else}
        <!-- User Message -->
        <div class="message-content">
          <div class="message-text">
            {message.content}
          </div>
          <div class="message-timestamp">
            {formatTimestamp(message.timestamp)}
          </div>
          <div class="message-actions">
            <button 
              class="message-action-btn" 
              on:click={() => handleCopy(message.content)}
              title="Copy"
            >
              <Copy size={14} />
            </button>
            <button 
              class="message-action-btn" 
              on:click={() => handleEdit(message.id, message.content)}
              title="Edit"
            >
              <Edit3 size={14} />
            </button>
          </div>
        </div>
      {/if}
    </div>
  {/each}
</div>

<style>
  .messages-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .message {
    animation: fadeIn 200ms ease-out;
  }

  .message.bot {
    display: flex;
    gap: 12px;
  }

  .message.user {
    display: flex;
    justify-content: flex-end;
  }

  .message-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: var(--bg-primary);
    flex-shrink: 0;
    margin-top: 4px;
  }

  .message-content {
    max-width: 80%;
    position: relative;
  }

  .message.bot .message-content {
    background: transparent;
  }

  .message.user .message-content {
    background: var(--user-bubble);
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg);
    padding: 12px 16px;
  }

  .message-text {
    font-size: 15px;
    line-height: 1.75;
    color: var(--text-primary);
    word-wrap: break-word;
  }

  .message-text.streaming {
    position: relative;
  }

  .streaming-cursor {
    color: var(--accent);
    animation: blink 500ms infinite;
    margin-left: 2px;
  }

  @keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
  }

  .message-text :global(.inline-code) {
    background: var(--bg-elevated);
    border: 1px solid var(--border-default);
    border-radius: var(--radius-sm);
    padding: 2px 6px;
    font-family: var(--font-mono);
    font-size: 14px;
    color: var(--accent);
  }

  .message-text :global(strong) {
    font-weight: 600;
    color: var(--text-primary);
  }

  .message-text :global(em) {
    font-style: italic;
    color: var(--text-secondary);
  }

  .message-timestamp {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 8px;
    opacity: 0;
    transition: opacity 150ms ease;
  }

  .message:hover .message-timestamp {
    opacity: 1;
  }

  .message-actions {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 8px;
    opacity: 0;
    transition: opacity 150ms ease;
  }

  .message:hover .message-actions {
    opacity: 1;
  }

  .message-action-btn {
    width: 28px;
    height: 28px;
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 150ms ease;
  }

  .message-action-btn:hover {
    background: var(--bg-elevated);
    color: var(--text-primary);
  }

  @media (max-width: 640px) {
    .message.user .message-content {
      max-width: 90%;
    }

    .message-actions {
      gap: 2px;
    }

    .message-action-btn {
      width: 24px;
      height: 24px;
    }
  }
</style>
