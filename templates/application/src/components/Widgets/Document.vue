<template id="document-template">
    <WidgetBaseResizable :widget="widget">
        <div class="w-100 h-100 center-content flex-column">
            <div>
                <span class="text-truncate">{{ title }}</span
                ><i class="mx-2 fas fa-file-alt text-muted"></i>
            </div>
            <div class="text-muted" v-if="widget.source">Uploaded: {{ timeFormatted(widget.source.last_update) }}</div>
        </div>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import { timeFormatted } from "../../common";
    export default {
        type: "document",
        name: "Document",
        template: "#document-template",
        components: {
            WidgetBaseResizable,
        },
        computed: {
            title() {
                return this.widget.title || (this.widget.source ? this.widget.source.name : "Not chosen");
            },
        },
        methods: {
            timeFormatted,
        },
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
    };
</script>
