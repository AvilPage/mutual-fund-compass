<script>
  import { page } from '$app/stores';

  // The whole row is available here
  $: record = $page.state;
</script>

<h1>Details Page</h1>

{#if record}
  <pre>{JSON.stringify(record, null, 2)}</pre>
{:else}
  <p>No record passed</p>
{/if}
