<script>
    import Header from "./Header.svelte";
    import {onMount} from "svelte";
    import mfs from "./result.json"
    import Tabulator from "./Tabulator.svelte";

    let isLoading = $state(true);
    let data = mfs;
    let columns = [
        {
            title: "Scheme Name",
            field: "Scheme Name",
            headerFilter: true,
        },
        {
            title: "NAV",
            field: "Net Asset Value",
        }
    ];

    onMount(async () => {
        console.log(mfs);
        isLoading = false;
        //     load data from csv file
    });
</script>

<svelte:head>
    <link href="https://unpkg.com/tabulator-tables@4.9.1/dist/css/tabulator.min.css" rel="stylesheet">
</svelte:head>

<Header/>

<Tabulator {data} {columns}/>

{#if isLoading}
    <div>Loading...</div>
{/if}
