<script lang="ts">
    const brandText = "Mutual Fund Compass";
    import {Navbar, NavbarBrand, NavLink} from "@sveltestrap/sveltestrap";
</script>

<Navbar color="primary-subtle" expand="md" container="md">
    <NavbarBrand href="/">{brandText}</NavbarBrand>
    <NavLink href="https://github.com/AvilPage/mutual-fund-compass">GitHub</NavLink>
    <NavLink href="/why">Why?</NavLink>
</Navbar>
