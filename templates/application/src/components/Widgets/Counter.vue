<template id="counter-template">
    <WidgetBaseResizable :widget="widget">
        <span v-show="widget.title" class="w-100 text-truncate widget-title">{{ widget.title }}</span>
        <div
            class="d-flex w-100 h-100 justify-content-between align-items-center"
            :class="{ 'flex-column': widget.vertical }"
        >
            <button
                v-if="widget.vertical"
                key="fa-chevron-up"
                class="btn border-bottom w-100"
                @click="changeValue(widget.step)"
                :disabled="$env.state.widgetsLock || $env.state.changesLock"
            >
                <i class="fa fa-chevron-up"></i>
            </button>
            <button
                v-else
                key="fa-chevron-left"
                class="btn border-right h-100"
                @click="changeValue(-widget.step)"
                :disabled="$env.state.widgetsLock || $env.state.changesLock"
            >
                <i class="fa fa-chevron-left"></i>
            </button>
            <span class="text-truncate text-wrap text-break cursor-default">
                {{ widget.value }}
            </span>
            <button
                v-if="widget.vertical"
                key="fa-chevron-down"
                class="btn border-top w-100"
                @click="changeValue(-widget.step)"
                :disabled="$env.state.widgetsLock || $env.state.changesLock"
            >
                <i class="fa fa-chevron-down"></i>
            </button>
            <button
                v-else
                key="fa-chevron-right"
                class="btn border-left h-100"
                @click="changeValue(widget.step)"
                :disabled="$env.state.widgetsLock || $env.state.changesLock"
            >
                <i class="fa fa-chevron-right"></i>
            </button>
        </div>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
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
        },
    };
</script>
<style scoped>
    button {
        background-color: inherit;
        border-radius: 0;
    }
</style>
