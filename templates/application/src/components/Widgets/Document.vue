<template>
  <WidgetBaseResizable :widget="widget">
    <div class="h-100 center-content flex-column text-break overflow-hidden">
      <strong :title="title" :class="{ 'text-muted': !title }">{{ title || "Empty" }}</strong>
      <hr class="w-75 text-secondary"/>
      <div v-if="title">
        <a :href="sourceURL + '?attachment=true'" target="_blank" class="text-truncate mr-3">Download</a>
        <a :href="sourceURL" target="_blank" class="text-truncate">Open</a>
      </div>
      <div class="text-muted" v-if="widget.source">{{ timeFormatted(widget.source.last_update) }}</div>
    </div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";
import {timeFormatted} from "../../common";

export default {
  type: "document",
  name: "Document",
  components: {
    WidgetBaseResizable,
  },
  computed: {
    widget() {
      return this.$store.getters.getWidgetByUid(this.widgetUid)
    },
    title() {
      return this.widget.title || (this.widget.source ? this.widget.source.name : "Not chosen");
    },
    sourceURL() {
      return this.$store.getters.getSourceUrl(this.widget)
    },
  },
  methods: {
    timeFormatted,
  },
  props: {
    widgetUid: {
      type: String,
      required: true,
    },
  },
};
</script>
