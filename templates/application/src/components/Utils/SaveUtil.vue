<template id="save-util-template">
    <span class="m-1 small font-weight-bold holder">
        <span class="text-overflow" :class="io.saveUtil.type ? 'text-' + io.saveUtil.type : 'text-secondary'">
            {{ io.saveUtil.state }}
        </span>
    </span>
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
<style scoped>
    .holder {
        width: 450px;
    }
    .text-overflow {
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
    }
</style>
