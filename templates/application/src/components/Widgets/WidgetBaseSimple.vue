<template>
    <div class="widget" :class="[widget.border ? 'widget-border' : 'widget-no-border']" :style="style">
        <slot name="content"></slot>
    </div>
</template>

<script>
    export default {
        name: "WidgetBaseSimple",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        watch: {
            widget: {
                handler() {
                    if (!this.$env.lockChanges) {
                        this.$store.dispatch("updateOrAddInstance", this.widget);
                    }
                },
                deep: true,
            },
        },
        computed: {
            style() {
                return `
                    width: ${this.widget.w}px;
                    height: ${this.widget.h}px;
                    z_index: ${this.widget.z};
                    top: ${this.widget.y}px;
                    left: ${this.widget.x}px;
                    background-color: ${this.widget.background_color};
                    color: ${this.widget.text_color};
                    font-size:${this.widget.font_size}px;
                    font-weight:${this.widget.font_weight};
                `;
            },
        },
    };
</script>
