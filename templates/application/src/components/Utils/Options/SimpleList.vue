<template>
  <widget-options :instance="instance">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Simple List</span>
      </options-item>
      <options-item>
        <label slot="title" v-scope:for.inner_border>Item borders</label>
        <input
            slot="input"
            v-scope:id.inner_border
            v-model="instance.inner_border"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
      </options-item>
    </div>
  </widget-options>
</template>

<script>
import OptionsItem from "../Options.Item";
import WidgetOptions from "./_WidgetOptions";

export default {
  name: "SimpleListOptions",
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
  components: {
    OptionsItem,
    WidgetOptions
  },
};
</script>
