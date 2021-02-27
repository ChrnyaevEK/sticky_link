<template>
    <vue-draggable-resizable
        @resizing="onResize"
        @dragging="onDrag"
        @mousedown.native.stop
        @mouseup.native.stop
        @mousemove.native.stop
        class="widget"
        :class="[widget.border ? 'widget-border' : 'widget-no-border']"
        :style="style"
        :parent="true"
        :w="widget.w"
        :h="widget.h"
        :y="widget.y"
        :x="widget.x"
        :z="widget.z"
    >
        <div class="widget-quick-access" v-show="quickAccessVisible">
            <button :disabled="lockWidgetCreation" class="btn btn-light border" @click="copyWidget">
                <i class="fas fa-copy"></i>
            </button>
            <button :disabled="lockWidgetCreation" class="btn btn-danger" @click="deleteWidget">
                <i class="fas fa-trash"></i>
            </button>
        </div>
        <div class="w-100 h-100" @contextmenu.stop.prevent="Context.$emit('openWidgetOptions', widget)">
            <slot name="content"></slot>
        </div>
    </vue-draggable-resizable>
</template>

<script>
    // Front end is absolutely passive
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import { registerIdSystem, UpdateManager, Context } from "../../common.js";
    import $ from "jquery";
    Context.$on("addBlankWidget", function(klass) {
        Context.$emit("lockWidgetCreation");
        Context.$emit("routeRequest", ($route) => {
            new UpdateManager(klass.type)
                .create({ wall: $route.params.wallId })
                .then((response) => {
                    Context.$emit("widgetCreated", response);
                })
                .always(() => {
                    Context.$emit("unlockWidgetCreation");
                });
        });
    });

    export default {
        name: "WidgetBaseResizable",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        created() {
            registerIdSystem(this, this.widget); // Create _ function to generate ids
            Context.$on("lockWidgetCreation", this.onLockWidgetCreation);
            Context.$on("unlockWidgetCreation", this.onUnlockWidgetCreation);
            Context.$on("widgetUpdatePosition", (wall) => {
                if (this.widget.x + this.widget.w >= wall.w) {
                    var x = wall.w - this.widget.w;
                    this.widget.x = x < 0 ? 0 : x;
                }
                if (this.widget.y + this.widget.h >= wall.h) {
                    var y = wall.h - this.widget.h;
                    this.widget.y = y < 0 ? 0 : y;
                }
                if (this.widget.h >= wall.h) {
                    this.widget.h = wall.h;
                }
                if (this.widget.w >= wall.w) {
                    this.widget.w = wall.w;
                }
            });
        },
        data: function() {
            var manager = new UpdateManager(this.widget.type, this.widget.id, this.unsetWarning, this.setWarningFromResponse);
            return {
                manager,
                Context,
                lockWidgetCreation: false,
                quickAccessClass: "widget-quick-access",
                quickAccessVisible: false,
            };
        },
        methods: {
            onResize(x, y, w, h) {
                this.widget.w = w;
                this.widget.h = h;
            },
            onDrag(x, y) {
                this.widget.x = x;
                this.widget.y = y;
            },
            deleteWidget() {
                if (confirm("Are you sure?")) {
                    Context.$emit("lockWidgetCreation");
                    this.manager
                        .delete()
                        .then(() => {
                            Context.$emit("widgetDeleted", this.widget);
                        })
                        .always(() => {
                            Context.$emit("unlockWidgetCreation");
                        });
                }
            },
            copyWidget() {
                Context.$emit("lockWidgetCreation");
                this.manager
                    .create({
                        ...this.widget,
                        x: this.widget.x + 5,
                        y: this.widget.y + 5,
                    })
                    .then((widget) => {
                        Context.$emit("widgetCreated", widget);
                    })
                    .always(() => {
                        Context.$emit("unlockWidgetCreation");
                    });
            },
            onLockWidgetCreation() {
                this.lockWidgetCreation = true;
            },
            onUnlockWidgetCreation() {
                this.lockWidgetCreation = false;
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
        watch: {
            widget: {
                handler: function() {
                    this.manager.updated(this.widget);
                },
                deep: true,
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
