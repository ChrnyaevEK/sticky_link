<template id="simple-text-widget">
    <WidgetBase v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column h-100">
                <span class="flex-grow-1 text-truncate text-wrap text-break">
                    {{ widget.text_content }}
                </span>
                <span class="text-right text-secondary">{{ widget.text_content ? widget.text_content.length : 0 }}/{{ widget.max_length }}</span>
            </div>
        </template>
    </WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    // import API from "../../../common.js";
    export default {
        name: "SimpleText",
        template: "#simple-text-widget",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        components: {
            WidgetBase,
        },
    };
</script>
