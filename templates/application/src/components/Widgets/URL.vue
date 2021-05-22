<template id="url-template">
    <WidgetBaseResizable :widget="widget">
        <a
            @click.stop.prevent="openHref"
            class="w-100 h-100 text-break cursor-pointer d-flex justify-content-center align-items-center"
            :style="`color: ${widget.text_color};`"
            :disabled="$env.state.widgetsLock || $env.state.changesLock"
            ><u>{{ widget.text || widget.href }}</u>
            <i class="mx-2 fas fa-external-link-square-alt text-muted"></i>
        </a>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    export default {
        type: "url",
        name: "URL",
        template: "#url-template",
        components: {
            WidgetBaseResizable,
        },
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        methods: {
            openHref() {
                if (this.widget.href && !this.$env.state.widgetsLock) {
                    window.open(this.widget.href, this.widget.open_in_new_window ? "_blank" : undefined);
                }
            },
        },
    };
</script>
