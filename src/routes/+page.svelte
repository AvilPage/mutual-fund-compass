<script>
    import Header from "./Header.svelte";
    import {onMount} from "svelte";
    import mfs from "./data.json"
    import Tabulator from "./Tabulator.svelte";
    import {ModuleRegistry} from 'ag-grid-community';
    import {SetFilterModule} from 'ag-grid-enterprise';

    ModuleRegistry.registerModules([SetFilterModule])

    let isLoading = $state(true);
    let data = mfs;
    // replace Dividend values "z" with "Growth"
    data.forEach((d) => {
        if (d.Dividend === "Z") {
            d.Dividend = "Growth";
        }
    });
    let category_values = {
        "Flexi Cap Fund": "Flexi Cap Fund",
        "Mid Cap Fund": "Mid Cap Fund",
    }

    let columns = [
        {
            title: "Name",
            field: "Name",
            headerFilter: true,
        },
        {
            title: "Type",
            field: "Type",
        },
        {
            title: "Category",
            field: "Category",
            editorParams: {values: category_values},
        },
        {
            title: "NAV",
            field: "Value",
        },
        {
            title: "Dividend",
            field: "Dividend",
        }
    ];


    onMount(async () => {
        console.log(mfs);
        isLoading = false;

        //     load data from csv file
        const gridOptions = {
            // Row Data: The data to be displayed.
            rowData: data,
            // Column Definitions: Defines the columns to be displayed.
            columnDefs: [
                {
                    field: "Name",
                    flex: 1.5,
                    filter: "agTextColumnFilter",
                    floatingFilter: true,
                },
                {
                    field: "Type",
                    filter: "agSetColumnFilter",
                    floatingFilter: true,
                },
                {
                    field: "Category",
                    filter: "agSetColumnFilter",
                    floatingFilter: true,
                },
                {field: "Value"},
                {field: "Dividend"},
            ],
        };

        // Your Javascript code to create the Data Grid
        const myGridElement = document.querySelector('#myGrid');
        agGrid.createGrid(myGridElement, gridOptions);

    });
</script>

<svelte:head>
    <link href="https://unpkg.com/tabulator-tables@4.9.1/dist/css/tabulator.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/ag-grid-community/dist/ag-grid-community.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/ag-grid-enterprise@33.0.3/dist/ag-grid-enterprise.min.js"></script>
</svelte:head>

<Header/>

<div id="myGrid" style="height: 1000px; padding: 20px"></div>

<!--<Tabulator {data} {columns}/>-->

{#if isLoading}
    <div>Loading...</div>
{/if}
