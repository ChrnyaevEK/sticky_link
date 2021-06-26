<template id="counter-template">
  <WidgetBaseResizable :widget="widget">
    <div class="h-100 d-flex flex-column">
      <div class="text-secondary text-truncate" :title="widget.title">
        {{ widget.title }}
      </div>
      <div
          class="d-flex justify-content-between align-items-center flex-grow-1"
          :class="{ 'flex-column': widget.vertical }"
      >
        <button
            v-if="widget.vertical"
            key="fa-chevron-up"
            class="btn border-bottom w-100"
            @click="changeValue(widget.step)"
            :disabled="$env.state.widgetsLock || $env.state.changesLock"
        >
          <i class="fa fa-chevron-up"></i>
        </button>
        <button
            v-else
            key="fa-chevron-left"
            class="btn border-right h-100"
            @click="changeValue(-widget.step)"
            :disabled="$env.state.widgetsLock || $env.state.changesLock"
        >
          <i class="fa fa-chevron-left"></i>
        </button>
        <span class="text-truncate text-wrap text-break cursor-default">
                    {{ widget.value }}
                </span>
        <button
            v-if="widget.vertical"
            key="fa-chevron-down"
            class="btn border-top w-100"
            @click="changeValue(-widget.step)"
            :disabled="$env.state.widgetsLock || $env.state.changesLock"
        >
          <i class="fa fa-chevron-down"></i>
        </button>
        <button
            v-else
            key="fa-chevron-right"
            class="btn border-left h-100"
            @click="changeValue(widget.step)"
            :disabled="$env.state.widgetsLock || $env.state.changesLock"
        >
          <i class="fa fa-chevron-right"></i>
        </button>
      </div>
    </div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "counter",
  name: "Counter",
  template: "#counter-template",
  components: {
    WidgetBaseResizable,
  },
  props: {
    widgetUid: {
      type: String,
      required: true,
    },
  },
  computed: {
    widget() {
      return this.$proxy.getters.getWidgetByUid(this.widgetUid)
    }
  },
  methods: {
    changeValue(diff) {
      this.widget.value += diff;
      this.$proxy.dispatch("updateWidget", {
        widget: this.widget
      });
    },
  },
}
;
</script>
<style scoped>
button {
  background-color: inherit;
  border-radius: 0;
}
</style>
