<template id="simple-switch-template">
  <WidgetBaseResizable :widget="widget">
    <div class="h-100 w-100 custom-switch center-content" :title="widget.title">
      <input
          type="checkbox"
          @change="changeValue"
          :checked="widget.value"
          v-scope:id.value
          :disabled="$env.state.widgetsLock || $env.state.changesLock"
          class="custom-control-input"
      />
      <label class="custom-control-label text-break" v-scope:for.value>{{ widget.title }}</label>
    </div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "simple_switch",
  name: "SimpleSwitch",
  template: "#simple-switch-template",
  components: {
    WidgetBaseResizable,
  },
  computed: {
    widget() {
      return this.$store.getters.getWidgetByUid(this.widgetUid)
    },
  },
  props: {
    widgetUid: {
      type: String,
      required: true,
    },
  },
  methods: {
    changeValue() {
      this.widget.value = !this.widget.value
      this.$proxy.dispatch("updateWidget", {
        widget: this.widget
      });
    },
  },
};
</script>
