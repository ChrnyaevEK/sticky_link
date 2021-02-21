<template id="counter">
    <component
        :is="
            $route.query.mode == Context.edit
                ? 'WidgetBaseResizable'
                : 'WidgetBaseSimple'
        "
        v-bind="{ ...$props, ...$attrs }"
    >
        <template slot="content">
            <div class="d-flex flex-column w-100 h-100">
                <span class="w-100 text-center">{{ widget.title }}</span>
                <button
                    @dblclick.stop.prevent
                    class="btn"
                    @click.stop="widget.value += 1"
                >
                    <i class="fa fa-chevron-up"></i>
                </button>
                <div
                    class="d-flex justify-content-center align-items-center h-100"
                >
                    <span
                        class="text-truncate text-wrap text-center text-break"
                    >
                        {{ widget.value }}
                    </span>
                </div>
                <button
                    @dblclick.stop.prevent
                    class="btn"
                    @click.stop="widget.value -= 1"
                >
                    <i class="fa fa-chevron-down"></i>
                </button>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('value')">Value </label>
                <input
                    :id="_('value')"
                    class="form-control"
                    v-model.number="widget.value"
                    :aria-describedby="_('valueHelp')"
                />
            </div>
            <div class="form-group">
                <label :for="_('title')">Title </label>
                <input
                    :id="_('title')"
                    class="form-control"
                    v-model.number="widget.title"
                    :aria-describedby="_('titleHelp')"
                />
            </div>
        </template>
    </component>
</template>

<script>
    import WidgetBaseResizable from "./../WidgetBaseResizable";
    import WidgetBaseSimple from "./../WidgetBaseSimple";
    import { registerIdSystem, Context  } from "../../common.js";
    export default {
        type: "counter",
        name: "Counter",
        template: "#counter",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        data(){
            return {
                Context
            }
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        components: {
            WidgetBaseResizable,
            WidgetBaseSimple,
        },
    };
</script>
<style scoped>
    button {
        background-color: inherit;
        border-radius: 0;
    }
</style>
