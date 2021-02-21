<template id="simple-text-widget">
    <component :is="$route.query.mode == Context.edit ? 'WidgetBaseResizable' : 'WidgetBaseSimple'" v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column h-100">
                <span class="flex-grow-1 text-truncate text-wrap text-break">{{ widget.text_content }}</span>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('text_content')"
                    >Content of widget
                </label>
                <textarea :id="_('text_content')" class="form-control" v-model="widget.text_content" rows="10"></textarea>
            </div>
        </template>
    </component>
</template>

<script>
    import WidgetBaseResizable from "./../WidgetBaseResizable";
    import WidgetBaseSimple from "./../WidgetBaseSimple";
    import { registerIdSystem, Context } from "../../common.js";
    export default {
        type: 'simple_text',
        name: "SimpleText",
        template: "#simple-text-widget",
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
