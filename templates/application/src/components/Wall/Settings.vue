<template>
  <div class="container py-3">
    <h4>
      Wall settings
    </h4>
    <h5>
      General
    </h5>
    <div class="form-group">
      <label v-scope:for.title>Title <span class="text-secondary">{{
          200 - (wall.title ? wall.title.length : 0)
        }}/200</span></label>
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
          500 - (wall.description ? wall.description.length : 0)
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
    <h5>Trusted users</h5>
    <div class="form-group">
      <label v-scope:for.trusted_users>
        Enter <strong>username</strong> to grant edit access on this wall
      </label>
      <div class="d-flex align-items-center">
        <input class="form-control mr-1 font-weight-bold" v-model="username" @input.stop="validate"
               :disabled="$env.state.changesLock"
               :class="this.user ? 'text-success' : 'text-danger'"
               :title="this.user ? 'User was found' : 'User was not found'"
               @keypress.enter.stop="addTrustedUser"
        >
        <button
            :disabled="$env.state.changesLock"
            class="btn btn-outline-secondary text-nowrap" @click="addTrustedUser">Grant permission
        </button>
      </div>
    </div>
    <div class="form-group">
      <div v-if="wall.trusted_users.length">
        <div v-for="user of wall.trusted_users" :key="user.id" class="d-flex align-items-center btn-outline-light">
          <div class="flex-grow-1 text-dark">
            <span class="mr-1">
              {{ user.username }}
            </span>
            <span class="text-secondary">
             {{ user.email || 'e-mail unknown' }}
            </span>
          </div>
          <button :disabled="$env.state.changesLock" class="btn btn-sm text-danger" @click="deleteTrustedUser(user)"
                  title="Remove from trusted users"><i
              class="fas fa-trash"></i></button>
        </div>
      </div>
      <div v-else>
        <div class="alert alert-info">You are the only wall editor</div>
      </div>
    </div>
    <div class="form-group d-flex justify-content-end">
      <button :disabled="$env.state.changesLock" class="btn btn-outline-danger mr-1" @click="$router.go(-1)">Close
      </button>
      <button :disabled="$env.state.changesLock" class="btn btn-outline-success"
              @click.stop="$proxy.dispatch('updateWall', {wall, warningTarget: $el})">
        Save
      </button>
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
      return this.$store.getters.getWallById(this.$route.params.wallId)
    }
  },
  data() {
    return {
      username: null,
      user: null,
      validateTimeout: 1000,
      validateTimeoutId: null,
      validating: false,
    }
  },
  methods: {
    isTrusted(user) {
      if (user) {
        for (let u of this.wall.trusted_users) {
          if (u.id === user.id) {
            return true
          }
        }
        if (this.$store.state.user.id === user.id){
          return true
        }
      }
      return false
    },
    validate(e) {
      this.username = e.target.value
      clearTimeout(this.validateTimeoutId)
      this.validateTimeoutId = setTimeout(this.$_validate, this.validateTimeout)
    },
    async $_validate() {
      this.validating = true
      this.user = await this.$store.dispatch('fetchTrustedUser', this.username)
      this.validating = false
      this.searched = true
    },
    async addTrustedUser() {
      if (!this.user) {
        await this.$_validate()
      }
      if (this.isTrusted(this.user)) {
        return this.$notify({
          text: "User is already trusted",
          type: "warn",
        })
      }
      if (!this.user) {
        return this.$notify({
          text: "User does not exist",
          type: "warn",
        })
      }
      await this.$proxy.dispatch('addTrustedUser', {
        username: this.user.username,
        wall: this.$route.params.wallId,
      })
      this.unsetUser()
    },
    async deleteTrustedUser(user) {
      await this.$proxy.dispatch('deleteTrustedUser', {
        username: user.username,
        wall: this.$route.params.wallId,
      })
    },
    unsetUser() {
      this.user = null
      this.username = null
    }
  },
  beforeRouteEnter: setupRoutine,
  beforeRouteUpdate: setupRoutine,
};
</script>
