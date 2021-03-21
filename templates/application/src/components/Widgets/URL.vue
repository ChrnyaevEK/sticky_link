<template id="url-template">
    <component :is="base" v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="w-100 h-100 d-flex justify-content-center align-items-center">
                <span class="btn btn-default p-2 border" @click="openHref" :disabled="$env.state.lockWidgets">
                    <a
                        :href="widget.href"
                        @click.stop.prevent="openHref"
                        class="text-break"
                        :style="`color: ${widget.text_color};`"
                        :disabled="$env.state.lockWidgets"
                        ><u>{{ widget.text || widget.href }}</u></a
                    >
                    <i class="fas fa-external-link-square-alt text-muted mx-1"></i>
                </span>
            </div>
        </template>
    </component>
</template>

<script>
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
        methods: {
            openHref() {
                if (this.widget.href && !this.$env.state.lockWidgets) window.open(this.widget.href, "_blank");
            },
        },
    };
</script>
