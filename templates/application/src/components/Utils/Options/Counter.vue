<template>
  <widget-options :instance="instance" @push="$emit('push')">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Value control</span>
      </options-item>
      <options-item>
        <label slot="title" v-scope:for.value>Current value</label>
        <input
            slot="input"
            v-scope:id.value
            v-model.number="instance.value"
            @input="$emit('push')"
            :disabled="$env.state.changesLock"
            class="form-control"
            type="number"
        />
      </options-item>
      <options-item>
        <label slot="title" v-scope:for.step>Step</label>
        <input
            slot="input"
            v-scope:id.step
            v-model.number="instance.step"
            @input="$emit('push')"
            :disabled="$env.state.changesLock"
            class="form-control"
            type="number"
        />
      </options-item>
      <options-item :isHeader="true">
        <span slot="title">Other</span>
      </options-item>
      <options-item>
        <label slot="title" v-scope:for.vertical>Vertical orientation</label>
        <input
            slot="input"
            v-scope:id.vertical
            v-model="instance.vertical"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
        <span slot="help">Counter may have vertical or horizontal orientation</span>
      </options-item>
    </div>
  </widget-options>
</template>

<script>
// Front end is absolutely passive
import OptionsItem from "../Options.Item";
import WidgetOptions from "./_WidgetOptions";

export default {
  name: "CounterOptions",
  components: {
    OptionsItem,
    WidgetOptions,
  },
  props: {
    instance: {
      type: Object,
      required: true,
    },
  },
};
</script>
