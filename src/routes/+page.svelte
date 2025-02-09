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
            // onGridReady: (event) => event.api.sizeColumnsToFit(),
            // onGridReady: (event) => event.api.autoSizeAllColumns(),
            // autoSizeStrategy: {
            //     type: 'SizeColumnsToFitProvidedWidthStrategy'
            // },
            domLayout: "autoHeight",
            // Row Data: The data to be displayed.
            rowData: data,
            suppressHorizontalScroll: false,
            suppressVerticalScroll: false,
            // Column Definitions: Defines the columns to be displayed.
            columnDefs: [
                {
                    field: "Name",
                    filter: "agTextColumnFilter",
                    floatingFilter: true,
                    width: 320,
                    // flex: 0.5,
                },
                {
                    field: "Type",
                    filter: "agSetColumnFilter",
                    floatingFilter: true,
                    width: 90,
                },
                {
                    field: "Category",
                    filter: "agSetColumnFilter",
                    floatingFilter: true,
                    width: 150,
                },
                {
                    field: "expense_ratio",
                    headerName: "Exp%",
                    width: 100,

                },
                {
                    field: "aum",
                    headerName: "AUM",
                    width: 90,
                },
                {
                    field: "year_1",
                    headerName: "1Y Ret",
                    width: 120,
                },
                {
                    field: "inception",
                    headerName: "Since Inception",
                    width: 150,
                },
                {
                    field: "Value",
                    width: 100,
                },
                {
                    field: "Dividend",
                    width: 150,
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
