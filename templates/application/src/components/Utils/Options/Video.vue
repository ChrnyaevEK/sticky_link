<template>
  <widget-options :instance="instance" @push="$emit('push')">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Video</span>
      </options-item>
      <options-item>
        <label slot="title" v-scope:for.source>Source</label>
        <input
            slot="input"
            v-scope:id.source
            v-model="instance.source"
            @input="$emit('push')"
            :disabled="$env.state.changesLock"
            class="form-control"
        />
      </options-item>
      <options-item>
        <label slot="title" class="form-check-label" v-scope:for.youtube>Youtube video</label>
        <input
            slot="input"
            v-scope:id.youtube
            v-model="instance.youtube"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
      </options-item>
      <options-item>
        <label slot="title" class="form-check-label" v-scope:for.autoplay>Autoplay</label>
        <input
            slot="input"
            v-scope:id.autoplay
            v-model="instance.autoplay"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
      </options-item>
      <options-item>
        <label slot="title" class="form-check-label" v-scope:for.loop>Loop video</label>
        <input
            slot="input"
            v-scope:id.loop
            v-model="instance.loop"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
      </options-item>
    </div>
  </widget-options>
</template>

<script>
import WidgetOptions from "./_WidgetOptions";
import OptionsItem from "../Options.Item";

export default {
  name: "VideoOptions",
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
  components: {
    OptionsItem,
    WidgetOptions,
  },
};
</script>
