<template>
    <span
        class="w-75 alert alert-dismissible fade show position-absolute"
        style="z-index: 1;"
        v-show="io.alertUtil.visible"
        :class="'alert-' + io.alertUtil.type"
        @mouseout="io.alertUtil.visible = false"
        v-html="io.alertUtil.html"
        >
        <a class="close btn" aria-label="Close" @click="io.alertUtil.visible = false">
            <span aria-hidden="true">&times;</span>
        </a></span
    >
</template>
<script>
    import { io } from "../../common";
    export default {
        data() {
            return {
                io,
            };
        },
    };
</script>
