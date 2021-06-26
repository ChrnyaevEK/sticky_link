<template>
  <div class="btn-outline-light my-1 p-1">
    <div class="d-flex align-items-center">
      <span class=" flex-grow-1">
        <span class="text-dark">
          {{ port.title }}
        </span>
        <span class="text-truncate text-secondary">
          {{ port.description }}
        </span>
      </span>
      <span class="mr-1 font-weight-bold text-dark" title="Visited">
        {{ port.visited }}
      </span>
      <button class="btn btn-sm text-danger mr-1" @click="$proxy.dispatch('deletePort', this.port)">
        <i class="fas fa-trash"></i>
      </button>
      <router-link class="btn btn-sm text-dark" :to="{name: 'portSettings', params: { portId }}">
        <i class="fas fa-ellipsis-v"></i>
      </router-link>
    </div>
  </div>
</template>
<script>
export default {
  name: 'PortOverviewItem',
  props: {
    portId: {
      type: String,
      required: true,
    }
  },
  computed: {
    port() {
      return this.$proxy.getters.getPortById(this.portId)
    }
  }
}
</script>