<template>
  <div class="btn-outline-light my-1 p-1">
    <div class="d-flex align-items-center">
      <div class="d-flex flex-grow-1 text-truncate">
        <strong class="text-dark mr-1 d-none d-sm-block">
          {{ wall.allow_anonymous_view ? 'Public' : 'Private' }}
        </strong>
        <div class="mr-1" :class="wall.title ? 'text-dark' : 'text-muted'">
          {{ wall.title || 'No title' }}
        </div>
        <div v-show="wall.description" class="text-secondary mr-1">
          {{ wall.description }}
        </div>
      </div>
      <router-link class="mr-2" :to="{name: 'wallEdit', params: { wallId: wall.id }}">
        Edit
      </router-link>
      <router-link class="mr-2" :to="{name: 'wallView', params: { wallId: wall.id }}">
        View
      </router-link>
      <button class="btn btn-sm text-danger mr-1" @click="$proxy.dispatch('deleteWall', wall)">
        <i class="fas fa-trash"></i>
      </button>
      <router-link class="btn btn-sm text-dark" :to="{name: 'wallSettings', params: { wallId: wall.id }}">
        <i class="fas fa-ellipsis-v"></i>
      </router-link>
    </div>
  </div>
</template>
<script>
export default {
  name: 'WallOverviewItem',
  props: {
    wall: {
      type: Object,
      required: true,
    }
  },
}
</script>