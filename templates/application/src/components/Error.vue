<template>
    <div class="d-flex flex-column justify-content-center align-items-center w-100 h-100 bg-light">
        <h4 class="text-secondary">
            <strong>An error occurred...</strong>
        </h4>
        <small class="text-muted">Application failed for some reasons </small>
        <small class="text-muted">We do our best to fix the issue</small>
        <button @click="reload" class="w-25 m-2 btn btn-sm btn-success">
            <strong>Reload</strong> (reloading in {{ beforeReload }}s.)
        </button>
    </div>
</template>
<script>
    export default {
        name: "Error",
        data() {
            return {
                beforeReloadDefault: 10,
                beforeReload: null,
                reloadInterval: null,
            };
        },
        created() {
            this.beforeReload = this.beforeReloadDefault;
            setInterval(() => {
                if (this.beforeReload > 0) {
                    this.beforeReload -= 1;
                }
            }, 1000);
            setTimeout(this.reload, this.beforeReloadDefault * 1000);
        },
        methods: {
            reload() {
                location.href = "/";
            },
        },
    };
</script>
