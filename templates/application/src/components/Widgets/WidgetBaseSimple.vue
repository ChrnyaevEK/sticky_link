<template>
    <div class="widget" :class="[widget.border ? 'widget-border' : 'widget-no-border']" :style="style">
        <slot name="content"></slot>
    </div>
</template>

<script>
    import { UpdateManager } from "../../common.js";
    export default {
        name: "WidgetBaseSimple",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        data: function() {
            var manager = new UpdateManager(this.widget.type, this.widget.id);
            return {
                manager,
            };
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
        watch: {
            widget: {
                handler: function() {
                    this.manager.updated(this.widget);
                },
                deep: true,
            },
        },
    };
</script>
