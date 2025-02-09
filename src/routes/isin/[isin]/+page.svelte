<script>
    import {page} from '$app/stores';

    import Header from "../../Header.svelte";
</script>

<Header/>


Name: {$page.params.isin}
