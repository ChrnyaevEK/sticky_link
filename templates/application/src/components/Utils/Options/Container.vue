<template>
  <div class="form-group">
    <options-item :isHeader="true">
      <span slot="title">Description</span>
    </options-item>
    <options-item>
      <label v-scope:for.title slot="title">Title</label>
      <input
          v-scope:id.title
          slot="input"
          v-model="instance.title"
          @input="$emit('push')"
          :disabled="$env.state.changesLock"
          class="form-control"
          maxlength="200"
      />
    </options-item>
    <options-item>
      <label v-scope:for.description slot="title">Description</label>
      <input
          slot="input"
          v-scope:id.description
          @input="$emit('push')"
          :disabled="$env.state.changesLock"
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
          v-scope:id.h
          :step="$store.state.app.grid"
          v-model.number="instance.h"
          @input="$emit('push')"
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
</template>

<script>
// Front end is absolutely passive
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
  },
};
</script>
