<template>
  <vue-draggable-resizable
      :draggable="!$env.state.changesLock && $env.state.editMode"
      :resizable="!$env.state.changesLock && $env.state.editMode"
      @resizestop="resizeStop"
      @dragstop="drag"
      @activated="activated"
      @deactivated="deactivated"
      class="widget"
      :class="{ 'widget-border': widget.border,  'no-border': !widget.border }"
      :style="style"
      :parent="true"
      :w="widget.w"
      :h="widget.h"
      :y="widget.y"
      :x="widget.x"
      :z="widget.z"
      :minHeight="50"
      :minWidth="100"
      :grid="[$store.state.app.grid, $store.state.app.grid]"
      ref="base"
  >
    <div class="bg-white quick-access widget-quick-access" v-if="$env.state.editMode && active">
      <button
          v-if="widget.sync_id || widget.is_referenced"
          :title="
                widget.sync_id
                    ? `This widget is synchronized with ${widget.sync_id}`
                    : 'This widget is referenced by at least one widget'
                "
          :disabled="$env.state.changesLock || !widget.sync_id"
          class="btn btn-sm btn-outline-secondary mr-1"
          @click="copySyncWidget"
      >
        <i class="fas fa-link"></i>
      </button>
      <button :disabled="$env.state.changesLock" class="btn btn-sm btn-outline-danger mr-1"
              @click="$proxy.dispatch('deleteWidget', widget)">
        <i class="fas fa-trash"></i>
      </button>
      <button
          :disabled="$env.state.changesLock"
          class="btn btn-sm btn-outline-secondary mr-1"
          @click="$proxy.dispatch('copyWidget', widget)"
      >
        <i class="fas fa-copy"></i>
      </button>
      <button class="btn btn-sm btn-outline-secondary d-none d-md-block" @click.stop="openOptions">
        <i class="fas fa-ellipsis-v"></i>
      </button>
    </div>
    <slot></slot>
  </vue-draggable-resizable>
</template>

<script>
import VueDraggableResizable from "vue-draggable-resizable";
import "vue-draggable-resizable/dist/VueDraggableResizable.css";
import {copyToClipboard} from "../../common";

export default {
  name: "WidgetBaseResizable",
  props: {
    widget: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      active: false
    }
  },
  beforeUpdate() {
    this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
  },
  methods: {
    resizeStop(x, y, w, h) {
      this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
      this.widget.h = h
      this.widget.w = w
      this.$proxy.dispatch("updateWidget", {
        widget: this.widget
      });
    },
    drag(x, y) {
      this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
      this.widget.x = x
      this.widget.y = y
      this.$proxy.dispatch("updateWidget", {
        widget: this.widget
      });
    },
    deactivated() {
      this.active = false
    },
    activated() {
      this.active = true
      this.$refs.base.checkParentSize(); // Solve problem with component disappearing after update
      window.dispatchEvent(new Event("resize"))
    },
    openOptions() {
      if (this.$env.state.editMode) {
        this.$env.dispatch("openOptions", this.widget);
      }
    },
    copySyncWidget() {
      copyToClipboard(this.widget.sync_id);
      this.$notify({text: "Copied to clipboard!", type: "success"});
    },
  },
  components: {
    VueDraggableResizable,
  },
  computed: {
    style() {
      return `
        background-color: ${this.widget.background_color};
        color: ${this.widget.text_color};
        font-size:${this.widget.font_size}px;
        font-weight:${this.widget.font_weight};
        touch-action: ${this.$env.state.editMode ? "none" : "initial"};
      `;
    },
  },
};
</script>

<style scoped>
.widget-quick-access {
  right: 0;
  top: 0;
  position: absolute;
  display: flex;
  justify-content: flex-end;
  z-index: 2;
}

.widget-quick-access > * {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 2rem;
  width: 2rem;
}
</style>
