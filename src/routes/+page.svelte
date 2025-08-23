<script>
    import Header from "./Header.svelte";
    import {onMount} from "svelte";
    import mfs from "./data.json"
    import {ModuleRegistry} from 'ag-grid-community';
    import {SetFilterModule, ClientSideRowModelModule} from 'ag-grid-enterprise';
    import { createGrid } from 'ag-grid-community';

    ModuleRegistry.registerModules([SetFilterModule, ClientSideRowModelModule])

    let isLoading = $state(true);
    let data = mfs;
    // replace Dividend values "z" with "Growth"
    data.forEach((d) => {
        if (d.Dividend === "Z") {
            d.Dividend = "Growth";
        }
    });

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
                    width: 450,
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
                    field: "Value",
                    headerName: "NAV",
                    width: 70,
                    valueFormatter: function(params) { return (typeof params.value === 'number' ? params.value.toFixed(2) : params.value); },
                },

                {
                    field: "expense_ratio",
                    headerName: "TER",
                    width: 70,
                    valueFormatter: function(params) { return (typeof params.value === 'number' ? params.value.toFixed(2) : params.value); },
                },
                {
                    field: "aum",
                    headerName: "AUM(Cr)",
                    width: 100,
                    valueFormatter: function(params) { return (typeof params.value === 'number' ? Math.round(params.value) : params.value); },
                },
                {
                    field: "year_1",
                    headerName: "1Y",
                    width: 70,
                    valueFormatter: function(params) { return (typeof params.value === 'number' ? params.value.toFixed(2) : params.value); },
                },
                {
                    field: "inception",
                    headerName: "Max",
                    width: 70,
                    valueFormatter: function(params) { return (typeof params.value === 'number' ? params.value.toFixed(2) : params.value); },
                },
                {
                    field: "Dividend",
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
        if (myGridElement) {
            createGrid(myGridElement, gridOptions);
        }

    });
</script>

<svelte:head>
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
