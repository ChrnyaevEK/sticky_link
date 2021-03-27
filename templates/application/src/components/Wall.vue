<template>
    <div class="w-100 h-100 py-5 overflow-auto" v-if="$store.state.wall">
        <vue-draggable-resizable
            @click.native="$env.closeOptions"
            @touchstart.native="$env.closeOptions"
            @contextmenu.native.stop.prevent="$env.openOptions(Object.assign({}, $store.state.wall))"
            @resizing="onResizing"
            v-for="container of containers"
            @activated="selectContainer(container)"
            :key="container.id"
            :resizable="true"
            :draggable="false"
            :parent="false"
            :handles="['bm']"
            :h="container.h"
            :minHeight="100"
            class="border wall wall-only my-3"
        >
            <component
                v-for="widget of filterWidgets(container)"
                :is="toComponent(widget)"
                :parent="true"
                :key="widget.type + widget.id"
                :widget="widget"
            >
            </component>
        </vue-draggable-resizable>
        <Options></Options>
    </div>
    <div v-else class="w-100 h-100 d-flex justify-content-center align-items-center text-secondary">
        <span v-if="$store.state.user.is_authenticated">No wall is selected...</span>
        <span v-else
            >No wall is available...
            <router-link class="text-success font-weight-bold" :to="{ name: 'login' }">Login</router-link> to
            continue</span
        >
    </div>
</template>

<script>
    import SimpleText from "./Widgets/SimpleText";
    import URL from "./Widgets/URL";
    import Counter from "./Widgets/Counter";
    import SimpleList from "./Widgets/SimpleList";
    import SimpleSwitch from "./Widgets/SimpleSwitch";

    import Options from "./Utils/Options";

    import VueDraggableResizable from "vue-draggable-resizable";
    import $ from "jquery";

    export default {
        components: {
            VueDraggableResizable,
            Options,
        },
        beforeRouteLeave(to, from, next) {
            this.$env.unlockWidgets();
            next();
        },
        created() {
            if (this.wall && this.wall.lock_widgets) this.$env.lockWidgets();
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.closeOptions(); // esc
            });
        },
        computed: {
            wall() {
                return this.$store.state.wall;
            },
            containers() {
                return this.$store.state.containers ? this.$store.state.containers : [this.$store.state.container];
            },
        },
        methods: {
            onResizing(x, y, w, h) {
                if (!this.$env.changesLocked && this.$store.state.container) {
                    this.$el.querySelector(".handle-bm").scrollIntoView({ behavior: "auto", block: "end" });
                    var update = Object.assign({}, this.$store.state.container, { h });
                    this.$store.dispatch("recalculateWidgets", update);
                    this.$store.dispatch("updateOrAddInstance", update);
                }
            },
            toComponent(widget) {
                return [SimpleText, URL, Counter, SimpleList, SimpleSwitch].filter(
                    (klass) => widget.type == klass.type
                )[0];
            },
            filterWidgets(container) {
                if (this.$store.state.widgets) {
                    var widgets = [];
                    for (var widget of this.$store.state.widgets) {
                        if (widget.container == container.id) {
                            widgets.push(widget);
                        }
                    }
                    return widgets;
                } else {
                    return [];
                }
            },
            selectContainer(container) {
                this.$store.commit("setContainer", container);
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
