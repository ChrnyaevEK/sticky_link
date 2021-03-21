<template>
    <vue-draggable-resizable
        :draggable="!$env.state.lockChanges"
        :resizable="!$env.state.lockChanges"
        @resizestop="onResizeStop"
        @dragstop="onDrag"
        @click.native.stop
        @mousedown.native.stop
        @mouseup.native.stop
        @mousemove.native.stop
        @contextmenu.stop.prevent
        class="widget"
        :class="[
            widget.border ? 'widget-border' : 'widget-no-border',
            $env.state.editInstance &&
            $env.state.editInstance.id == widget.id &&
            $env.state.editInstance.type == widget.type
                ? 'shadow'
                : '',
        ]"
        :style="style"
        :parent="true"
        :w="widget.w"
        :h="widget.h"
        :y="widget.y"
        :x="widget.x"
        :z="widget.z"
    >
        <div class="widget-quick-access" v-show="quickAccessVisible">
            <button
                :disabled="$env.state.lockChanges"
                class="btn btn-light border"
                @click="$store.dispatch('copyWidget', widget)"
            >
                <i class="fas fa-copy"></i>
            </button>
            <button :disabled="$env.state.lockChanges" class="btn btn-danger" @click="deleteWidget">
                <i class="fas fa-trash"></i>
            </button>
        </div>
        <div class="w-100 h-100" @contextmenu.stop.prevent="$env.dispatch('openOptions', Object.assign({}, widget))">
            <slot name="content"></slot>
        </div>
    </vue-draggable-resizable>
</template>

<script>
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import $ from "jquery";

    export default {
        name: "WidgetBaseResizable",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        data() {
            return {
                quickAccessClass: "widget-quick-access",
                quickAccessVisible: false,
            };
        },
        methods: {
            onResizeStop(x, y, w, h) {
                if (!this.$env.lockChanges) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { w, h }));
                }
            },
            onDrag(x, y) {
                if (!this.$env.lockChanges) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { x, y }));
                }
            },
            deleteWidget() {
                if (confirm("Are you sure?")) {
                    this.$store.dispatch("deleteInstance", this.widget);
                }
            },
        },
        components: {
            VueDraggableResizable,
        },
        computed: {
            style() {
                return `
                    background-color: ${this.widget.background_color};
                    color: ${this.widget.text_color};
                    font-size:${this.widget.font_size}px;
                    font-weight:${this.widget.font_weight};
                `;
            },
        },
        updated() {
            window.dispatchEvent(new Event("resize"));
        },
        mounted() {
            $(this.$el)
                .mouseenter(() => {
                    this.quickAccessVisible = true;
                })
                .mouseleave(() => {
                    this.quickAccessVisible = false;
                });
        },
    };
</script>

<style scoped>
    .control-area {
        width: 100%;
        height: 100%;
        position: absolute;
    }
    .widget-quick-access {
        right: 0;
        top: 0;
        position: absolute;
        display: flex;
        justify-content: flex-end;
        padding: 2px 2px 0 2px;
        z-index: 2;
    }
    .widget-quick-access a {
        margin: 0 0 0 2px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 2rem;
        width: 2rem;
    }
</style>
