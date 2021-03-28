<template>
    <div class="w-100 h-100 py-5 overflow-auto" v-if="$store.state.wall">
        <div class="d-flex flex-column relative m-1" v-for="container of containers" :key="container.id">
            <div
                :id="_(container.id)"
                class="overflow-auto border container-wrap scrollbar-hidden scrollable-element relative bottom-element"
            >
                <vue-draggable-resizable
                    @click.native.stop.prevent="onCloseOptions"
                    @touchstart.native.stop.prevent="onCloseOptions"
                    @resizing="onResizing"
                    @activated="onActivated(container)"
                    :resizable="$env.edit"
                    :draggable="false"
                    :parent="false"
                    :handles="['bm']"
                    :h="container.h"
                    :w="container.w"
                    :minHeight="100"
                    class="relative wall-only no-border"
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
            </div>
            <div class="quick-access container-quick-access hidden p-1" v-if="$env.edit">
                <a class="btn btn-sm btn-light border" @click.stop="$env.openOptions(Object.assign({}, container))">
                    <i class="fas fa-ellipsis-v"></i>
                </a>
            </div>
        </div>
        <Options v-if="$env.edit"></Options>
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
                if (!this.$env.changesLocked && this.$env.edit && this.$store.state.container) {
                    this.$el.querySelector(".handle-bm").scrollIntoView({ behavior: "smooth", block: "center" });
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
            onCloseOptions() {
                if (this.$env.edit) {
                    this.$env.closeOptions();
                }
            },
            onActivated(container) {
                if (this.$env.edit) {
                    window.dispatchEvent(new Event("resize"));
                    var containerId = "#" + this._(container.id);
                    $(".container-wrap")
                        .addClass("scrollbar-hidden")
                        .removeClass("shadow-sm");
                    $(containerId).addClass("shadow-sm");
                    $(".quick-access")
                        .not(`${containerId} .quick-access`)
                        .addClass("hidden");
                    $(containerId)
                        .removeClass("scrollbar-hidden")
                        .parent()
                        .find(".container-quick-access")
                        .removeClass("hidden");
                    this.$store.commit("setContainer", container);
                }
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
    .relative {
        position: relative;
    }
    .container-quick-access {
        position: absolute;
        display: flex;
        right: 0px;
    }
    .container-quick-access > * {
        margin: 0 0 0 2px;
        height: 2rem;
        width: 2rem;
    }
    .bottom-element {
        padding-bottom: 6px;
    }
</style>
