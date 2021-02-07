<template id="url-widget">
    <WidgetBase v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="w-100 h-100">
                <a :href="widget.href" target="_blank" class="text-break" :style="`color: ${widget.text_color};`">{{widget.text || widget.href}}</a>    
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('href')"
                    >URL address
                </label>
                <input id="_('href')" class="form-control" v-model="widget.href" :aria-describedby="_('hrefHelp')" />
            </div>
            <div class="form-group">
                <label :for="_('text')"
                    >URL text
                </label>
                <input id="_('text')" class="form-control" v-model="widget.text" :aria-describedby="_('textHelp')" />
            </div>
        </template>
    </WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    import { registerIdSystem } from "../../../common.js";
    export default {
        type: 'url',
        name: "URL",
        template: "#url-widget",
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
