<template id="simple-text-template">
  <WidgetBaseResizable :widget="widget" class="overflow-hidden">
    <span class="ql-editor editor p-0" v-html="widget.text_content"></span>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "simple_text",
  name: "SimpleText",
  template: "#simple-text-template",
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
};
</script>

<style>
.editor {
  min-height: unset !important;
  white-space: pre;
}
</style>
