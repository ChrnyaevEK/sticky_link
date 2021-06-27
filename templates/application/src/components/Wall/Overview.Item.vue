<template>
  <div class="btn-outline-light my-1 p-1 row no-gutters">
    <div class="col-12 col-md-8 d-md-flex align-items-center">
      <div class="w-25 text-dark font-weight-bold d-none d-sm-block mr-1">
        {{ wall.allow_anonymous_view ? 'Public' : 'Private' }}
      </div>
      <div class="w-25 text-truncate mr-1" :class="wall.title ? 'text-dark' : 'text-muted'">
        {{ wall.title || 'No title' }}
      </div>
      <div class="w-50 text-truncate text-secondary">
        {{ wall.description }}
      </div>
    </div>
    <div class="col-12 col-md-4 d-flex justify-content-end align-items-center">
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