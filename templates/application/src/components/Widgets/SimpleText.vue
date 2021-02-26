<template id="simple-text-template">
    <component :is="base" v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column h-100">
                <span class="flex-grow-1 text-truncate text-wrap text-break ql-editor" v-html="widget.text_content"></span>
            </div>
        </template>
    </component>
</template>

<script>
    import { registerIdSystem, Context } from "../../common.js";
    export default {
        type: "simple_text",
        name: "SimpleText",
        template: "#simple-text-template",
        props: {
            widget: {
                type: Object,
                required: true,
            },
            base: {
                type: Object,
                required: true,
            },
        },
        data() {
            return {
                Context,
            };
        },
        created() {
            registerIdSystem(this, this.widget); // Create _ function to generate ids
        },
    };
</script>
