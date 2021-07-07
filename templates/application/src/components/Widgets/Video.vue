<template>
  <WidgetBaseResizable :widget="widget" class="center-content" :class="{ 'p-3': $env.state.editMode }">
    <video v-if="widget.source && !widget.youtube"
           :src="widget.source"
           type="video/mp4"
           :autoplay="widget.autoplay"
           :loop="widget.loop"
           :widget-uid="widget.uid"
           controls
           class="w-100 h-100"/>
    <iframe v-else-if="widget.source && widget.youtube" class="w-100 h-100"
            :src="'https://www.youtube.com/embed/' + youtubeId" title="YouTube video player" frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen></iframe>
    <div v-else class="d-flex text-secondary align-items-center text-break p-2">
      <span class="mr-3"> {{ widget.title }} </span>
      <i class="fas fa-video"></i>
    </div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "video",
  name: "SimpleVideo",
  computed: {
    widget() {
      return this.$store.getters.getWidgetByUid(this.widgetUid)
    },
    youtubeId() {
      if (this.widget.source && this.widget.youtube) {
        return this.widget.source.split('/').slice(this.widget.source.slice(-1) === '/' ? -2 : -1)[0]
      }
      return ''
    }
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
