<template id="simple-switch-template">
    <WidgetBaseResizable :widget="widget">
        <div class="custom-control custom-switch w-100 h-100">
            <input
                type="checkbox"
                @change="changeValue"
                :checked="widget.value"
                :id="_('value')"
                :disabled="$env.widgetsLocked"
                class="custom-control-input"
            />
            <label class="custom-control-label w-100 h-100" :for="_('value')">{{ widget.title }}</label>
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
                if (!this.$env.widgetsLocked) {
                    this.$store.dispatch(
                        "updateOrAddInstance",
                        Object.assign({}, this.widget, { value: !this.widget.value })
                    );
                }
            },
        },
    };
</script>
