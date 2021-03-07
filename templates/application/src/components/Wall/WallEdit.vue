<template>
    <div class="w-100 h-100 overflow-hidden">
        <div
            v-if="wall"
            class="w-100 h-100 wall-container overflow-auto"
            @click.stop="$env.dispatch('closeWidgetOptions')"
        >
            <vue-draggable-resizable
                @resizestop="onResizeStop"
                @resizing="onResizing"
                :resizable="true"
                :draggable="true"
                :parent="false"
                :h="wall.h"
                :w="wall.w"
                :x="15"
                :y="15"
                :minWidth="$store.state.settings.wall.min_width"
                :minHeight="$store.state.settings.wall.min_height"
                class="border border-muted shadow"
            >
                <WidgetList :base="WidgetBaseResizable"></WidgetList>
            </vue-draggable-resizable>
            <WidgetOptions></WidgetOptions>
            <span class="wall-title col-12 col-md-4 col-lg-3 p-0"
                ><input
                    @input="onWallTitleUpdate($event.target.value)"
                    class="form-control border-0"
                    :value="wall.title"
            /></span>
        </div>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import WidgetOptions from "../Widgets/WidgetOptions";
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import $ from "jquery";

    export default {
        components: {
            VueDraggableResizable,
            WidgetList,
            WidgetOptions,
        },
        created() {
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.dispatch("closeWidgetOptions"); // esc
            });
        },
        data() {
            return {
                WidgetBaseResizable,
            };
        },
        computed: {
            wall() {
                return this.$store.state.walls.filter(
                    (wall) => wall.id == this.$route.params.wallId
                )[0];
            },
        },
        methods: {
            onResizeStop(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
                this.$store.dispatch("updateWall", {
                    id: this.wall.id,
                    w,
                    h,
                });
                this.$store.dispatch("recalculateWidgets", this.wall);
            },
            onResizing(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
                this.$store.dispatch("recalculateWidgets", this.wall);
            },
            onWallTitleUpdate(value) {
                this.wall.title = value;
                this.$store.dispatch("updateWall", {
                    id: this.wall.id,
                    title: value,
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
