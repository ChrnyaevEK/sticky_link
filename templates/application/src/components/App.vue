<template>
  <div class="h-100 d-flex flex-column overflow-hidden">
    <nav v-if="$store.state.user" class="navbar navbar-expand-md navbar-light border-bottom">
      <a class="navbar-brand" :href="homeUrl">{{ $store.state.app.title }}</a>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav">
          <li class="nav-item" v-if="$store.state.user.is_authenticated">
            <router-link
                class="nav-link"
                :to="{ name: 'wallOverview'}"
            > Walls
            </router-link>
          </li>
          <li class="nav-item" v-if="$store.state.user.is_authenticated">
            <router-link
                class="nav-link"
                :to="{ name: 'portOverview'}"
            > Ports
            </router-link>
          </li>
          <li class="nav-item" v-if="$store.state.user.is_authenticated">
            <router-link
                class="nav-link"
                :to="{ name: 'profile'}"
            > Account
            </router-link>
          </li>
        </ul>
      </div>
      <a :href="loginUrl" v-if="$store.state.user.is_anonymous">Login</a>
      <div class="d-flex align-items-center" v-if="$store.state.user.is_authenticated">
        <SaveUtil></SaveUtil>
        <button
            class="navbar-toggler ml-2"
            type="button"
            data-toggle="collapse"
            data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </nav>
    <notifications class="notification" :duration="3000" position="bottom left"></notifications>
    <div class="overflow-auto h-100">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import SaveUtil from "./Utils/SaveUtil";
import $ from "jquery";

export default {
  data() {
    return {
      homeUrl: process.env.VUE_APP_HOME,
      loginUrl: process.env.VUE_APP_LOGIN,
    };
  },
  components: {
    SaveUtil,
  },
  created() {
    $(document).keyup((e) => {
      if (e.keyCode === 27) this.$env.dispatch("closeOptions");
    });
  },
};
</script>
