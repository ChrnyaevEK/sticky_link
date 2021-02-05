<template id="simple-text-widget">
    <WidgetBase v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column h-100">
                <span class="flex-grow-1 text-truncate text-wrap text-break">
                    {{ widget.text_content }}
                </span>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('left')" class="w-100 d-flex justify-content-between"
                    >Content of widget
                </label>
                <textarea id="_('text_content')" class="form-control" v-model="widget.text_content" :aria-describedby="_('textContentHelp')" rows="10"></textarea>
            </div>
        </template>
    </WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    import { registerIdSystem } from "../../../common.js";
    export default {
        type: 'simple_text',
        name: "SimpleText",
        template: "#simple-text-widget",
        data(){
            return {
            }
        },
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        components: {
            WidgetBase,
        },
    };
</script>
