<template>
    <div
        class="w-100 h-100"
        @click.native="$env.dispatch('closeOptions')"
        @touchstart.native="$env.dispatch('closeOptions')"
        @contextmenu.native.stop.prevent="$env.dispatch('openOptions', Object.assign({}, wall))"
    >
        <vue-draggable-resizable
            v-for="containser of widgetContainers"
            @resizing="onResizing"
            :resizable="true"
            :draggable="false"
            :parent="false"
            :handles="['bm']"
            :minHeight="100"
            :h="100"
            class="border wall wall-only my-4"
        >
            <component
                v-for="widget of container"
                :is="toComponent(widget)"
                :parent="true"
                :base="WidgetBaseResizable"
                :key="widget.type + widget.id"
                :widget="widget"
            >
            </component>
        </vue-draggable-resizable>
        <Options></Options>
    </div>
</template>

<script>
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";
    import SimpleSwitch from "../Widgets/SimpleSwitch";

    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";
    import Options from "../Utils/Options";

    import VueDraggableResizable from "vue-draggable-resizable";
    import { DefaultDict } from "../../common";
    import $ from "jquery";

    export default {
        components: {
            VueDraggableResizable,
            WidgetList,
            Options,
        },
        async beforeRouteUpdate(to, from, next) {
            if (this.wall.lock_widgets) await this.$env.dispatch("unlockWidgets");
            await this.$store.dispatch("fetchWidgets", to.params.wallId);
            next();
        },
        async beforeRouteLeave(to, from, next) {
            await this.$env.dispatch("unlockWidgets");
            next();
        },
        created() {
            if (this.wall.lock_widgets) this.$env.dispatch("lockWidgets");
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.dispatch("closeOptions"); // esc
            });
        },
        data() {
            var wall = this.$store.state.walls.filter((w) => w.id == this.$route.params.wallId)[0];
            var groups = new DefaultDict(() => []);
            for (let widget of this.$store.state.widgets) {
                groups[widget.container].push(widget);
            }
            var widgetContainers = Object.values(groups);
            return {
                WidgetBaseResizable,
                widgetContainers,
                wall,
            };
        },
        methods: {
            onResizing(x, y, w, h) {
                if (!this.$env.state.lockChanges) {
                    this.$el.querySelector(".handle-bm").scrollIntoView({ behavior: "smooth", block: "center" });
                    this.$store.dispatch("recalculateWidgets", Object.assign({}, this.wall, { h }));
                }
            },
            toComponent(widget) {
                return [SimpleText, URL, Counter, SimpleList, SimpleSwitch].filter(
                    (klass) => widget.type == klass.type
                )[0];
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
