<template>
  <div class="d-flex flex-column container py-3">
    <h5>Walls overview</h5>
    <div class="d-flex justify-content-end">
      <button
          class="btn btn-outline-success mr-1 text-truncate"
          @click="$proxy.dispatch('createWall', false)"
          :disabled="$env.state.changesLock"
      >
        Create wall
      </button>
      <button
          class="btn btn-outline-success text-truncate"
          @click="$proxy.dispatch('createWall', true)"
          :disabled="$env.state.changesLock"
      >
        Create and open wall
      </button>
    </div>
    <div v-if="$store.state.walls.length" class="my-3 py-2">
      <overview-item
          v-for="wall of $store.state.walls"
          :key="wall.id"
          :wall="wall"
      ></overview-item>
    </div>
    <p class="text-info" v-else>
      No walls yet... Go on and create one!
    </p>
  </div>
</template>
<script>
import OverviewItem from './Overview.Item';

export default {
  name: 'WallOverview',
  components: {
    OverviewItem,
  },
}
</script>