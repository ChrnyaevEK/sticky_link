<template>
  <WidgetBaseResizable :widget="widget" class="center-content p-0">
    <img v-if="sourceURL" :src="sourceURL" class="w-100 h-100">
    <div v-else class="d-flex text-secondary align-items-center text-break p-2">
      <span class="mr-3">{{ widget.title }} </span>
      <i class="fas fa-images"></i>
    </div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "image",
  name: "SimpleImage",
  computed: {
    widget() {
      return this.$store.getters.getWidgetByUid(this.widgetUid)
    },
    sourceURL() {
      return this.$store.getters.getSourceUrl(this.widget)
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
