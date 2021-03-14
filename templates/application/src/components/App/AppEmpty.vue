<template>
    <div class="w-100 h-100 d-flex flex-column">
        <div class="w-100 p-1 bg-white border-bottom">
            <span>Select or create a <span class="text-success font-weight-bold">wall</span> to continue</span>
            <SaveUtil></SaveUtil>
        </div>
        <div class="w-100 h-100 d-flex flex-column align-items-center">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
        </div>
        <div class="w-100 p-1 d-flex bg-white border-top">
            <WallSelectCreate :deleteWall="false" @createWall="onCreateWall"></WallSelectCreate>
        </div>
    </div>
</template>

<script>
    import WallSelectCreate from "../Utils/WallSelectCreate";
    import AlertUtil from "../Utils/AlertUtil";
    import SaveUtil from "../Utils/SaveUtil";

    export default {
        components: { WallSelectCreate, AlertUtil, SaveUtil },
        methods: {
            onCreateWall() {
                this.$store.dispatch("createWall").then((wall) => {
                    this.$env.dispatch("resolveWallCreated", wall);
                });
            },
        },
    };
</script>
