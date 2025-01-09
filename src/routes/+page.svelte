<script>
    import Header from "./Header.svelte";
    import {onMount} from "svelte";
    import mfs from "./data.json"
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

    onMount(async () => {
        console.log(mfs);
        isLoading = false;

        //     load data from csv file
        const gridOptions = {
            domLayout: "autoHeight",
            // Row Data: The data to be displayed.
            rowData: data,
            // Column Definitions: Defines the columns to be displayed.
            columnDefs: [
                {
                    field: "Name",
                    flex: 2,
                    filter: "agTextColumnFilter",
                    floatingFilter: true,
                },
                {
                    field: "Type",
                    flex: 0.6,
                    filter: "agSetColumnFilter",
                    floatingFilter: true,
                },
                {
                    field: "Category",
                    filter: "agSetColumnFilter",
                    floatingFilter: true,
                },
                {field: "expense_ratio"},
                {
                    field: "aum",
                    flex: 0.6,
                },
                {
                    field: "Value",
                    flex: 0.6,
                },
                {
                    field: "Dividend"
                },
            ],
            statusBar: {
                statusPanels: [
                    {statusPanel: 'agTotalAndFilteredRowCountComponent'},
                    {statusPanel: 'agTotalRowCountComponent'},
                    {statusPanel: 'agFilteredRowCountComponent'},
                    {statusPanel: 'agSelectedRowCountComponent'},
                    {statusPanel: 'agAggregationComponent'}
                ]
            },
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
    <style>
        .ag-theme-alpine .ag-status-bar {
            font-weight: normal;
            position: absolute;
            top: 50px;
            right: 5px;
            border-top: none !important;
        }

        .ag-theme-alpine .ag-body-viewport {
            top: 50px;
            border-top: solid 1px lightgrey;
        }
    </style>

</svelte:head>

<Header/>

<div id="myGrid" style="width: 100%; height: 100%; padding: 20px"></div>

{#if isLoading}
    <div>Loading...</div>
{/if}

<style>
    .ag-theme-alpine .ag-status-bar {
        font-weight: normal;
        position: absolute;
        top: 50px;
        right: 5px;
        border-top: none !important;
    }

    .ag-theme-alpine .ag-body-viewport {
        top: 50px;
        border-top: solid 1px lightgrey;
    }
</style>
