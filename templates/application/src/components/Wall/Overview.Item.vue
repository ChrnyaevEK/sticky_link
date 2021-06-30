<template>
  <div class="btn-outline-light my-1 p-1 row no-gutters">
    <div class="col-12 col-md-8 d-md-flex align-items-center">
      <div class="w-25 text-truncate mr-1 d-flex align-items-center" :title="wall.title"
           :class="wall.title ? 'text-dark font-weight-bold' : 'text-muted'">
        <small class="text-secondary mr-2">
          <i class="fas fa-user-friends mr-2" v-if="isShared" title="This wall is shared"></i>
          <i class="fas fa-check mr-2" v-else title="This wall is not shared, you are the only editor"></i>
          <i class="fas fa-eye" v-if="isPublic" title="Anonymous access is allowed"></i>
          <i class="fas fa-lock" v-else title="Anonymous access is forbidden"></i>
        </small>
        {{ wall.title || 'No title' }}
      </div>
      <div class="w-75 text-truncate text-secondary" :title="wall.description">
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
      <button :disabled="$env.state.changesLock" class="btn btn-sm text-danger mr-1" v-if="wall.owner_permission"
              @click="$proxy.dispatch('deleteWall', wall)">
        <i class="fas fa-trash"></i>
      </button>
      <router-link class="btn btn-sm text-dark" v-if="wall.owner_permission"
                   :to="{name: 'wallSettings', params: { wallId: wall.id }}">
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
  computed: {
    isShared() {
      return this.wall.trusted_users.length
    },
    isPublic() {
      return this.wall.allow_anonymous_view
    }
  }
}
</script>