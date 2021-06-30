<template>
  <div class="d-flex justify-content-center align-items-center h-100 w-100">
    <a :href="loginUrl" class="mr-1">Login</a> and try again!
  </div>
</template>
<script>
export default {
  data() {
    return {
      loginUrl: process.env.VUE_APP_LOGIN,
    }
  }
}
</script>
