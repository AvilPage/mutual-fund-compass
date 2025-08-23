<script lang="ts">
    const brandText = "Mutual Fund Compass";
    import {
        Navbar,
        NavbarBrand,
        NavLink,
        Nav,
    } from "@sveltestrap/sveltestrap";
</script>

<Navbar color="primary-subtle" expand="md" container="md" class="shadow-sm py-2">
    <NavbarBrand href="/" class="d-flex align-items-center gap-2">
        <img src="/favicon.png" alt="Logo" width="32" height="32"
             style="border-radius:6px;box-shadow:0 1px 3px #0001;"/>
        <span class="fw-bold">{brandText}</span>
    </NavbarBrand>
    <Nav class="ms-auto" navbar>
        <NavLink href="/why">Why?</NavLink>
        <NavLink href="https://github.com/AvilPage/mutual-fund-compass">GitHub</NavLink>
    </Nav>
</Navbar>

<style>
    .navbar-brand span {
        font-size: 1.25rem;
        letter-spacing: 0.5px;
    }
</style>
