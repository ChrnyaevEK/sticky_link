<template id="simple-switch-template">
    <WidgetBaseResizable :widget="widget">
        <span v-show="widget.title" class="w-100 text-truncate widget-title">{{ widget.title }}</span>
        <div
            class="custom-control custom-switch h-100 w-100 d-flex justify-content-center align-items-center"
            :title="widget.title"
        >
            <input
                type="checkbox"
                @change="changeValue"
                :checked="widget.value"
                v-scope:id.value
                :disabled="$env.state.widgetsLock || $env.state.changesLock"
                class="custom-control-input"
            />
            <label class="custom-control-label" v-scope:for.value>{{ widget.title }}</label>
        </div>
    </WidgetBaseResizable>
</template>

<script>
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    export default {
        type: "simple_switch",
        name: "SimpleSwitch",
        template: "#simple-switch-template",
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
            changeValue() {
                this.$store.dispatch(
                    "updateOrAddInstance",
                    Object.assign({}, this.widget, { value: !this.widget.value })
                );
            },
        },
    };
</script>
