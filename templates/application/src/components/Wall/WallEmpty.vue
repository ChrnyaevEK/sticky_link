<template>
    <div class="w-100 h-100 d-flex justify-content-center align-items-center text-muted">
        <span v-if="$store.state.user.is_authenticated">No wall is selected...</span>
        <span v-else>No wall is available...</span>
    </div>
</template>

<style scoped>
    .rotate-left-315 {
        transform: rotate(315deg);
    }
</style>
