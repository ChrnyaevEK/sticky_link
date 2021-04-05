<template id="url-template">
    <WidgetBaseResizable :widget="widget">
        <div class="w-100 h-100 d-flex justify-content-center align-items-center">
            <button
                class="btn btn-default p-2 border"
                @click="openHref"
                :disabled="$env.widgetsLocked || $env.changesLocked"
            >
                <a
                    :href="widget.href"
                    @click.stop.prevent="openHref"
                    class="text-break"
                    :style="`color: ${widget.text_color};`"
                    :disabled="$env.widgetsLocked || $env.changesLocked"
                    ><u>{{ widget.text || widget.href }}</u></a
                >
                <i class="fas fa-external-link-square-alt text-muted mx-1"></i>
            </button>
        </div>
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
                if (this.widget.href && !this.$env.widgetsLocked) window.open(this.widget.href, "_blank");
            },
        },
    };
</script>
