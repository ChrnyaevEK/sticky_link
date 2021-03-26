<template>
    <div class="w-100 h-100">
        <vue-draggable-resizable
            @click.native="$env.dispatch('closeOptions')"
            @touchstart.native="$env.dispatch('closeOptions')"
            @contextmenu.native.stop.prevent="$env.dispatch('openOptions', Object.assign({}, wall))"
            @resizestop="onResizeStop"
            @resizing="onResizing"
            :resizable="true"
            :draggable="false"
            :parent="false"
            :handles="['bm']"
            :h="wall.h"
            :minHeight="$store.state.settings.wall.min_height"
            class="border wall wall-only my-4"
        >
            <WidgetList :base="WidgetBaseResizable"></WidgetList>
        </vue-draggable-resizable>
        <Options></Options>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import Options from "../Utils/Options";
    import VueDraggableResizable from "vue-draggable-resizable";
    import $ from "jquery";

    export default {
        components: {
            VueDraggableResizable,
            WidgetList,
            Options,
        },
        async beforeRouteUpdate(to, from, next) {
            if (this.wall.lock_widgets) this.$env.dispatch("unlockWidgets");
            await this.$store.dispatch("fetchWidgets", to.params.wallId);
            next();
        },
        async beforeRouteLeave(to, from, next) {
            this.$env.dispatch("unlockWidgets");
            next();
        },
        created() {
            if (this.wall.lock_widgets) this.$env.dispatch("lockWidgets");
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
                return this.$store.state.walls.filter((w) => w.id == this.$route.params.wallId)[0];
            },
        },
        methods: {
            onResizeStop(x, y, w, h) {
                if (!this.$env.state.lockChanges) {
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.wall, { h }));
                }
            },
            onResizing(x, y, w, h) {
                if (!this.$env.state.lockChanges) {
                    this.$el.querySelector(".handle-bm").scrollIntoView({ behavior: "smooth", block: "center" });
                    this.$store.dispatch("recalculateWidgets", Object.assign({}, this.wall, { h }));
                }
            },
        },
        watch: {
            "wall.lock_widgets"() {
                this.$env.dispatch(this.wall.lock_widgets ? "lockWidgets" : "unlockWidgets");
            },
        },
    };
</script>

<style scoped>
    .wall {
        position: relative;
        width: 100% !important;
    }
</style>
