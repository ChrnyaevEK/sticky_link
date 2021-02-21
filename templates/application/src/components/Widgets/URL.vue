<template id="url-widget">
    <component
        :is="
            $route.query.mode == Context.edit
                ? 'WidgetBaseResizable'
                : 'WidgetBaseSimple'
        "
        v-bind="{ ...$props, ...$attrs }"
    >
        <template slot="content">
            <div
                class="w-100 h-100 d-flex justify-content-center align-items-center"
            >
                <span class="p-2 border rounded" @click="openHref">
                    <a
                        :href="widget.href"
                        target="_blank"
                        class="text-break"
                        :style="`color: ${widget.text_color};`"
                        >{{ widget.text || widget.href }}</a
                    >
                </span>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('href')">URL address </label>
                <input
                    :id="_('href')"
                    class="form-control"
                    v-model="widget.href"
                />
            </div>
            <div class="form-group">
                <label :for="_('text')">URL text </label>
                <input
                    :id="_('text')"
                    class="form-control"
                    v-model="widget.text"
                />
            </div>
        </template>
    </component>
</template>

<script>
    import WidgetBaseResizable from "./../WidgetBaseResizable.vue";
    import WidgetBaseSimple from "./../WidgetBaseSimple";
    import { registerIdSystem, Context } from "../../common.js";
    export default {
        type: "url",
        name: "URL",
        template: "#url-widget",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        data() {
            return {
                Context,
            };
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        components: {
            WidgetBaseResizable,
            WidgetBaseSimple,
        },
        methods: {
            openHref() {
                window.open(this.widget.href, "_blank");
            },
        },
    };
</script>
