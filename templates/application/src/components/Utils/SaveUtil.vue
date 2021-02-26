<template id="save-util-template">
    <span class="mr-3 small font-weight-bold text-secondary">
        <span v-if="Context.saving">Saving...</span>
        <span v-else-if="Context.saved" class="text-success">Saved!</span>
        <span v-else>Auto save</span>
    </span>
</template>
<script>
    import { Context } from "../../common.js";
    export default {
        data() {
            return { Context };
        },
    };
</script>
