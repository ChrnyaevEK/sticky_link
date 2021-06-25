<template>
  <widget-options :instance="instance">
    <div class="form-group">
      <options-item :isHeader="true">
        <span slot="title">Description</span>
      </options-item>
      <options-item>
        <label v-scope:for.title slot="title">Title</label>
        <input
            slot="input"
            @input="$emit('push')"
            v-scope:id.title
            v-model="instance.title"
            :disabled="$env.state.changesLock"
            class="form-control"
            maxlength="200"
        />
      </options-item>
      <options-item>
        <label v-scope:for.description slot="title">Description</label>
        <input
            slot="input"
            @input="$emit('push')"
            :disabled="$env.state.changesLock"
            v-scope:id.description
            v-model="instance.description"
            class="form-control"
            maxlength="500"
        />
      </options-item>
      <options-item :isHeader="true">
        <span slot="title">Size</span>
        <span slot="description">(container has constant width)</span>
      </options-item>
      <options-item>
        <label v-scope:for.h slot="title">Height</label>
        <input
            slot="input"
            @input="$emit('push')"
            v-scope:id.h
            v-model.number="instance.h"
            :step="$store.state.app.grid"
            :disabled="$env.state.changesLock"
            min="50"
            class="form-control"
            type="number"
        />
        <span slot="help">Widgets will be recalculated to fit the container.</span>
      </options-item>
      <options-item :isHeader="true">
        <span slot="title">Other</span>
      </options-item>
      <options-item>
        <label v-scope:for.grid slot="title">Enable grid</label>
        <input
            slot="input"
            v-scope:id.grid
            v-model="instance.grid"
            @change="$emit('push')"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
      </options-item>
    </div>
  </widget-options>
</template>

<script>
// Front end is absolutely passive
import WidgetOptions from "./_WidgetOptions";
import OptionsItem from "../Options.Item";

export default {
  name: "ContainerOptions",
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
