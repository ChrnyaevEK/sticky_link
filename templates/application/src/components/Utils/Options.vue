<template>
  <div v-if="instance">
    <div class="text-right">
      <a class="btn" @click="$env.dispatch('closeOptions')"><i class="fas fa-times"></i></a>
    </div>
    <component :is="component" :instance="instance"
               @push="$proxy.dispatch('updateTargetInstance', {instance, warningTarget: $el})"></component>
    <div class="form-group">
      <button
          class="btn btn-sm btn-outline-danger w-100"
          :disabled="$env.state.changesLock"
          @click.stop="$proxy.dispatch('deleteTargetInstance', instance)"
      >
        Delete
      </button>
    </div>
    <div class="form-group text-center">
      <small class="text-secondary">All changes are automatically saved</small>
    </div>
  </div>
</template>

<script>
import CounterOptions from "./Options/Counter";
import SimpleListOptions from "./Options/SimpleList";
import SimpleTextOptions from "./Options/SimpleText";
import UrlOptions from "./Options/Url";
import DocumentOptions from "./Options/Document";
import ContainerOptions from "./Options/Container";
import WidgetsOptions from "./Options/_WidgetOptions";

export default {
  name: "Options",
  computed: {
    component() {
      switch (this.instance.type) {
        case 'container':
          return ContainerOptions;
        case 'counter':
          return CounterOptions
        case 'simple_list':
          return SimpleListOptions
        case 'simple_text':
          return SimpleTextOptions
        case 'url':
          return UrlOptions
        case 'document':
          return DocumentOptions
        default:
          return WidgetsOptions
      }
    },
    instance() {
      return this.$store.getters.getInstanceByUid(this.$proxy.state.targetInstanceUid)
    },
  },
  components: {
    ContainerOptions,
    CounterOptions,
    SimpleListOptions,
    SimpleTextOptions,
    UrlOptions,
    DocumentOptions,
    WidgetsOptions,
  },
};
</script>
