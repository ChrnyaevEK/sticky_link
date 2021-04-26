<template>
    <span
        :class="`w-100 alert alert-dismissible fade show position-absolute alert-${this.io.alertUtil.type}`"
        style="z-index: 1;"
        v-show="io.alertUtil.visible"
        v-html="io.alertUtil.html"
        @mouseleave="handleMouseLeave"
        @mouseenter="handleMouseEnter"
    >
        <a class="close btn" aria-label="Close" @click="close">
            <span aria-hidden="true">&times;</span>
        </a></span
    >
</template>
<script>
    import io from "../../modules/io";
    export default {
        data() {
            return {
                io,
                fadeOutId: null,
            };
        },
        methods: {
            handleMouseLeave() {
                clearTimeout(this.fadeOutId);
                this.fadeOutId = setTimeout(() => {
                    this.fadeOutId == null;
                    this.close();
                }, this.io.alertUtil.fadeOutCoolDown);
            },
            handleMouseEnter() {
                clearTimeout(this.fadeOutId);
            },
            close() {
                this.io.alertUtil.visible = false;
            },
        },
    };
</script>
