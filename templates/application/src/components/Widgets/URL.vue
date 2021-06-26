<template id="url-template">
  <WidgetBaseResizable :widget="widget">
    <a
        @click.stop.prevent="openHref"
        class="w-100 h-100 text-break cursor-pointer center-content"
        :style="`color: ${widget.text_color};`"
        :disabled="$env.state.widgetsLock || $env.state.changesLock"
    ><u>{{ widget.title || widget.href }}</u>
      <i class="mx-2 fas fa-external-link-square-alt text-muted"></i>
    </a>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "url",
  name: "URL",
  template: "#url-template",
  computed: {
    widget() {
      return this.$store.getters.getWidgetByUid(this.widgetUid)
    },
  },
  components: {
    WidgetBaseResizable,
  },
  props: {
    widgetUid: {
      type: String,
      required: true,
    },
  },
  methods: {
    openHref() {
      if (this.widget.href && !this.$env.state.widgetsLock) {
        window.open(this.widget.href, this.widget.open_in_new_window ? "_blank" : undefined);
      }
    },
  },
};
</script>
