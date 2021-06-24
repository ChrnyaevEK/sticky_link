<template>
  <div class="btn-outline-light my-1 p-1">
    <div class="d-flex align-items-center">
      <span class=" flex-grow-1">
        <router-link :to="{name: 'wallEdit', params: { wallId: wall.id }}">
          {{ wall.title }}
        </router-link>
        <span class="text-truncate text-secondary">
          {{ wall.description }}
        </span>
      </span>
      <strong class="text-dark mr-1">
        {{ wall.allow_anonymous_view ? 'Public' : 'Private' }}
      </strong>
      <button class="btn btn-sm text-danger" @click="deleteWall">
        <i class="fas fa-trash"></i>
      </button>
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
  methods: {
    deleteWall() {
      if (confirm("Are you sure?")) {
        this.$store.dispatch("deleteInstance", this.wall);
      }
    },
  }
}
</script>