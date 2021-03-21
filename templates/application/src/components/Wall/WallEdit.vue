<template>
    <div class="w-100 h-100 overflow-hidden">
        <div class="w-100 h-100 wall-container overflow-auto" @click.stop="$env.dispatch('closeOptions')">
            <vue-draggable-resizable
                @contextmenu.native.stop.prevent="$env.dispatch('openOptions', Object.assign({}, wall))"
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
            <Options></Options>
            <div class="wall-edit px-2">
                {{ wall.title }}
            </div>
        </div>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import Options from "../Utils/Options";
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import $ from "jquery";
    import { deepCopy } from "../../common";

    export default {
        components: {
            VueDraggableResizable,
            WidgetList,
            Options,
        },
        beforeRouteUpdate(to, from, next) {
            this.$store.dispatch("fetchWidgets", to.params.wallId).then(next);
        },
        created() {
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.dispatch("closeOptions"); // esc
            });
        },
        data() {
            return {
                WidgetBaseResizable,
            };
        },
        computed: {
            wall() {
                return this.$store.state.walls.filter((wall) => wall.id == this.$route.params.wallId)[0];
            },
        },
        methods: {
            deepCopy: deepCopy,
            onResizeStop(x, y, w, h) {
                if (!this.$env.state.lockChanges) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.wall, { x, y, w, h }));
                }
            },
            onResizing(x, y, w, h) {
                if (!this.$env.state.lockChanges) {
                    this.$store.dispatch("recalculateWidgets", Object.assign({}, this.wall, { w, h }));
                }
            },
        },
    };
</script>

<style scoped>
    .centered {
        display: flex;
        justify-content: center;
    }
    .wall-container {
        position: relative;
    }
    .wall-edit {
        position: absolute;
        bottom: 0;
        left: 0;
    }
    .wall-edit input {
        background-color: transparent;
    }
</style>
