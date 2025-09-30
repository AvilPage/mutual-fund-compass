<script>
  import Header from "./Header.svelte";
  import { onMount } from "svelte";
  import mfs from "./data.json";
  import { goto } from "$app/navigation";
  import {
    createGrid,
    ModuleRegistry,
    SetFilterModule,
    ClientSideRowModelModule,
    StatusBarModule,
    TextFilterModule,
  } from "ag-grid-enterprise";
  import { get } from "svelte/store";
  import { page } from "$app/stores";

  ModuleRegistry.registerModules([
    SetFilterModule,
    ClientSideRowModelModule,
    StatusBarModule,
    TextFilterModule,
  ]);

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
     const url = get(page).url;
    const fundHouseFilter = url.searchParams.get("fund_house");

    //     load data from csv file
    const gridOptions = {
      // onGridReady: (event) => event.api.sizeColumnsToFit(),
      // onGridReady: (event) => event.api.autoSizeAllColumns(),
      // autoSizeStrategy: {
      //     type: 'SizeColumnsToFitProvidedWidthStrategy'
      // },
      // domLayout: "autoHeight",
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
          width: 400,
          // flex: 0.5,
        },
        {
          field: "Type",
          filter: "agSetColumnFilter",
          floatingFilter: true,
          width: 100,
        },
        {
          field: "Category",
          filter: "agSetColumnFilter",
          floatingFilter: true,
          width: 200,
        },
        {
          field: "nav",
          headerName: "NAV",
          width: 100,
          valueFormatter: function (params) {
            return typeof params.value === "number"
              ? params.value.toFixed(2)
              : params.value;
          },
        },

        {
          field: "expense_ratio",
          headerName: "TER",
          width: 70,
          valueFormatter: function (params) {
            return typeof params.value === "number"
              ? params.value.toFixed(2)
              : params.value;
          },
        },
        {
          field: "aum",
          headerName: "AUM(Cr)",
          width: 100,
          valueFormatter: function (params) {
            return typeof params.value === "number"
              ? Math.round(params.value)
              : params.value;
          },
        },
        {
          field: "year_1",
          headerName: "1Y",
          width: 70,
          valueFormatter: function (params) {
            return typeof params.value === "number"
              ? params.value.toFixed(2)
              : params.value;
          },
        },
        {
          field: "inception",
          headerName: "Max",
          width: 70,
          valueFormatter: function (params) {
            return typeof params.value === "number"
              ? params.value.toFixed(2)
              : params.value;
          },
        },
         {
          field: "Dividend",
          width: 100,
        },
        {
          field: "fund_house",
          filter: "agTextColumnFilter",
          floatingFilter: true,
          width: 200,
          // flex: 0.5, 
        },
      ],
      //   onRowClicked: (event) => {
      //     // event.data has the row data
      //     console.log("Row clicked", event.data);

      //     // navigate to another page (example using window.location)
      //     window.location.href = `/details/${event.data.Name}`;

      //     // OR if using svelte-navigator / svelte-spa-router:
      //     // navigate(`/details/${event.data.id}`, { state: event.data });
      //   },
      //   onRowClicked: (event) => {
      //     goto(`/details`, { state: event.data });
      //   },
    //   onRowClicked: (event) => {
    //     const record = event.data;
    //     const encodedName = encodeURIComponent(event.data.Name);

    //     goto(`/details/${encodedName}`, { state: record });
    //   },
    onGridReady: (params) => {
        if (fundHouseFilter) {
          params.api.setFilterModel({
            fund_house: { type: "contains", filter: fundHouseFilter }
          });
          params.api.onFilterChanged();
        }
      },
    onRowClicked: (event) => {
    console.log("Row clicked:", event.data);
    const record = event.data;
    const encodedName = encodeURIComponent(record.Name + record.isin);
    goto(`/details/${encodedName}`, { state: record });
},

      statusBar: {
        statusPanels: [
          { statusPanel: "agTotalAndFilteredRowCountComponent" },
          { statusPanel: "agTotalRowCountComponent" },
          { statusPanel: "agFilteredRowCountComponent" },
          { statusPanel: "agSelectedRowCountComponent" },
          { statusPanel: "agAggregationComponent" },
        ],
      },
    };

    // Your Javascript code to create the Data Grid
    const myGridElement = document.querySelector("#myGrid");
    if (myGridElement) {
      createGrid(myGridElement, gridOptions);
    }
  });
</script>

<svelte:head>
  <style>
    

    .ag-theme-alpine .ag-body-viewport {
      bottom: 0px;
      border-top: solid 1px lightgrey;
    }
   #myGrid {
  display: flex;
  flex-direction: column;
}

.ag-root-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.ag-body-viewport {
  flex: 1; /* fills available space */
}

.ag-status-bar {
  margin-top: auto; /* push to bottom */
  position: sticky;
  bottom: 0;
  background: white; /* optional */
}
  </style>
</svelte:head>

<Header />

<div
  id="myGrid"
  class="ag-theme-alpine"
  style="width: 100%; height: 95vh; padding: 20px;"
></div>

{#if isLoading}
  <div>Loading...</div>
{/if}


