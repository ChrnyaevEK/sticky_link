<template id="save-util-template">
    <span class="mx-1 small font-weight-bold" :class="io.saveUtil.type ? 'text-' + io.saveUtil.type : 'text-secondary'">
        {{ io.saveUtil.state }}
    </span>
</template>
<script>
    import io  from "../../modules/io";
    export default {
        data() {
            return {
                io,
            };
        },
    };
</script>
