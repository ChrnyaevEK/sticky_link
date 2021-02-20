<template>
    <vue-draggable-resizable
        @resizing="onResize"
        @dragging="onDrag"
        @mousedown.native.stop.prevent
        @mouseup.native.stop.prevent
        @mousemove.native.stop.prevent
        @click.native.stop.prevent
        class="widget"
        :parent="true"
        :w="widget.w"
        :h="widget.h"
        :y="widget.y"
        :x="widget.x"
        :z="widget.z"
    >
        <div class="widget-quick-access" v-show="quickAccessVisible">
            <a class="widget-drag btn btn-light border" @click="copyWidget"
                ><i class="fas fa-copy"></i
            ></a>
            <a class="widget-drag btn btn-danger" @click="deleteWidget"
                ><i class="fas fa-trash"></i
            ></a>
        </div>
        <div
            class="w-100 h-100"
            :style="style"
            @contextmenu.stop.prevent="optionsVisible = true"
        >
            <slot name="content"></slot>
        </div>
        <vue-draggable-resizable
            v-if="optionsVisible"
            @mousedown.native.stop.prevent
            @mouseup.native.stop.prevent
            @mousemove.native.stop.prevent
            @click.native.stop.prevent
            :w="400"
            :h="600"
            :resizable="false"
            :parent="false"
            class="bg-white widget-options border border-secondary rounded"
        >
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
    } from "../../common.js";
    import $ from "jquery";

    Context.$on("addBlankWidget", function(klass) {
        Context.$emit("routeRequest", ($route) => {
            new API(klass.type)
                .create({ wall: $route.params.wall_id })
                .then((response) => {
                    Context.$emit("widgetCreated", response);
                });
        });
    });

    export default {
        name: "WidgetBase",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        data: function() {
            registerIdSystem(this, this.widget); // Create _ function to generate ids
            Context.$on("closeWidgetOptions", () => {
                this.optionsVisible = false;
            });
            Context.$on('widgetUpdatePosition', (wall)=>{
                if (this.widget.x + this.widget.w >= wall.w ) {
                    this.widget.x = wall.w - this.widget.w
                }
                if (this.widget.y + this.widget.h >= wall.h ) {
                    this.widget.y = wall.h - this.widget.h
                }
            })
            var vm = this;
            return {
                manager: new UpdateManager(
                    vm.widget.type,
                    vm.widget.id,
                    this.unsetWarning,
                    this.setWarningFromResponse
                ),
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
            setWarningFromResponse(response) {
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
                    this.manager.delete().then(() => {
                        Context.$emit("widgetDeleted", this.widget);
                    });
                }
            },
            copyWidget() {
                this.manager.create(this.widget);
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
        width: 100%;
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
