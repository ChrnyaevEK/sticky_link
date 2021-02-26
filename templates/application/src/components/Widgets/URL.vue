<template id="url-template">
    <component :is="base" v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="w-100 h-100 d-flex justify-content-center align-items-center">
                <span class="p-2 border rounded" @click="openHref">
                    <a :href="widget.href" target="_blank" class="text-break" :style="`color: ${widget.text_color};`">{{ widget.text || widget.href }}</a>
                </span>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('href')">URL address </label>
                <input :id="_('href')" class="form-control" v-model="widget.href" />
            </div>
            <div class="form-group">
                <label :for="_('text')">URL text </label>
                <input :id="_('text')" class="form-control" v-model="widget.text" />
            </div>
        </template>
    </component>
</template>

<script>
    import { registerIdSystem, Context } from "../../common.js";
    export default {
        type: "url",
        name: "URL",
        template: "#url-template",
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
        data() {
            return {
                Context,
            };
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        methods: {
            openHref() {
                window.open(this.widget.href, "_blank");
            },
        },
    };
</script>
