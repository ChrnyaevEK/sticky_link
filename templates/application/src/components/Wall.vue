<template>
    <div class="h-100 bg-light d-flex flex-column justify-content-between align-items-center overflow-hidden p-1">
        <div v-if="$env.state.wall && ($env.state.wall.title || $env.state.wall.description)" class="w-100 text-nowrap overflow-hidden">
            {{ $env.state.wall.title }} <small class="mx-1">{{ $env.state.wall.description }}</small>
        </div>
        <div
            class="w-100 h-100 py-1 overflow-auto pb-5"
            v-if="$env.state.wall"
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
                <div
                    v-show="container.title || container.description"
                    class="w-100 text-nowrap text-secondary overflow-hidden"
                >
                    {{ container.title }} <small class="mx-1">{{ container.description }}</small>
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
                        :resizable="$env.state.mode == $env.state.editMode && !$env.state.changesLock"
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
                    v-if="$env.state.mode == $env.state.editMode"
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
            <Options v-if="$env.state.mode == $env.state.editMode"></Options>
        </div>
        <div v-else class="w-100 h-100 d-flex justify-content-center align-items-center text-secondary">
            <span v-if="$store.state.user.is_authenticated">No wall is selected...</span>
            <span v-else>No wall is available... Login to continue</span>
        </div>
        <SelectCreate
            @wallCreated="onCreateWall"
            @portSelected="onPortSelected"
            v-if="$env.state.mode == $env.state.editMode && $store.state.user.is_authenticated"
        ></SelectCreate>
    </div>
</template>

<script>
    import SelectCreate from "./Utils/SelectCreate";
    import SimpleText from "./Widgets/SimpleText";
    import URL from "./Widgets/URL";
    import Counter from "./Widgets/Counter";
    import SimpleList from "./Widgets/SimpleList";
    import SimpleSwitch from "./Widgets/SimpleSwitch";
    import Options from "./Utils/Options";
    import VueDraggableResizable from "vue-draggable-resizable";
    import $ from "jquery";
    import router from "../modules/router";

    export default {
        components: {
            VueDraggableResizable,
            Options,
            SelectCreate,
        },
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

                if (this.$env.state.mode == this.$env.state.editMode) {
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
            onCreateWall(wall) {
                this.$io.alert("New wall has been created!", "success");
                router.push({
                    name: "wallEdit",
                    params: {
                        wallId: wall.id,
                    },
                });
            },
            onPortSelected(port) {
                this.$env.dispatch("openOptions", port);
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
