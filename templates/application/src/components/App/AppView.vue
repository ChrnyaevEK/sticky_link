<template>
    <div class="w-100 h-100 d-flex flex-column">
        <span class=" w-100 p-1 bg-white border-bottom">
            <a href="/" class="m-3"> Sticky link </a>
            <router-link
                class="mr-3"
                :to="{
                    name: 'wallEdit',
                    params: { wallId: $route.params.wallId },
                }"
                >Edit</router-link
            >
            <SaveUtil></SaveUtil>
        </span>
        <div class="w-100 h-100 d-flex flex-column align-items-center">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import SaveUtil from "../Utils/SaveUtil";
    import AlertUtil from "../Utils/AlertUtil";
    export default {
        components: { SaveUtil, AlertUtil },
    };
</script>
