<template>
  <widget-options :instance="instance" @push="$emit('push')">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Image</span>
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
        <label slot="title" class="form-check-label" v-scope:for.alt>Alternative text</label>
        <input
            slot="input"
            v-scope:id.alt
            v-model="instance.alt"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            class="form-control"
        />
        <span slot="help">This text will be displayed if we fail to obtain an image for any reason</span>
      </options-item>
    </div>
  </widget-options>
</template>

<script>
import WidgetOptions from "./_WidgetOptions";
import OptionsItem from "../Options.Item";

export default {
  name: "ImageOptions",
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
