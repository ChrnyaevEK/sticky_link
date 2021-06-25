<template>
  <div class="d-flex flex-grow-1 h-100 overflow-hidden" :class="{ 'bg-light': $env.state.editMode }">
    <div class="w-75 d-flex flex-column flex-grow-1 overflow-auto" v-if="$proxy.state.wall">
      <div class="alert alert-warning d-block d-md-none" role="alert" v-if="$env.state.editMode">
        <strong>Ups...</strong>
        <span>
                    The device your are using is not wide enough, some features are disabled. Switch to wider screen to
                    access full version!</span
        >
      </div>
      <!-- Wall title -->
      <div class="d-flex justify-content-end p-2 align-items-center">
        <span
            v-if="$proxy.state.wall"
            class="overflow-hidden py-1 flex-grow-1"
            :class="$env.state.editMode ? 'text-truncate' : 'text-break'"
        >
            <strong class="mr-1 text-primary" :title="$proxy.state.wall.title">{{
                $proxy.state.wall.title
              }}</strong>
            <span class="text-secondary" :title="$proxy.state.wall.description">{{
                $proxy.state.wall.description
              }}</span>
        </span>
        <router-link
            class="btn btn-sm btn-outline-primary mr-1"
            :to="{ name: 'wallView', params: { wallId: $proxy.state.wall.id }}"
        > View
        </router-link>
        <button
            v-if="$proxy.state.wall && $env.state.editMode"
            class="btn btn-sm bg-white btn-outline-secondary d-none d-md-block"
            @click.stop="$env.dispatch('openOptions', $proxy.state.wall)"
            :disabled="$env.state.changesLock"
        >
          Settings
        </button>
      </div>
      <!-- Container section -->
      <div class="flex-grow-1">

        <div
            class="d-flex flex-column bg-white"
            :class="{ 'border-top border-bottom': $env.state.editMode }"
            v-for="container of $store.state.containers"
            :key="container.id"
        >
          <div class="px-2 d-flex justify-content-between">
            <div class="mr-1 py-1" :class="$env.state.editMode ? 'text-truncate' : 'text-break'">
              <strong class="mr-1 text-primary">{{ container.title }}</strong>
              <span class="text-secondary">{{ container.description }}</span>
            </div>
            <button
                v-if="$env.state.editMode"
                class="btn btn-sm d-none d-md-block"
                @click.stop="$env.dispatch('openOptions', container)"
                :disabled="$env.state.changesLock"
            >
              <i class="fas fa-ellipsis-h"></i>
            </button>
          </div>
          <div class="overflow-auto" style="-webkit-overflow-scrolling: touch;">
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
                class="position-relative wall-only content-box overflow-hidden"
                :class="{
                                    'border-top border-bottom border-left-0 border-right-0':
                                        $env.state.editMode && !container.grid,
                                    'grid no-border': $env.state.editMode && container.grid,
                                    'no-border': !$env.state.editMode,
                                }"
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
          <div class="px-2 py-1 d-flex align-items-center">
            <div
                v-if="$env.state.editMode"
                class="flex-grow-1 d-flex justify-content-end align-items-center"
            >
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
                  class="btn border btn-sm text-nowrap bg-white mr-1"
                  title="Add new widget of type Switch"
                  :disabled="$env.state.changesLock"
              >
                Switch
              </button>
              <button
                  @click.stop="
                                        handleContainerActivated(container);
                                        $env.dispatch('handleCreateWidget', 'document');
                                    "
                  class="btn border btn-sm text-nowrap bg-white"
                  title="Add new widget of type File"
                  :disabled="$env.state.changesLock"
              >
                Document
              </button>
            </div>
          </div>
        </div>
        <div class="d-flex justify-content-end p-2">
          <button
              v-if="$proxy.state.wall"
              @click.stop="$env.dispatch('handleCreateContainer')"
              class="btn btn-sm btn-outline-success"
              title="Add Container to hold widgets"
              :disabled="$env.state.changesLock"
          >
            Container
          </button>
        </div>
      </div>
    </div>
    <!-- Sidebar -->
    <div
        class="w-25 border-left px-2 overflow-auto d-none d-md-block"
        v-if="$env.state.editMode && $env.state.targetInstance"
    >
      <!-- Button trigger modal -->
      <Options></Options>
    </div>
  </div>
</template>

<script>
import SimpleText from "../Widgets/SimpleText";
import URL from "../Widgets/URL";
import Counter from "../Widgets/Counter";
import SimpleList from "../Widgets/SimpleList";
import SimpleSwitch from "../Widgets/SimpleSwitch";
import Document from "../Widgets/Document";
import Options from "../Utils/Options";

import VueDraggableResizable from "vue-draggable-resizable";

import store from "../../modules/store";
import proxy from "../../modules/proxy";
import env from "../../modules/env";
import ws from "../../modules/ws";

async function setupRoutine(to, from, next) {
  await env.dispatch("closeOptions");
  await proxy.dispatch("setWallById", to.params.wallId);
  if (!proxy.state.wall) {
    return next({to: "home"});
  }
  ws.open(to.params.wallId);
  if (proxy.state.wall.lock_widgets && !env.state.viewMode) {
    await env.dispatch("lockWidgets");
  } else {
    await env.dispatch("unlockWidgets");
  }
  await proxy.dispatch("setContainerById", store.state.containers[0].id);
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
      let instance = Object.assign({}, this.$proxy.state.container, {h});

      this.$store.dispatch("recalculateWidgets", instance);
      this.$store.dispatch("updateOrAddInstance", instance);
    },
    handleContainerActivated(container) {
      window.dispatchEvent(new Event("resize"));
      this.$proxy.dispatch("setContainerById", container.id);
    },
    getComponent(widget) {
      return [SimpleText, URL, Counter, SimpleList, SimpleSwitch, Document].filter(
          (klass) => widget.type == klass.type
      )[0];
    },
  },
};
</script>
