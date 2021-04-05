<template id="counter-template">
    <WidgetBaseResizable :widget="widget">
        <div class="d-flex flex-column w-100 h-100">
            <span class="w-100 text-center">{{ widget.title }}</span>
            <button class="btn" @click.stop="changeValue(1)" :disabled="$env.widgetsLocked || $env.changesLocked">
                <i class="fa fa-chevron-up"></i>
            </button>
            <div class="d-flex justify-content-center align-items-center h-100">
                <span class="text-truncate text-wrap text-center text-break">
                    <span class="cursor-default">{{ widget.value }}</span>
                    <button
                        class="btn btn-sm small"
                        @click="copyToClipboard"
                        :disabled="$env.widgetsLocked || $env.changesLocked"
                    >
                        <i class="fas fa-copy"></i>
                    </button>
                </span>
            </div>
            <button class="btn" @click.stop="changeValue(-1)" :disabled="$env.widgetsLocked || $env.changesLocked">
                <i class="fa fa-chevron-down"></i>
            </button>
        </div>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import { copyToClipboard } from "../../common";
    export default {
        type: "counter",
        name: "Counter",
        template: "#counter-template",
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
            changeValue(diff) {
                var value = this.widget.value + diff;
                this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { value }));
            },
            copyToClipboard() {
                copyToClipboard(this.widget.value);
            },
        },
    };
</script>
<style scoped>
    button {
        background-color: inherit;
        border-radius: 0;
    }
</style>
