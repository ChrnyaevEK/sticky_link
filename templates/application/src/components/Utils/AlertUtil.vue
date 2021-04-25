<template>
    <span
        :class="`w-100 alert alert-dismissible fade show position-absolute alert-${this.io.alertUtil.type}`"
        style="z-index: 1;"
        v-show="io.alertUtil.visible"
        v-html="io.alertUtil.html"
        @mouseout="handleMouseOut"
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
            handleMouseOut() {
                if (this.fadeOutId == null) {
                    this.fadeOutId = setTimeout(() => {
                        this.fadeOutId == null
                        this.close();
                    }, this.io.alertUtil.fadeOutCoolDown);
                }
            },
            close() {
                this.io.alertUtil.visible = false;
            },
        },
    };
</script>
