<!-- <script>
  import { page } from '$app/stores';

  $: name = $page.params.name;   // from the URL
  $: record = $page.state;       // from goto()
</script>

<h1>Details for {decodeURIComponent(name)}</h1>

{#if record}
  <ul>
    {#each Object.entries(record) as [key, value]}
      <li><strong>{key}:</strong> {value}</li>
    {/each}
  </ul>
{:else}
  <p>No record data available. (Maybe refreshed the page?)</p>
{/if} -->
<script>
  import { page } from '$app/stores';
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import { goto } from "$app/navigation";
  import Header from '../../Header.svelte';

  

  $: name = $page.params.name;   // from URL
  $: record = $page.state;       // from goto()
  let chartCanvas;
  onMount(async () => {
    const response = await fetch('/nav_history.json'); 
    const record1 = await response.json();
    const matchedRecord = record1.find(r => r.scheme_code === record.scheme_code);
    matchedRecord.nav_history =matchedRecord.nav_history.split("|").map(item => {
      const [date, nav] = item.split(":");
      return { date, nav };
    });
    if (chartCanvas && record) {
      new Chart(chartCanvas, {
        type: 'line',
        data: {
          labels: matchedRecord.nav_history.map(d => d.date).reverse(), // oldest first
          datasets: [{
            label: matchedRecord.scheme_name,
            data: matchedRecord.nav_history.map(d => d.nav).reverse(),
            borderColor: 'blue',
            backgroundColor: 'rgba(0, 0, 255, 0.1)',
            fill: true,
            tension: 0.2
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: false }
          }
        }
      });
    }
  });
  function filterByFundHouse(fund_house) {
    const encoded = encodeURIComponent(fund_house);
    goto(`/?fund_house=${encoded}`);
  }
</script>

<style>
  .container {
    max-width: 900px;
    margin: auto;
    padding: 1rem;
    font-family: sans-serif;
  }
  h1 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
  .cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }
  .card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    padding: 1rem;
    text-align: center;
  }
  .value {
    font-size: 1.25rem;
    font-weight: bold;
    color: #16a34a;
  }
  .label {
    font-size: 0.9rem;
    color: #6b7280;
  }
  canvas {
    width: 100% !important;
    max-height: 400px;
  }
  h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    color: #111827;
  }
  .subheading {
    font-size: 1rem;
    color: #6b7280;
    margin-bottom: 1.5rem;
    cursor: pointer;
  }
</style>

<Header />
<div class="container">
  {#if record}
  <h1>{record.Name}</h1>
    <div class="subheading" on:click={() => filterByFundHouse(record.fund_house)}>
  Fund House: {record.fund_house}
</div>
    <div class="cards">
      <div class="card">
        <div class="value">₹{record.nav}</div>
        <div class="label">Current NAV</div>
      </div>
      <div class="card">
        <div class="value">{record.year_1}%</div>
        <div class="label">CAGR (1 Year)</div>
      </div>  
      <div class="card">
        <div class="value">₹{record.min_amount}</div>
        <div class="label">Min. Investment</div>
      </div>
      <div class="card">
        <div class="value">₹{record.aum} Cr.</div>
        <div class="label">AUM</div>
      </div>
      <div class="card">
        <div class="value">{record.Value}</div>
        <div class="label">Volatility</div>
      </div>
      <div class="card">
        <div class="value">{record.expense_ratio}%</div>
        <div class="label">Expense Ratio</div>
      </div>
    </div>

    <!-- Chart -->
    <canvas bind:this={chartCanvas}></canvas>
  {:else}
    <p>No record data available. (Maybe refreshed the page?)</p>
  {/if}
</div>
