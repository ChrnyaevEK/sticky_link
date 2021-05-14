<template>
    <div class="h-100 bg-light d-flex flex-column justify-content-between align-items-center overflow-hidden p-1">
        <div class="w-100 w-100" v-if="$env.state.wall">
            <div class="w-100 text-nowrap overflow-hidden">
                <span v-if="$env.state.wall.title">{{ $env.state.wall.title }}</span>
                <small v-if="$env.state.wall.description" class="mx-1">{{ $env.state.wall.description }}</small>
            </div>
            <div
                class="w-100 h-100 py-1 overflow-auto pb-5"
                @click="
                    unsetWidgetSelection();
                    $env.dispatch('closeOptions');
                "
            >
                <div
                    class="d-flex flex-column relative py-1"
                    v-for="container of $store.state.containers"
                    :key="container.id"
                >
                    <div class="w-100 text-nowrap text-secondary overflow-hidden">
                        <span v-if="container.title">{{ container.title }}</span>
                        <small v-if="container.description" class="mx-1">{{ container.description }}</small>
                    </div>
                    <div
                        v-scope:id="container.id"
                        class="overflow-auto border container-wrap scrollable-element relative bg-white"
                    >
                        <vue-draggable-resizable
                            @click.native.stop="$env.dispatch('closeOptions')"
                            @touchstart.native="$env.dispatch('closeOptions')"
                            @resizing="onResizing"
                            @activated="onActivated(container)"
                            :resizable="$env.state.editMode && !$env.state.changesLock"
                            :draggable="false"
                            :parent="false"
                            :handles="['bm']"
                            :h="container.h"
                            :w="container.w"
                            :minHeight="100"
                            class="relative overflow-hidden wall-only no-border"
                            style="touch-action: initial;"
                            :grid="[$store.state.app.grid, $store.state.app.grid]"
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
                    <div
                        class="quick-access container-quick-access hidden p-1"
                        :class="{ 'container-title-offset': container.title }"
                        v-if="$env.state.editMode"
                    >
                        <button
                            class="btn btn-sm btn-light border"
                            @click.stop="$env.dispatch('openOptions', container)"
                            :disabled="$env.state.changesLock"
                        >
                            <i class="fas fa-ellipsis-v"></i>
                        </button>
                    </div>
                </div>
                <Options v-if="$env.state.editMode"></Options>
            </div>
        </div>
        <div v-else class="w-100 h-100 d-flex justify-content-center align-items-center text-secondary">
            <span v-if="$store.state.user.is_authenticated">No wall is selected...</span>
            <span v-else>No wall is available... Login to continue</span>
        </div>

        <div
            v-if="$env.state.editMode && $store.state.user.is_authenticated"
            class="p-1 w-100 shadow d-flex justify-content-between border bg-white"
        >
            <div class="btn-group dropup">
                <div v-if="$store.state.walls">
                    <a
                        class="btn btn-sm dropdown-toggle"
                        id="wall-list"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                        title="Select wall to edit"
                    >
                        Walls
                    </a>
                    <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                        <router-link
                            class="dropdown-item btn btn-sm"
                            v-for="wall of $store.state.walls"
                            :key="wall.id"
                            :class="{ active: wall.id == $route.params.wallId }"
                            :to="{
                                name: 'wallEdit',
                                params: { wallId: wall.id },
                            }"
                            >{{ wall.title }}</router-link
                        >
                    </div>
                </div>
                <button
                    class="mr-1 btn btn-sm btn-success text-white border"
                    @click="createWall"
                    title="Add new wall"
                    :disabled="$env.state.changesLock"
                >
                    <i class="fas fa-plus"></i>
                </button>
                <button
                    v-if="$env.state.wall"
                    class="mr-1 btn btn-sm btn-default"
                    @click.stop="$env.dispatch('openOptions', $env.state.wall)"
                    :disabled="$env.state.changesLock"
                >
                    <i class="fas fa-ellipsis-v"></i>
                </button>
                <div v-if="$store.state.ports && $env.state.wall">
                    <a
                        class="btn btn-sm dropdown-toggle"
                        id="wall-list"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                        title="Select port to edit"
                    >
                        Ports
                    </a>
                    <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                        <a
                            class="dropdown-item btn btn-sm"
                            v-for="port of $store.state.ports"
                            :key="port.id"
                            @click="$env.dispatch('openOptions', port)"
                            :title="'Visit counter: ' + port.visited"
                            >{{ port.title }} <small>{{ port.visited }}</small>
                        </a>
                    </div>
                </div>
                <button
                    v-if="$store.state.ports && $env.state.wall"
                    class="mr-1 btn btn-sm btn-success text-white border"
                    @click="createInstance('port')"
                    title="Add new port"
                    :disabled="$env.state.changesLock"
                >
                    <i class="fas fa-plus"></i>
                </button>
            </div>
            <span class="overflow-auto scrollbar-hidden d-flex" v-if="$env.state.wall">
                <button
                    @click.stop="createInstance('container')"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add Container to hold widgets"
                    :disabled="$env.state.changesLock"
                >
                    Container
                </button>
                <button
                    @click.stop="createInstance('simple_text')"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Simple text"
                    :disabled="$env.state.changesLock"
                >
                    Text
                </button>
                <button
                    @click.stop="createInstance('url')"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type URL"
                    :disabled="$env.state.changesLock"
                >
                    URL
                </button>
                <button
                    @click.stop="createInstance('counter')"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Counter"
                    :disabled="$env.state.changesLock"
                >
                    Counter
                </button>
                <button
                    @click.stop="createInstance('simple_list')"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Simple list"
                    :disabled="$env.state.changesLock"
                >
                    List
                </button>
                <button
                    @click.stop="createInstance('simple_switch')"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Switch"
                    :disabled="$env.state.changesLock"
                >
                    Switch
                </button>
            </span>
        </div>
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

    import router from "../modules/router";
    import store from "../modules/store";
    import env from "../modules/env";

    async function setupRoutine(to, from, next) {
        await env.dispatch("closeOptions");
        await env.dispatch("setWallByWallId", to.params.wallId);
        if (store.state.containers) {
            let container = store.state.containers[0];
            if (container) {
                await env.dispatch("setContainerByContainerId", container.id);
            }
        }
        next();
    }

    export default {
        name: 'Wall',
        components: {
            VueDraggableResizable,
            Options,
        },
        beforeRouteEnter: setupRoutine,
        beforeRouteUpdate: setupRoutine,
        methods: {
            onResizing(x, y, w, h) {
                let instance = Object.assign({}, this.$env.state.container, { h });
                this.$store.dispatch("recalculateWidgets", instance);
                this.$store.dispatch("updateOrAddInstance", instance);
            },
            toComponent(widget) {
                return [SimpleText, URL, Counter, SimpleList, SimpleSwitch].filter(
                    (klass) => widget.type == klass.type
                )[0];
            },
            onActivated(container) {
                this.$env.dispatch("setContainerByContainerId", container.id);
                window.dispatchEvent(new Event("resize"));

                let containerId = "#" + this._(container.id);
                container = $(containerId);

                if (this.$env.state.editMode) {
                    $(".quick-access")
                        .not(`${containerId} .quick-access`)
                        .addClass("hidden");
                    container
                        .parent()
                        .find(".container-quick-access")
                        .removeClass("hidden");
                }
            },
            unsetWidgetSelection() {
                $(".quick-access").addClass("hidden");
            },
            async createInstance(type) {
                if (type == "container") {
                    let index = 0;
                    for (let container of this.$store.state.containers) {
                        if (container.index > index) {
                            index = container.index + 1;
                        }
                    }
                    await this.$store.dispatch("createInstance", {
                        type,
                        index,
                        wall: this.$env.state.wall.id,
                    });
                } else if (type == "port") {
                    let port = await this.$store.dispatch("createInstance", {
                        type: "port",
                        wall: this.$env.state.wall.id,
                    });
                    this.$env.dispatch("openOptions", port);
                } else {
                    await this.$store.dispatch("createInstance", { type, container: this.$env.state.container.id });
                    this.$store.dispatch("recalculateWidgets", this.$env.state.container);
                }
            },
            async createWall() {
                let wall = await this.$store.dispatch("createInstance", { type: "wall" });
                this.$notify({
                    text: "New wall has been created!",
                    type: "success",
                });
                router.push({
                    name: "wallEdit",
                    params: {
                        wallId: wall.id,
                    },
                });
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
    .select-create-pos {
        position: absolute;
        bottom: 0;
    }
    .container-title-offset {
        margin-top: 1.5rem;
    }
</style>
