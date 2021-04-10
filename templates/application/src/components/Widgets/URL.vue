<template id="url-template">
    <WidgetBaseResizable :widget="widget">
        <div class="w-100 h-100 p-2 d-flex flex-column">
            <span class="text-truncate">{{ widget.title }}</span>
            <a
                @click.stop.prevent="openHref"
                class="w-100 h-100 text-break border cursor-pointer d-flex justify-content-center align-items-center"
                :style="`color: ${widget.text_color};`"
                :disabled="$env.widgetsLocked || $env.changesLocked"
                ><u>{{ widget.text || widget.href }}</u>
                <i class="mx-2 fas fa-external-link-square-alt text-muted"></i>
            </a>
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
                if (this.widget.href && !this.$env.widgetsLocked) {
                    window.open(this.widget.href, this.widget.open_in_new_window ? "_blank" : undefined);
                }
            },
        },
    };
</script>
