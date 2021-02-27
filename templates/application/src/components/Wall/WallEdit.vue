<template>
    <div class="w-100 h-100 overflow-hidden">
        <div class="w-100 h-100 wall-container overflow-auto" @click.stop="Context.$emit('closeWidgetOptions')" v-if="dataReady">
            <vue-draggable-resizable
                @click.stop="Context.$emit('closeWidgetOptions')"
                @resizing="onResizing"
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
                <WidgetList :widgets="widgets" :base="WidgetBaseResizable"></WidgetList>
                <WidgetOptions></WidgetOptions>
            </vue-draggable-resizable>
            <span class="wall-title col-12 col-md-4 col-lg-3 p-0"><input @input="onWallTitleUpdate" class="form-control border-0" v-model="wall.title"/></span>
        </div>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import WidgetOptions from "../Widgets/WidgetOptions";
    import { Context, UpdateManager, API, WS } from "../../common.js";
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import $ from "jquery";
    import { deleteWall, updateWall } from "../../common.js";

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
            WidgetOptions,
        },
        data() {
            return {
                Context,
                WidgetBaseResizable,
                manager: undefined,
                ws: undefined,
                wall: undefined,
                widgets: undefined,
                dataReady: false,
            };
        },
        created() {
            Context.$on("widgetDeleted", this.onWidgetDeleted);
            Context.$on("widgetCreated", this.onWidgetCreated);
            Context.$on("deleteWall", this.onDeleteWall);
            this.initiateWall();
        },
        watch: {
            $route: "initiateWall",
            wall(newVal, oldVal) {
                if (newVal && oldVal && newVal.id == oldVal.id) this.manager.updated(newVal, oldVal);
            },
        },
        methods: {
            onResizing(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
                Context.$emit("widgetUpdatePosition", this.wall);
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
            initiateWall() {
                this.dataReady = false;
                this.wall = undefined;
                this.widgets = undefined;
                var manager = new UpdateManager("wall", this.$route.params.wallId);
                var ws = new WS("wall", this.$route.params.wallId);
                return manager.retrieve().then((response) => {
                    $(document).keyup(function(e) {
                        if (e.keyCode === 27) Context.$emit("closeWidgetOptions"); // esc
                    });
                    this.$set(this, "manager", manager);
                    this.$set(this, "ws", ws);
                    this.$set(this, "wall", response.wall);
                    this.$set(this, "widgets", response.widgets);
                    this.dataReady = true;
                });
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
