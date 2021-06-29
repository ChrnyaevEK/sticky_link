<template>
  <div class="d-flex flex-grow-1 h-100 overflow-hidden" :class="{ 'bg-light': $env.state.editMode }">
    <div class="w-75 d-flex flex-column flex-grow-1 overflow-auto" v-if="wall">
      <div class="alert alert-warning d-block d-md-none" role="alert" v-if="$env.state.editMode">
        <strong>Ups...</strong>
        <span> The device your are using is not wide enough, some features are disabled. Switch to wider screen to access full version!</span>
      </div>
      <div class="d-flex justify-content-end p-2 align-items-center">
        <span
            class="overflow-hidden py-1 flex-grow-1"
            :class="$env.state.editMode ? 'text-truncate' : 'text-break'"
        >
          <strong class="mr-1 text-primary" :title="wall.title">{{ wall.title }}</strong>
          <span class="text-secondary" :title="wall.description">{{ wall.description }}</span>
        </span>
        <router-link
            v-if="$env.state.editMode"
            class="btn btn-sm btn-outline-primary mr-1"
            :to="{ name: 'wallView', params: { wallId: wall.id }}"
        > View
        </router-link>
        <router-link
            v-if="$env.state.editMode && wall.owner_permission"
            :to="{name: 'wallSettings', params: {wallId: wall.id}}"
            class="btn btn-sm btn-outline-secondary d-none d-md-block"
        > Settings
        </router-link>
      </div>
      <!-- Container section -->
      <div class="flex-grow-1">
        <container
            v-for="container of $store.state.containers"
            :key="container.id"
            :containerId="container.id"
        >
        </container>
        <div v-if="$env.state.editMode" class="d-flex justify-content-end p-2">
          <button
              @click.stop="$proxy.dispatch('createContainer', wall)"
              :disabled="$env.state.changesLock"
              class="btn btn-sm btn-outline-success"
              title="Add Container to hold widgets"
          >
            Container
          </button>
        </div>
      </div>
    </div>
    <!-- Sidebar -->
    <div
        class="w-25 border-left px-2 overflow-auto d-none d-md-block"
        v-if="$env.state.editMode && $proxy.state.targetInstanceUid"
    >
      <Options></Options>
    </div>
  </div>
</template>

<script>
import Options from "../Utils/Options";
import Container from '../Widgets/Container'

import env from "../../modules/env";
import store from "../../modules/store";
import ws from "../../modules/ws";

async function setupRoutine(to, from, next) {
  await env.dispatch("closeOptions");
  let wall = store.getters.getWallById(to.params.wallId)
  await env.dispatch(wall.lock_widgets && env.state.editMode ? "lockWidgets" : 'unlockWidgets');
  ws.open(to.params.wallId);
  next();
}

export default {
  name: "Wall",
  components: {
    Container,
    Options,
  },
  computed: {
    wall() {
      return this.$store.getters.getWallById(this.$route.params.wallId)
    }
  },
  beforeRouteEnter: setupRoutine,
  beforeRouteUpdate: setupRoutine,
};
</script>
