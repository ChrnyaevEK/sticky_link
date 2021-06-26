<template>
  <div class="container py-3">
    <h4> Your profile at Sticky Link </h4>
    <div class="form-group">
      <div class="row">
        <div class="col-12 col-sm-3">
          <span class="text-secondary">Username</span>
        </div>
        <div class="col-12 col-sm-9">
          <span>{{ $store.state.user.username }}</span>
        </div>
      </div>
    </div>
    <div class="form-group">
      <div class="row">
        <div class="col-12 col-sm-3">
          <span class="text-secondary">E-mail</span>
        </div>
        <div class="col-12 col-sm-9">
          <span>{{ $store.state.user.email || '-' }}</span>
        </div>
      </div>
    </div>
    <div class="form-group d-flex justify-content-end">
      <a class="btn btn-outline-dark" :href="logoutUrl"> Logout </a>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Profile',
  data() {
    return {
      logoutUrl: process.env.VUE_APP_LOGOUT,
    };
  },
}
</script>