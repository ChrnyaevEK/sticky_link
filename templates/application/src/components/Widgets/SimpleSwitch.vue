<template id="simple-switch-template">
    <component :is="base" v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="custom-control custom-switch w-100 h-100">
                <input
                    type="checkbox"
                    @change="changeValue"
                    :checked="widget.value"
                    :id="_('value')"
                    :disabled="$env.state.lockWidgets"
                    class="custom-control-input"
                />
                <label class="custom-control-label w-100 h-100" :for="_('value')">{{ widget.title }}</label>
            </div>
        </template>
    </component>
</template>

<script>
    export default {
        type: "simple_switch",
        name: "SimpleSwitch",
        template: "#simple-switch-template",
        props: {
            widget: {
                type: Object,
                required: true,
            },
            base: {
                type: Object,
                required: true,
            },
        },
        methods: {
            changeValue() {
                if (!this.$env.state.lockWidgets) {
                    this.$store.dispatch(
                        "updateOrAddInstance",
                        Object.assign({}, this.widget, { value: !this.widget.value })
                    );
                }
            },
        },
    };
</script>
