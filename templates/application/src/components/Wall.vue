<template>
    <div
        class="w-100 h-100"
        @click.native="$env.closeOptions"
        @touchstart.native="$env.closeOptions"
        @contextmenu.native.stop.prevent="$env.openOptions(Object.assign({}, $store.state.wall))"
    >
        <vue-draggable-resizable
            v-if="$store.state.wall"
            v-for="containser of widgetContainers"
            @resizing="onResizing"
            :resizable="true"
            :draggable="false"
            :parent="false"
            :handles="['bm']"
            :minHeight="100"
            class="border wall wall-only my-4"
        >
            <component
                v-for="widget of container"
                :is="toComponent(widget)"
                :parent="true"
                :key="widget.type + widget.id"
                :widget="widget"
            >
            </component>
        </vue-draggable-resizable>
        <div v-else>
            <span v-if="$store.state.user.is_authenticated">No wall is selected...</span>
            <span v-else>No wall is available...</span>
        </div>
        <Options v-if="$store.state.wall"></Options>
    </div>
</template>

<script>
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";
    import SimpleSwitch from "../Widgets/SimpleSwitch";

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
            if (this.wall.lock_widgets) await this.$env.unlockWidgets();
            await this.$store.dispatch("fetchState", to.params.wallId);
            next();
        },
        async beforeRouteLeave(to, from, next) {
            await this.$env.unlockWidgets();
            next();
        },
        created() {
            if (this.wall.lock_widgets) this.$env.lockWidgets();
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.closeOptions(); // esc
            });
        },
        computed: {
            wall() {
                return this.$store.state.walls.filter((w) => w.id == this.$route.params.wallId)[0];
            },
            widgetContainers() {
                var groups = new DefaultDict(() => []);
                for (let widget of this.$store.state.widgets) {
                    groups[widget.container].push(widget);
                }
                return Object.values(groups);
            },
        },
        methods: {
            onResizing(x, y, w, h) {
                if (!this.$env.lockChanges) {
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
                this.wall.lock_widgets ? this.$env.lockWidgets() : this.$env.unlockWidgets();
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
