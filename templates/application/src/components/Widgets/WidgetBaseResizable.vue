<template>
    <vue-draggable-resizable
        :draggable="!$env.changesLocked && $env.edit"
        :resizable="!$env.changesLocked && $env.edit"
        @resizestop="onResizeStop"
        @dragstop="onDrag"
        @activated="onActivated"
        @touchstart.native.stop
        @click.native.stop
        class="widget"
        :class="[
            widget.border ? 'widget-border' : 'no-border',
            $env.openOptionsFor && $env.openOptionsFor.id == widget.id && $env.openOptionsFor.type == widget.type
                ? 'shadow'
                : '',
        ]"
        :title="title"
        :style="style"
        :parent="true"
        :w="widget.w"
        :h="widget.h"
        :y="widget.y"
        :x="widget.x"
        :z="widget.z"
        :minHeight="50"
        :minWidth="50"
        :grid="[$store.state.app.grid, $store.state.app.grid]"
        ref="base"
    >
        <div class="quick-access widget-quick-access hidden" v-if="$env.edit">
            <button :disabled="$env.changesLocked" class="btn btn-sm btn-danger" @click="deleteWidget">
                <i class="fas fa-trash"></i>
            </button>
            <button
                :disabled="$env.changesLocked"
                class="btn btn-sm btn-light border"
                @click="$store.dispatch('copyWidget', widget)"
            >
                <i class="fas fa-copy"></i>
            </button>
            <button class="btn btn-sm btn-light border" @click.stop="onOpenOptions">
                <i class="fas fa-ellipsis-v"></i>
            </button>
        </div>
        <slot></slot>
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
        beforeUpdate() {
            this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
        },
        methods: {
            onResizeStop(x, y, w, h) {
                this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
                if (!this.$env.changesLocked) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { w, h }));
                }
            },
            onDrag(x, y) {
                this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
                if (!this.$env.changesLocked) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { x, y }));
                }
            },
            deleteWidget() {
                if (confirm("Are you sure?")) {
                    this.$store.dispatch("deleteInstance", this.widget);
                }
            },
            onActivated() {
                this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
                if (this.$env.edit) {
                    window.dispatchEvent(new Event("resize"));
                    $(".widget-quick-access").addClass("hidden");
                    $(this.$el)
                        .find(".widget-quick-access")
                        .removeClass("hidden");
                }
            },
            onOpenOptions() {
                if (this.$env.edit) {
                    this.$env.openOptions(this.widget);
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
            title() {
                if (this.widget.title || this.widget.help) {
                    return `Title: ${this.widget.title || ""};\n${this.widget.help || ""}`;
                }
                return "";
            },
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
    .widget-quick-access > * {
        margin: 0 0 0 2px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 2rem;
        width: 2rem;
    }
</style>
