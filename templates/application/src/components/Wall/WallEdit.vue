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
            <div class="wall-edit px-1">
                <input v-model="wall.title" class="form-control border-0 px-1" />
            </div>
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
        beforeRouteUpdate(to, from, next) {
            this.$store.dispatch("fetchWidgets", to.params.wallId).then(next);
        },
        created() {
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.dispatch("closeWidgetOptions"); // esc
            });
        },
        data() {
            return {
                WidgetBaseResizable,
                wall: this.$store.state.walls.filter((wall) => wall.id == this.$route.params.wallId)[0],
            };
        },

        methods: {
            onResizeStop(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
            },
            onResizing(x, y, w, h) {
                this.wall.w = w;
                this.wall.h = h;
            },
        },
        watch: {
            wall: {
                handler() {
                    if (!this.$env.state.lockChanges) {
                        this.$store.dispatch("updateOrAddInstance", this.wall);
                        this.$store.dispatch("recalculateWidgets", this.wall);
                    }
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
    .wall-edit {
        position: absolute;
        bottom: 0;
        left: auto;
    }
    .wall-edit input {
        background-color: transparent;
    }
</style>
