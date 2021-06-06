<template>
    <vue-draggable-resizable
        :draggable="!$env.state.changesLock && $env.state.editMode"
        :resizable="!$env.state.changesLock && $env.state.editMode"
        @resizestop="onResizeStop"
        @dragstop="onDrag"
        @activated="onActivated"
        @touchstart.native="$_prevent"
        @click.native="$_prevent"
        class="widget"
        :class="[
            widget.border ? 'widget-border' : 'no-border',
            $env.state.optionsSource &&
            $env.state.optionsSource.id == widget.id &&
            $env.state.optionsSource.type == widget.type
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
        :minHeight="50"
        :minWidth="100"
        :grid="[$store.state.app.grid, $store.state.app.grid]"
        ref="base"
    >
        <div class="quick-access widget-quick-access hidden" v-if="$env.state.editMode">
            <button
                v-if="widget.sync_id || widget.is_referenced"
                :title="
                    widget.sync_id
                        ? `This widget is synchronized with ${widget.sync_id}`
                        : 'This widget is referenced by at least one widget'
                "
                :disabled="$env.state.changesLock || !widget.sync_id"
                class="btn btn-sm btn-light border"
                @click="copySyncWidget"
            >
                <i class="fas fa-link"></i>
            </button>
            <button :disabled="$env.state.changesLock" class="btn btn-sm btn-danger" @click="deleteWidget">
                <i class="fas fa-trash"></i>
            </button>
            <button
                :disabled="$env.state.changesLock"
                class="btn btn-sm btn-light border"
                @click="$store.dispatch('copyWidget', widget)"
            >
                <i class="fas fa-copy"></i>
            </button>
            <button class="btn btn-sm btn-light border d-none d-md-block" @click.stop="onOpenOptions">
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
    import { copyToClipboard } from "../../common";

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
                if (!this.$env.state.changesLock) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { w, h }));
                }
            },
            onDrag(x, y) {
                this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
                if (!this.$env.state.changesLock) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { x, y }));
                }
            },
            deleteWidget() {
                if (confirm("Are you sure?")) {
                    this.$env.dispatch("closeOptions");
                    this.$store.dispatch("deleteInstance", this.widget);
                }
            },
            onActivated() {
                this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
                if (this.$env.state.editMode) {
                    window.dispatchEvent(new Event("resize"));
                    $(".widget-quick-access").addClass("hidden");
                    $(this.$el)
                        .find(".widget-quick-access")
                        .removeClass("hidden");
                }
            },
            onOpenOptions() {
                if (this.$env.state.editMode) {
                    this.$env.dispatch("openOptions", this.widget);
                }
            },
            copySyncWidget() {
                copyToClipboard(this.widget.sync_id);
                this.$notify({ text: "Copied to clipboard!", type: "success" });
            },
            $_prevent(e){
                if (this.$env.state.editMode){
                    e.stopPropagation()
                }
            }
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
                return this.widget.help || "";
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
