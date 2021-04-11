<template id="simple-switch-template">
    <WidgetBaseResizable :widget="widget">
        <div
            class="custom-control custom-switch"
            :title="widget.title"
        >
            <input
                type="checkbox"
                @change="changeValue"
                :checked="widget.value"
                :id="_('value')"
                :disabled="$env.widgetsLocked || $env.changesLocked"
                class="custom-control-input"
            />
            <label class="custom-control-label" :for="_('value')">{{ widget.title }}</label>
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
