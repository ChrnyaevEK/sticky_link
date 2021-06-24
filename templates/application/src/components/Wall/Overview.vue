<template>
  <div class="d-flex flex-column container py-3">
    <h5>Walls overview</h5>
    <div v-if="$store.state.walls && $store.state.walls.length" class="my-3 py-2">
      <overview-item
          v-for="wall of $store.state.walls"
          :key="wall.id"
          :wall="wall"
      ></overview-item>
    </div>
    <p class="text-info" v-else>
      No walls yet... Go on and create one!
    </p>
    <div class="d-flex justify-content-end">
      <button
          class="btn btn-outline-success"
          @click="$env.dispatch('handleCreateWall')"
          :disabled="$env.state.changesLock"
      >
        Create wall
      </button>
    </div>
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