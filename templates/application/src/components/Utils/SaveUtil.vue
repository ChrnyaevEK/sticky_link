<template id="save-util-template">
    <span class="m-3 small font-weight-bold">
        <span :class="io.saveUtil.type ? 'text-' + io.saveUtil.type : 'text-secondary'">
            {{ io.saveUtil.state }}
        </span>
        <span class="px-5 text-secondary">
            {{ io.changeUtil.state }}
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
