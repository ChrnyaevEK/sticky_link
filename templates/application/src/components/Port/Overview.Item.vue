<template>
  <div class="btn-outline-light my-1 p-1">
    <div class="d-flex align-items-center">
      <span class=" flex-grow-1">
        <router-link :to="{name: 'portEdit', params: { portId: port.id }}">
          {{ port.title }}
        </router-link>
        <span class="text-truncate text-secondary">
          {{ port.description }}
        </span>
      </span>
      <strong class="mr-1 text-dark">
        {{ port.visited }}
      </strong>
      <button class="btn btn-sm text-danger" @click="deletePort">
        <i class="fas fa-trash"></i>
      </button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'PortOverviewItem',
  props: {
    port: {
      type: Object,
      required: true,
    }
  },
  methods: {
    deletePort() {
      if (confirm("Are you sure?")) {
        this.$store.dispatch("deleteInstance", this.port);
      }
    },
  }
}
</script>