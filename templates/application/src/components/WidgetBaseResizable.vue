<template>
    <vue-draggable-resizable
        @resizing="onResize"
        @dragging="onDrag"
        @mousedown.native.stop
        @mouseup.native.stop
        @mousemove.native.stop
        @click.native.stop
        class="widget"
        :parent="true"
        :w="widget.w"
        :h="widget.h"
        :y="widget.y"
        :x="widget.x"
        :z="widget.z"
    >
        <div class="widget-quick-access w-100" v-show="quickAccessVisible">
            <a class="btn btn-light border" @click="copyWidget"
                ><i class="fas fa-copy"></i
            ></a>
            <a class="btn btn-danger" @click="deleteWidget"
                ><i class="fas fa-trash"></i
            ></a>
        </div>
        <div
            class="w-100 h-100"
            :style="style"
            @contextmenu.stop.prevent="onOpenOptions"
        >
            <slot name="content"></slot>
        </div>
        <vue-draggable-resizable
            v-if="optionsVisible"
            @mousedown.native.stop
            @mouseup.native.stop
            @mousemove.native.stop
            :w="400"
            :h="600"
            :z="4"
            :resizable="false"
            :parent="false"
            class="bg-white widget-options border overflow-auto shadow rounded"
        >
            <div class="w-100 h-100 p-3">
                <div class="form-group d-flex justify-content-between">
                    <strong>Options</strong>
                    <a class="btn" @click="onCloseOptions"
                        ><i class="fas fa-times"></i
                    ></a>
                </div>

                <div class="form-group">
                    <label :for="_('x')">X coordinate</label>
                    <input
                        class="form-control"
                        v-model.number="widget.x"
                        type="number"
                        :id="_('x')"
                        step="1"
                    />
                </div>

                <div class="form-group">
                    <label :for="_('y')">Y coordinate</label>
                    <input
                        class="form-control"
                        v-model.number="widget.y"
                        type="number"
                        :id="_('y')"
                        step="1"
                    />
                </div>

                <div class="form-group">
                    <label :for="_('z')">Z coordinate</label>
                    <input
                        class="form-control"
                        v-model.number="widget.z"
                        type="number"
                        :id="_('z')"
                        step="1"
                    />
                </div>

                <div class="form-group">
                    <label :for="_('w')">Width</label>
                    <input
                        class="form-control"
                        v-model.number="widget.w"
                        type="number"
                        :id="_('w')"
                        step="1"
                    />
                </div>

                <div class="form-group">
                    <label :for="_('h')">Height</label>
                    <input
                        class="form-control"
                        v-model.number="widget.h"
                        type="number"
                        :id="_('h')"
                        step="1"
                    />
                </div>
                <div class="form-group">
                    <label :for="_('font_size')">Font size</label>
                    <input
                        class="form-control"
                        v-model.number="widget.font_size"
                        type="number"
                        step="1"
                        :id="_('font_size')"
                        :min="
                            Context.settings.widget
                                ? Context.settings.widget.min_font_size
                                : 0
                        "
                        :max="
                            Context.settings.widget
                                ? Context.settings.widget.max_font_size
                                : 0
                        "
                    />
                </div>

                <div class="form-group">
                    <label :for="_('font_weight')">Font weight</label>
                    <input
                        class="form-control"
                        v-model.number="widget.font_weight"
                        type="number"
                        step="100"
                        :id="_('font_weight')"
                        :min="
                            Context.settings.widget
                                ? Context.settings.widget.min_font_weight
                                : 0
                        "
                        :max="
                            Context.settings.widget
                                ? Context.settings.widget.max_font_weight
                                : 0
                        "
                    />
                </div>

                <div class="form-group">
                    <label :for="_('background_color')">Background color</label>
                    <input
                        type="color"
                        v-model="widget.background_color"
                        class="form-control"
                    />
                </div>

                <div class="form-group">
                    <label :for="_('text_color')">Text color</label>
                    <input
                        type="color"
                        v-model="widget.text_color"
                        class="form-control"
                    />
                </div>
                <slot name="options"></slot>
                <div class="form-group d-flex justify-content-center">
                    <small class="text-secondary">All changes are automatically saved</small>
                </div>
            </div>
        </vue-draggable-resizable>
    </vue-draggable-resizable>
</template>

<script>
    // Front end is absolutely passive
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import {
        registerIdSystem,
        UpdateManager,
        API,
        Context,
    } from "../common.js";
    import $ from "jquery";

    Context.$on("addBlankWidget", function(klass) {
        Context.$emit("lockWidgetCreation");
        Context.$emit("routeRequest", ($route) => {
            new API(klass.type)
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
            Context.$on("closeWidgetOptions", this.onCloseOptions);
            Context.$on("widgetUpdatePosition", (wall) => {
                if (this.widget.x + this.widget.w >= wall.w) {
                    this.widget.x = wall.w - this.widget.w;
                }
                if (this.widget.y + this.widget.h >= wall.h) {
                    this.widget.y = wall.h - this.widget.h;
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
            var manager = new UpdateManager(
                this.widget.type,
                this.widget.id,
                this.unsetWarning,
                this.setWarningFromResponse
            );
            return {
                manager,
                Context,
                warningClass: "widget-options-warning", // Show warning messages
                quickAccessClass: "widget-quick-access",
                quickAccessVisible: false,
                optionsVisible: false,
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
            onOpenOptions() {
                this.optionsVisible = true;
            },
            onCloseOptions() {
                this.optionsVisible = false;
            },
            setWarningFromResponse(response) {
                this.unsetWarning();
                for (var [field, error] of Object.entries(
                    response.responseJSON
                )) {
                    $(`[for='${this._(field)}']`)
                        .addClass("text-danger")
                        .append(
                            $(`
                        <p class="${this.warningClass}"><small>${error[0]}</small></p>
                    `)
                        );
                }
            },
            unsetWarning() {
                $(`.${this.warningClass}`)
                    .parent()
                    .removeClass("text-dander");
                $(`.${this.warningClass}`).remove();
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
    .widget {
        margin: 0;
        padding: 0;
        border-style: solid;
        border-width: 1px;
        border-color: #dadada;
    }
    .control-area {
        width: 100%;
        height: 100%;
        position: absolute;
    }
    .widget-quick-access {
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
