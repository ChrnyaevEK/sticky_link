<template id="document-template">
    <WidgetBaseResizable :widget="widget">
        <div class="w-100 h-100 center-content">
            <span>{{ widget.title }}<i class="mx-2 fas fa-file-alt text-muted"></i></span>
        </div>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    export default {
        type: "document",
        name: "Document",
        template: "#document-template",
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
