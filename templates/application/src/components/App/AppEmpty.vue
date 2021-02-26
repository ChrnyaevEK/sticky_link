<template>
    <div class="w-100 h-100 d-flex flex-column">
        <span class=" w-100 p-1 bg-white border-bottom">Select or create a <span class="text-success font-weight-bold">wall</span> to continue</span>
        <router-view></router-view>
        <div class="w-100 p-1 d-flex bg-white border-top">
            <WallSelectCreate :deleteWall="false"></WallSelectCreate>
        </div>
    </div>
</template>

<script>
    import WallSelectCreate from "../Utils/WallSelectCreate";
    export default {
        components: { WallSelectCreate },
    };
</script>
