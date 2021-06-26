<template>
  <div class="container py-3">
    <h4>
      Wall settings
    </h4>
    <div class="form-group">
      <label v-scope:for.title>Title <span class="text-secondary">{{ 200 - wall.title.length }}/200</span></label>
      <input
          :disabled="$env.state.changesLock"
          v-model="wall.title"
          v-scope.id:title
          class="form-control mr-1"
          maxlength="200"
      />
      <small class="form-text">Each wall has it's title - you personal wall name</small>
    </div>
    <div class="form-group">
      <label v-scope:for.description>Description <span class="text-secondary">{{
          500 - wall.description.length
        }}/500</span></label>
      <textarea
          v-scope:id.description
          v-model="wall.description"
          :disabled="$env.state.changesLock"
          class="form-control mr-1"
          maxlength="500"
          rows="5"
          style="resize: vertical;"
      />
      <small class="form-text">Describe what does this wall represent</small>
    </div>
    <div class="form-group">
      <label v-scope:for.allow_anonymous_view class="form-check">
        <input
            @change="$emit('push')"
            v-scope:id.allow_anonymous_view
            v-model="wall.allow_anonymous_view"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
        Allow anonymous <strong>view</strong>
      </label>
      <small class="form-text">Anyone will be able to view this wall and change widgets values</small>
    </div>
    <div class="form-group">
      <label v-scope:for.lock_widgets class="form-check">
        <input
            v-scope:id.lock_widgets
            v-model="wall.lock_widgets"
            :disabled="$env.state.changesLock"
            type="checkbox"
        />
        Lock widget actions
      </label>
      <small class="form-text">Lock widgets to prevent miss-click in wall editor</small>
    </div>
    <div class="form-group d-flex justify-content-end">
      <router-link class="btn btn-outline-danger mr-1" :to="{name: 'wallOverview'}">Close</router-link>
      <button class="btn btn-outline-success" @click.stop="$proxy.dispatch('updateWall', $el)">Save</button>
    </div>
  </div>
</template>
<script>
import ws from "../../modules/ws";

async function setupRoutine(to, from, next) {
  ws.open(to.params.wallId);
  next();
}

export default {
  computed: {
    wall() {
      return this.$proxy.getters.getWallById(this.$route.params.wallId)
    }
  },
  beforeRouteEnter: setupRoutine,
  beforeRouteUpdate: setupRoutine,
};
</script>
