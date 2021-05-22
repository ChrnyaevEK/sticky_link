<template id="simple-text-template">
    <WidgetBaseResizable :widget="widget">
        <span
            class="w-100 h-100 flex-grow-1 text-truncate text-wrap text-break ql-editor editor p-0"
            v-html="widget.text_content"
        ></span>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    export default {
        type: "simple_text",
        name: "SimpleText",
        template: "#simple-text-template",
        components: {
            WidgetBaseResizable,
        },
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
    };
</script>

<style>
    .editor {
        min-height: unset !important;
    }
</style>
