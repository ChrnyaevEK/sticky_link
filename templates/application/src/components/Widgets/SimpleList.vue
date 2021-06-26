<template id="simple-list-template">
  <WidgetBaseResizable :widget="widget">
    <div class="h-100 d-flex flex-column">
      <div class="text-secondary text-truncate" :title="widget.title">
        {{ widget.title }}
      </div>
      <div class="flex-grow-1" :class="$env.state.editMode ? 'overflow-hidden' : 'overflow-auto'">
        <div
            class="d-flex mb-1 align-items-start"
            :class="{ border: widget.inner_border }"
            v-for="(val, i) of widget.items"
            :key="i"
        >
          <div class="d-flex flex-grow-1 p-1 text-break">
            <span class="mr-1 text-secondary text-nowrap">{{ i + 1 }}.</span>
            <span>{{ val }}</span>
          </div>
          <button
              @click.stop="removeItem(i)"
              :disabled="$env.state.widgetsLock || $env.state.changesLock"
              class="btn btn-sm text-danger"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>
      <div class="d-flex">
        <input
            type="text"
            v-scope:id.item-input
            v-model="item"
            @keyup.enter="addItem"
            class="form-control"
            :disabled="$env.state.widgetsLock || $env.state.changesLock"
        />
        <button @click.stop="addItem" :disabled="$env.state.widgetsLock || $env.state.changesLock" class="btn">
          <i class="fas fa-plus"></i>
        </button>
      </div>
    </div>
  </WidgetBaseResizable>
</template>

<script>
import WidgetBaseResizable from "./_Base";

export default {
  type: "simple_list",
  name: "SimpleList",
  template: "#simple-list-template",
  components: {WidgetBaseResizable},
  computed: {
    widget() {
      return this.$store.getters.getWidgetByUid(this.widgetUid)
    },
  },
  data() {
    return {
      item: undefined, // Item to add
    };
  },
  props: {
    widgetUid: {
      type: String,
      required: true,
    },
  },
  methods: {
    addItem() {
      if (this.item && !this.$env.state.widgetsLock) {
        if (this.widget.items === undefined) {
          this.widget.items = []
        }
        this.widget.items.push(this.item);
        this.item = undefined;
        this.$proxy.dispatch("updateWidget", {
          widget: this.widget
        });
      }
    },
    removeItem(i) {
      if (this.widget.items) {
        this.widget.items.splice(i, 1);
        this.$proxy.dispatch("updateWidget", {
          widget: this.widget
        });
      }
    },
  },
};
</script>

<style scoped>
input,
input:active,
input:focus {
  background-color: inherit;
}
</style>
