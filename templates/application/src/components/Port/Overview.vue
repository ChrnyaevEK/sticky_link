<template>
  <div class="d-flex flex-column container py-3">
    <h5>Ports overview</h5>
    <p>
      Port is a static link to wall. You should use ports for any external navigation, to be able to change
      target wall online
    </p>
    <div class="d-flex justify-content-end">
      <button
          class="btn btn-outline-success text-truncate"
          @click="$proxy.dispatch('createPort')"
          :disabled="$env.state.changesLock"
      >
        Create port
      </button>
    </div>
    <div v-if="$store.state.ports.length" class="my-3 py-2">
      <overview-item
          v-for="port of $store.state.ports"
          :key="port.id"
          :portId="port.id"
      ></overview-item>
    </div>
    <p v-else class="text-secondary">
      No ports yet... Go on and create one!
    </p>
  </div>
</template>
<script>
import OverviewItem from './Overview.Item';

export default {
  name: 'PortOverview',
  components: {
    OverviewItem,
  },
}
</script>