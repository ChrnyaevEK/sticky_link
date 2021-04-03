<template id="simple-switch-template">
    <WidgetBaseResizable :widget="widget">
        <div class="h-100 custom-control custom-switch d-flex justify-content-center align-items-center" :title="widget.title">
            <input
                type="checkbox"
                @change="changeValue"
                :checked="widget.value"
                :id="_('value')"
                :disabled="$env.widgetsLocked"
                class="custom-control-input"
            />
            <label class="custom-control-label text-muted small" :for="_('value')">{{ widget.title }}</label>
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
