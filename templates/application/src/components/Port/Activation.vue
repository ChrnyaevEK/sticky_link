<template>
  <div class="h-100 container d-flex justify-content-center align-items-center">
    <div class="d-flex flex-column align-items-center">
      <div class="alert alert-warning">
        You are about to activate port {{ $route.params.portId }}. After that, the port will be assigned to the current account. This
        action is not revertible.
      </div>
      <button class="btn btn-outline-warning w-25" @click="$proxy.dispatch('activatePort', $route.params.portId)">Activate</button>
    </div>
  </div>
</template>
<script>
export default {};
</script>
