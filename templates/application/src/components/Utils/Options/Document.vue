<template>
  <widget-options :instance="instance" @push="$emit('push')">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Content</span>
      </options-item>
      <options-item>
        <options-upload slot="input" :instance="instance"></options-upload>
      </options-item>
    </div>
  </widget-options>
</template>

<script>
import OptionsItem from "../Options.Item";
import WidgetOptions from "./_WidgetOptions";
import OptionsUpload from "../Options.Upload";

export default {
  name: "DocumentOptions",
  components: {
    OptionsItem,
    WidgetOptions,
    OptionsUpload,
  },
  props: {
    instance: {
      type: Object,
      required: true,
    },
  }
};
</script>
