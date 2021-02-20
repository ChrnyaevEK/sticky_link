<template>
    <div class="w-100 h-100 d-flex flex-column overflow-hidden">
        <a id="side-top" class="btn btn-sm btn-light" @click="wall.h += 10">
            <i class="fas fa-plus"></i>
        </a>
        <div class="w-100 h-100 d-flex">
            <a
                id="side-left"
                class="btn btn-sm btn-light"
                @click="wall.w -= 10"
            >
                <i class="fas fa-minus"></i>
            </a>
            <div class="w-100 h-100 wall-container border overflow-auto">
                <vue-draggable-resizable
                    @click="Context.$emit('closeWidgetOptions')"
                    @resizing="onResize"
                    @resizestop="onResizeStop"
                    :resizable="true"
                    :draggable="true"
                    :parent="false"
                    :h="wall.h"
                    :w="wall.w"
                >
                    <div v-if="staticSize" class="w-100 h-100">
                        <SimpleText
                            v-for="widget of filterWidgets(SimpleText)"
                            :key="widget.type + widget.id"
                            :parent="true"
                            :widget="widget"
                        >
                        </SimpleText>
                        <URL
                            v-for="widget of filterWidgets(URL)"
                            :key="widget.type + widget.id"
                            :widget="widget"
                        >
                        </URL>
                        <Counter
                            v-for="widget of filterWidgets(Counter)"
                            :key="widget.type + widget.id"
                            :widget="widget"
                        >
                        </Counter>
                        <SimpleList
                            v-for="widget of filterWidgets(SimpleList)"
                            :key="widget.type + widget.id"
                            :widget="widget"
                        >
                        </SimpleList>
                    </div>
                </vue-draggable-resizable>
            </div>
            <a
                id="side-right"
                class="btn btn-sm btn-light"
                @click="wall.w += 10"
            >
                <i class="fas fa-plus"></i>
            </a>
        </div>
        <a id="side-bottom" class="btn btn-sm btn-light" @click="wall.h -= 10">
            <i class="fas fa-minus"></i>
        </a>
    </div>
</template>

<script>
    import SimpleText from "./Widgets/SimpleText";
    import URL from "./Widgets/URL";
    import Counter from "./Widgets/Counter";
    import SimpleList from "./Widgets/SimpleList";
    import { API, Context, UpdateManager } from "../common.js";
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";

    Context.$on("addBlankWall", () => {
        new API("wall").create().then((response) => {
            Context.$emit("wallCreated", response);
        });
    });

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
        VueDraggableResizable,
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
                blockUpdate: false,
                staticSize: true,
                ...components,
            };
        },
        methods: {
            onResize(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
            },
            onResizeStop() {
                this.staticSize = false;
                Context.$emit('widgetUpdatePosition', this.wall)
                this.$nextTick(()=>{
                    this.staticSize = true;
                })
            },
            initiateWall(id) {
                this.blockUpdate = true;
                this.$set(this, "manager", new UpdateManager("wall", id));
                this.manager.retrieve().then((response) => {
                    this.$set(this, "wall", response.wall);
                    this.$set(this, "widgets", response.widgets);
                    this.$nextTick(() => {
                        this.blockUpdate = false;
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
            filterWidgets(klass) {
                return this.widgets.filter(function(widget) {
                    return widget.type == klass.type;
                });
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
                    if (!this.blockUpdate) {
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
    #side-top,
    #side-bottom,
    #side-right,
    #side-left {
        width: 0;
        height: 0;
        display: flex;
    }
    #side-top,
    #side-bottom {
        justify-content: center;
        height: auto;
        width: 100%;
    }
    #side-left,
    #side-right {
        align-items: center;
        width: auto;
        height: 100%;
    }
    .wall-container {
        position: relative;
    }
</style>
