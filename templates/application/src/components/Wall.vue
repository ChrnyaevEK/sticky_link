<template>
    <div class="w-100 h-100 py-1 overflow-auto pb-5" v-if="$store.state.wall">
        <div
            class="d-flex flex-column relative m-1 bg-white"
            v-for="container of $store.state.containers"
            :key="container.id"
        >
            <div
                :id="_(container.id)"
                class="overflow-auto border container-wrap scrollbar-hidden scrollable-element relative"
            >
                <vue-draggable-resizable
                    @click.native.stop="$env.closeOptions"
                    @touchstart.native.stop="$env.closeOptions"
                    @resizing="onResizing"
                    @activated="onActivated(container)"
                    @deactivated="onDeactivated"
                    :resizable="$env.edit && !$env.changesLocked"
                    :draggable="false"
                    :parent="false"
                    :handles="['bm']"
                    :h="container.h"
                    :w="container.w"
                    :minHeight="100"
                    class="relative overflow-hidden wall-only no-border"
                >
                    <template v-for="widget of $store.state.widgets">
                        <component
                            v-if="widget.container == container.id"
                            :is="toComponent(widget)"
                            :key="widget.type + widget.id"
                            :widget="widget"
                        >
                        </component>
                    </template>
                </vue-draggable-resizable>
            </div>
            <div class="quick-access container-quick-access hidden p-1" v-if="$env.edit">
                <a class="btn btn-sm btn-light border" @click.stop="$env.openOptions(container)">
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
        async beforeRouteLeave(to, from, next) {
            await this.$env.unlockWidgets();
            next();
        },
        computed: {
            wall() {
                let wall = this.$store.state.wall;
                if (wall && wall.lock_widgets) this.$env.lockWidgets();
                return wall;
            },
        },
        methods: {
            onResizing(x, y, w, h) {
                this.$el.querySelector(".handle-bm").scrollIntoView({ behavior: "smooth", block: "center" });
                let instance = this.$env.makeMutable(this.$store.state.container, { h });
                this.$store.dispatch("recalculateWidgets", instance);
                this.$store.dispatch("updateOrAddInstance", instance);
            },
            toComponent(widget) {
                return [SimpleText, URL, Counter, SimpleList, SimpleSwitch].filter(
                    (klass) => widget.type == klass.type
                )[0];
            },
            onActivated(container) {
                if (this.$env.edit) {
                    // Add scroll bar, hide previous active element
                    window.dispatchEvent(new Event("resize"));
                    let containerId = "#" + this._(container.id);
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
            onDeactivated() {
                window.dispatchEvent(new Event("resize"));
                $(this.$el)
                    .find(".container-wrap")
                    .addClass("scrollbar-hidden");
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
</style>
