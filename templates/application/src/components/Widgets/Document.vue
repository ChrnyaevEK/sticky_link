<template id="document-template">
    <WidgetBaseResizable :widget="widget">
        <div class="h-100 center-content flex-column text-break overflow-hidden">
            <strong :title="title" :class="{ 'text-muted': !title }">{{ title || "Empty" }}</strong>
            <hr class="w-75 text-secondary" />
            <div v-if="title">
                <a :href="sourceURL + '?attachment'" target="_blank" class="text-truncate mr-3">Download</a>
                <a :href="sourceURL" target="_blank" class="text-truncate">Open</a>
            </div>
            <div class="text-muted" v-if="widget.source">{{ timeFormatted(widget.source.last_update) }}</div>
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
            sourceURL() {
                if (this.widget.source && this.widget.source.file) {
                    return this.$store.state.app.sourceURL + this.widget.source.id + "/";
                }
                return false;
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
