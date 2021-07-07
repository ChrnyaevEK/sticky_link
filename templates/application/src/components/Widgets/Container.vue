<template>
  <div
      class="d-flex flex-column bg-white mb-2"
      :class="{ 'border-top border-bottom': $env.state.editMode }"
  >
    <div class="px-2 d-flex">
      <div class="mr-1 py-1 flex-grow-1" :class="$env.state.editMode ? 'text-truncate' : 'text-break'">
        <strong class="mr-1 text-primary">{{ container.title }}</strong>
        <span class="text-secondary">{{ container.description }}</span>
      </div>
      <button
          v-if="$env.state.editMode"
          class="btn btn-sm text-secondary d-none d-md-block"
          @click.stop="$env.dispatch('openOptions', container)"
          :disabled="$env.state.changesLock"
      >
        <i class="fas fa-ellipsis-v"></i>
      </button>
    </div>
    <div class="overflow-auto" style="-webkit-overflow-scrolling: touch;">
      <vue-draggable-resizable
          @resizing="resizing"
          @activated="activated"
          :resizable="$env.state.editMode && !$env.state.changesLock"
          :draggable="false"
          :parent="false"
          :handles="['bm']"
          :h="container.h"
          :w="container.w"
          :minHeight="100"
          class="position-relative wall-only content-box overflow-hidden"
          :class="{
                    'border-top border-bottom border-left-0 border-right-0': $env.state.editMode && !container.grid,
                    'grid no-border': $env.state.editMode && container.grid,
                    'no-border': !$env.state.editMode,
                  }"
          style="touch-action: initial;"
          :grid="[$store.state.app.grid, $store.state.app.grid]"
      >
        <template v-for="widget of $store.state.widgets">
          <component
              v-if="widget.container === container.id"
              :is="getComponent(widget)"
              :key="widget.type + widget.id"
              :widgetUid="widget.uid"
          >
          </component>
        </template>
      </vue-draggable-resizable>
    </div>
    <div v-if="$env.state.editMode" class="px-2 py-1 d-flex align-items-center">
      <div class="flex-grow-1 d-flex justify-content-end align-items-center">
        <button
            v-for="type of Object.keys(mapping)"
            @click.stop="activated(); $proxy.dispatch('createWidget', {type, container});"
            :key="type"
            :disabled="$env.state.changesLock"
            :title="'Add new widget, ' + mapping[type]"
            class="mr-1 btn btn-sm btn-outline-secondary text-nowrap"
        >
          {{ mapping[type] }}
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import VueDraggableResizable from "vue-draggable-resizable";
import SimpleText from "../Widgets/SimpleText";
import URL from "../Widgets/URL";
import SimpleImage from "../Widgets/Image";
import SimpleVideo from "../Widgets/Video";
import Counter from "../Widgets/Counter";
import SimpleList from "../Widgets/SimpleList";
import SimpleSwitch from "../Widgets/SimpleSwitch";
import Document from "../Widgets/Document";

export default {
  components: {
    VueDraggableResizable,
  },
  props: {
    containerId: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      mapping: {
        simple_text: 'Text',
        url: 'URL',
        image: 'Image',
        video: 'Video',
        counter: 'Counter',
        simple_list: 'List',
        simple_switch: 'Switch',
        document: 'Document'
      },
    }
  },
  computed: {
    container() {
      return this.$store.getters.getContainerById(this.containerId)
    }
  },
  methods: {
    resizing(x, y, w, h) {
      this.container.h = h;
      this.$store.dispatch("recalculateWidgets", this.container);
      this.$proxy.dispatch("updateContainer", {
        container: this.container
      });
    },
    activated() {
      window.dispatchEvent(new Event("resize"));
    },
    getComponent(widget) {
      return [SimpleText, URL, Counter, SimpleList, SimpleSwitch, Document, SimpleImage, SimpleVideo].filter(
          (c) => widget.type === c.type
      )[0];
    },
  }
}
</script>