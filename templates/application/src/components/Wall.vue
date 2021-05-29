<template>
    <div class="d-flex flex-grow-1 h-100 overflow-hidden">
        <div class="w-75 d-flex flex-column flex-grow-1 overflow-auto">
            <!-- Wall title -->
            <div class="d-flex justify-content-between px-2 align-items-center">
                <span
                    v-if="$env.state.wall"
                    class="overflow-hidden"
                    :class="$env.state.editMode ? 'text-truncate' : 'text-break'"
                >
                    <span v-show="$env.state.editMode" class="mr-2">Wall</span
                    ><strong class="mr-1 text-primary" :title="$env.state.wall.title">{{
                        $env.state.wall.title
                    }}</strong>
                    <span class="text-secondary" :title="$env.state.wall.description">{{
                        $env.state.wall.description
                    }}</span>
                </span>
                <button
                    v-if="$env.state.wall && $env.state.editMode"
                    class="btn btn-sm bg-white"
                    @click.stop="$env.dispatch('openOptions', $env.state.wall)"
                    :disabled="$env.state.changesLock"
                >
                    <i class="fas fa-ellipsis-v"></i>
                </button>
            </div>
            <!-- Container section -->
            <div class="flex-grow-1">
                <div v-if="$env.state.wall">
                    <div class="d-flex flex-column" v-for="container of $store.state.containers" :key="container.id">
                        <div class="overflow-auto">
                            <vue-draggable-resizable
                                @resizing="handleContainerResizing"
                                @activated="handleContainerActivated(container)"
                                :resizable="$env.state.editMode && !$env.state.changesLock"
                                :draggable="false"
                                :parent="false"
                                :handles="['bm']"
                                :h="container.h"
                                :w="container.w"
                                :minHeight="100"
                                class="position-relative wall-only no-border"
                                :class="{ grid: $env.state.editMode }"
                                style="touch-action: initial;"
                                :grid="[$store.state.app.grid, $store.state.app.grid]"
                            >
                                <template v-for="widget of $store.state.widgets">
                                    <component
                                        v-if="widget.container == container.id"
                                        :is="getComponent(widget)"
                                        :key="widget.type + widget.id"
                                        :widget="widget"
                                    >
                                    </component>
                                </template>
                            </vue-draggable-resizable>
                        </div>
                        <div class="px-2 my-1 d-flex align-items-center">
                            <div class="mr-1" :class="$env.state.editMode ? 'text-truncate' : 'text-break'">
                                <span v-show="$env.state.editMode" class="mr-2">Container</span
                                ><strong class="mr-1 text-primary">{{ container.title }}</strong>
                                <span class="text-secondary">{{ container.description }}</span>
                            </div>
                            <div
                                v-if="$env.state.editMode"
                                class="flex-grow-1 d-flex justify-content-end align-items-center"
                            >
                                <span class="mr-2 text-nowrap">Available widgets</span>
                                <button
                                    @click.stop="
                                        handleContainerActivated(container);
                                        $env.dispatch('handleCreateWidget', 'simple_text');
                                    "
                                    class="mr-1 btn btn-sm bg-white border text-nowrap"
                                    title="Add new widget of type Simple text"
                                    :disabled="$env.state.changesLock"
                                >
                                    Text
                                </button>
                                <button
                                    @click.stop="
                                        handleContainerActivated(container);
                                        $env.dispatch('handleCreateWidget', 'url');
                                    "
                                    class="mr-1 btn btn-sm bg-white border text-nowrap"
                                    title="Add new widget of type URL"
                                    :disabled="$env.state.changesLock"
                                >
                                    URL
                                </button>
                                <button
                                    @click.stop="
                                        handleContainerActivated(container);
                                        $env.dispatch('handleCreateWidget', 'counter');
                                    "
                                    class="mr-1 btn btn-sm bg-white border text-nowrap"
                                    title="Add new widget of type Counter"
                                    :disabled="$env.state.changesLock"
                                >
                                    Counter
                                </button>
                                <button
                                    @click.stop="
                                        handleContainerActivated(container);
                                        $env.dispatch('handleCreateWidget', 'simple_list');
                                    "
                                    class="mr-1 btn btn-sm bg-white border text-nowrap"
                                    title="Add new widget of type Simple list"
                                    :disabled="$env.state.changesLock"
                                >
                                    List
                                </button>
                                <button
                                    @click.stop="
                                        handleContainerActivated(container);
                                        $env.dispatch('handleCreateWidget', 'simple_switch');
                                    "
                                    class="btn border btn-sm text-nowrap bg-white"
                                    title="Add new widget of type Switch"
                                    :disabled="$env.state.changesLock"
                                >
                                    Switch
                                </button>
                                <button
                                    class="btn btn-sm"
                                    @click.stop="$env.dispatch('openOptions', container)"
                                    :disabled="$env.state.changesLock"
                                >
                                    <i class="fas fa-ellipsis-v"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Create / select section -->
            <div>
                <div v-if="$env.state.editMode && $store.state.user.is_authenticated">
                    <div class="d-flex p-1 border-top justify-content-between align-item-center">
                        <div class="d-flex p-1 mr-1">
                            <div v-if="$store.state.walls">
                                <a
                                    class="mr-1 btn dropdown-toggle bg-white"
                                    id="wall-list"
                                    data-toggle="dropdown"
                                    aria-haspopup="true"
                                    aria-expanded="false"
                                    title="Select wall to edit"
                                >
                                    Wall
                                </a>
                                <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                                    <router-link
                                        class="dropdown-item btn"
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
                                class="mr-1 btn btn-success"
                                @click="$env.dispatch('handleCreateWall')"
                                title="Add new wall"
                                :disabled="$env.state.changesLock"
                            >
                                <i class="fas fa-plus"></i>
                            </button>
                            <button
                                v-if="$env.state.wall"
                                @click.stop="$env.dispatch('handleCreateContainer')"
                                class="btn btn-success text-nowrap"
                                title="Add Container to hold widgets"
                                :disabled="$env.state.changesLock"
                            >
                                Container
                            </button>
                        </div>
                        <div class="d-flex p-1">
                            <div v-if="$store.state.ports && $env.state.wall">
                                <a
                                    class="btn btn-s dropdown-toggle bg-white mr-1"
                                    id="wall-list"
                                    data-toggle="dropdown"
                                    aria-haspopup="true"
                                    aria-expanded="false"
                                    title="Select port to edit"
                                >
                                    Port
                                </a>
                                <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                                    <a
                                        class="dropdown-item btn"
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
                                class="btn btn-success text-white"
                                @click="$env.dispatch('handleCreatePort')"
                                title="Add new port"
                                :disabled="$env.state.changesLock"
                            >
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Sidebar -->
        <div class="w-25 border-left px-2 overflow-auto" v-if="$env.state.editMode && $env.state.optionsSource">
            <Options></Options>
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

    import store from "../modules/store";
    import env from "../modules/env";
    import ws from "../modules/ws";

    async function setupRoutine(to, from, next) {
        await env.dispatch("closeOptions");
        await env.dispatch("setWallByWallId", to.params.wallId);
        if (!env.state.wall || (env.state.editMode && !store.state.meta.edit_permission)) {
            return next({ to: env.state.editMode ? "wallEdit" : "wallView" });
        }
        ws.open(to.params.wallId);
        if (env.state.wall.lock_widgets && !env.state.viewMode) {
            await env.dispatch("lockWidgets");
        } else {
            await env.dispatch("unlockWidgets");
        }
        await env.dispatch("setContainerByContainerId", store.state.containers[0].id);
        next();
    }

    export default {
        name: "Wall",
        components: {
            VueDraggableResizable,
            Options,
        },
        beforeRouteEnter: setupRoutine,
        beforeRouteUpdate: setupRoutine,
        methods: {
            handleContainerResizing(x, y, w, h) {
                let instance = Object.assign({}, this.$env.state.container, { h });

                this.$store.dispatch("recalculateWidgets", instance);
                this.$store.dispatch("updateOrAddInstance", instance);
            },
            handleContainerActivated(container) {
                window.dispatchEvent(new Event("resize"));
                this.$env.dispatch("setContainerByContainerId", container.id);
            },
            getComponent(widget) {
                return [SimpleText, URL, Counter, SimpleList, SimpleSwitch].filter(
                    (klass) => widget.type == klass.type
                )[0];
            },
        },
    };
</script>
