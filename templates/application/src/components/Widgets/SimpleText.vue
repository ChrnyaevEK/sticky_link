<template id="simple-text-template">
  <WidgetBaseResizable :widget="widget">
    <div class="ql-editor editor p-0" v-html="widget.text_content"></div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "simple_text",
  name: "SimpleText",
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
  height: 100%;
  width: 100%;
  overflow: hidden !important;
  min-height: unset !important;
  white-space: pre;
}
</style>
