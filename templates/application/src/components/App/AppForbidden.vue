<template>
    <div class="w-100 h-100 d-flex flex-column">
        <div class="w-100 p-1 bg-white border-bottom">
            <span>Select or create a <span class="text-success font-weight-bold">wall</span> to continue</span>
        </div>
        <div class="w-100 h-100 d-flex flex-column align-items-center">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import AlertUtil from "../Utils/AlertUtil";

    export default {
        components: { AlertUtil },
    };
</script>
