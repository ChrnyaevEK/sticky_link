<template>
    <div class="w-100 h-100 overflow-hidden">
        <div class="w-100 h-100 wall-container overflow-auto" @click.stop="Context.$emit('closeWidgetOptions')">
            <vue-draggable-resizable
                @click.native.stop
                @resizing="onResize"
                @resizestop="onResizeStop"
                :resizable="true"
                :draggable="true"
                :parent="false"
                :h="wall.h"
                :w="wall.w"
                :x="15"
                :y="15"
                :minWidth="Context.settings.wall ? Context.settings.wall.min_width : 50"
                :minHeight="Context.settings.wall ? Context.settings.wall.min_height : 50"
                class="border-secondary shadow"
            >
                <WidgetList v-if="ready" :widgets="widgets" :WidgetBase="WidgetBaseResizable"></WidgetList>
            </vue-draggable-resizable>
        </div>
        <span class="wall-title col-12 col-md-4 col-lg-3 p-0"><input @input="onWallTitleUpdate" class="form-control border-0" v-model="wall.title"/></span>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseResizable from '../Widgets/WidgetBaseResizable'
    import { API, Context, UpdateManager } from "../../common.js";
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import $ from "jquery";
    import { validateWall, deleteWall, updateWall } from "./wall.js";

    Context.$on("addBlankWall", () => {
        new API("wall").create().then((response) => {
            Context.walls.push(response);
            Context.$emit("wallCreated", response);
        });
    });

    export default {
        components: {
            VueDraggableResizable,
            WidgetList,
        },
        created() {
            $(document).keyup(function(e) {
                if (e.keyCode === 27) Context.$emit("closeWidgetOptions"); // esc
            });
            this.initiateWall(this.$route.params.wallId).then(() => {
                Context.$on("widgetDeleted", this.onWidgetDeleted);
                Context.$on("widgetCreated", this.onWidgetCreated);
                Context.$on("deleteWall", this.onDeleteWall);
            });
        },
        beforeRouteEnter(to, from, next) {
            if (validateWall(to.params.wallId)) {
                this.initiateWall(to.params.wallId).then(next);
            } else {
                next({
                    name: "app",
                });
            }
        },
        beforeRouteUpdate(to, from, next) {
            if (validateWall(to.params.wallId)) {
                this.initiateWall(to.params.wallId).then(next);
            } else {
                next({
                    name: "app",
                });
            }
        },
        data() {
            return {
                Context,
                manager: null,
                wall: null,
                widgets: null,
                ready: false,
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
                this.$set(this, "manager", new UpdateManager("wall", id));
                return this.manager.retrieve().then((response) => {
                    this.$set(this, "wall", response.wall);
                    this.$set(this, "widgets", response.widgets);
                });
            },
            onDeleteWall() {
                if (confirm("Are you sure? Wall will be permanently removed!")) {
                    deleteWall(this.wall.id);
                    this.manager.delete();
                    Context.$emit("wallDeleted", this.wall);
                }
            },
            onWallTitleUpdate() {
                updateWall(this.wall.id, { title: this.wall.title });
            },
            onWidgetCreated(widget) {
                this.widgets.push(widget);
            },
            onWidgetDeleted(widget) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
            },
        },
        watch: {
            wall: {
                handler() {
                    Context.$emit("widgetUpdatePosition", this.wall);
                    this.manager.updated(this.wall);
                },
                deep: true,
            },
        },
    };
</script>

<style scoped>
    .wall-container {
        position: relative;
    }
    .wall-alert,
    .wall-title {
        position: absolute;
        bottom: 0;
        left: auto;
    }
    .wall-title input {
        background-color: transparent;
    }
</style>
