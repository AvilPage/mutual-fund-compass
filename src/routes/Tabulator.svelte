<script>
    import {TabulatorFull as Tabulator} from "tabulator-tables";
    import {onMount} from "svelte";

    let tableComponent;
    export let data, columns;

    onMount(() => {
        new Tabulator(tableComponent, {
                data: data, //link data to table
                reactiveData: true, //enable data reactivity
                columns: columns, //define table columns
                layout: "fitColumns", //fit columns to width of table (optional)
                initialFilter: [
                ],
            }
        )
    })
</script>

<div bind:this={tableComponent} style="padding: 15px"></div>

<svelte:head>
    <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/tabulator-tables@5.1.0/dist/css/tabulator.min.css"
    />
</svelte:head>
