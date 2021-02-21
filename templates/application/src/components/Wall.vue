<template>
    <div class="w-100 h-100">
        <div
            v-if="$route.query.mode == Context.edit"
            class="w-100 h-100 overflow-hidden"
        >
            <div
                class="w-100 h-100 wall-container overflow-auto"
                @click.stop="Context.$emit('closeWidgetOptions')"
            >
                <vue-draggable-resizable
                    @click.native.stop.prevent
                    @resizing="onResize"
                    @resizestop="onResizeStop"
                    :resizable="true"
                    :draggable="true"
                    :parent="false"
                    :h="wall.h"
                    :w="wall.w"
                    :x="15"
                    :y="15"
                    class="border border-secondary"
                >
                    <WidgetList v-if="ready" :widgets="widgets"></WidgetList>
                </vue-draggable-resizable>
            </div>
            <span class="wall-title col-12 col-md-4 col-lg-3 p-0"
                ><input
                    type="text"
                    class="form-control border-0"
                    v-model="wall.title"
            /></span>
        </div>
        <div v-if="$route.query.mode == Context.view">
            <WidgetList :widgets="widgets"></WidgetList>
            <span class="wall-title col-12 col-md-4 col-lg-3">
                <span class="font-weight-bold text-primary">{{ wall.title }}</span>
            </span>
        </div>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import { API, Context, UpdateManager } from "../common.js";
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";

    Context.$on("addBlankWall", () => {
        new API("wall").create().then((response) => {
            Context.$emit("wallCreated", response);
        });
    });

    var components = {
        VueDraggableResizable,
        WidgetList,
    };

    export default {
        components,
        created() {
            Context.$on("widgetDeleted", this.onWidgetDeleted);
            Context.$on("widgetCreated", this.onWidgetCreated);
            this.initiateWall(this.$route.params.wallId);
        },
        data() {
            return {
                Context,
                manager: {},
                wall: {},
                widgets: [],
                ready: true,
                ...components,
            };
        },
        methods: {
            onResize(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
            },
            onResizeStop() {
                this.ready = false;
                this.$nextTick(() => {
                    this.ready = true;
                });
            },
            initiateWall(id) {
                this.ready = false;
                this.$set(this, "manager", new UpdateManager("wall", id));
                this.manager.retrieve().then((response) => {
                    this.$set(this, "wall", response.wall);
                    this.$set(this, "widgets", response.widgets);
                    this.$nextTick(() => {
                        this.ready = true;
                    });
                });
            },
            onDeleteWall() {
                if (
                    confirm("Are you sure? Wall will be permanently removed!")
                ) {
                    this.manager.delete();
                    Context.$emit("wallDeleted", this.wall);
                }
            },
            onWidgetCreated(widget) {
                this.widgets.push(widget);
            },
            onWidgetDeleted(widget) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
            },
        },
        watch: {
            $route(to) {
                this.initiateWall(to.params.wallId);
            },
            wall: {
                handler() {
                    if (this.ready) {
                        Context.$emit("widgetUpdatePosition", this.wall);
                        this.manager.updated(this.wall);
                    }
                },
                deep: true,
            },
        },
        computed: {
            style() {
                return `
                    min-width: ${
                        Context.settings.wall
                            ? Context.settings.wall.min_width
                            : 0
                    }px;
                    min-height: ${
                        Context.settings.wall
                            ? Context.settings.wall.min_height
                            : 0
                    }px;
                `;
            },
        },
    };
</script>

<style scoped>
    .wall-container {
        position: relative;
    }
    .wall-title {
        position: absolute;
        bottom: 0;
    }
</style>
