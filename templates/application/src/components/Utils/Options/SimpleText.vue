<template>
  <widget-options :instance="instance" @push="$emit('push')">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Content</span>
      </options-item>
      <TextEditor v-model="instance.text_content" @input="$emit('push')"
                  :disabled="$env.state.changesLock"></TextEditor>
    </div>
  </widget-options>
</template>

<script>
import OptionsItem from "../Options.Item";
import WidgetOptions from "./_WidgetOptions";
import TextEditor from "../TextEditor";

export default {
  name: "SimpleTextOptions",
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },

  components: {
    WidgetOptions,
    TextEditor,
    OptionsItem,
  },
};
</script>
