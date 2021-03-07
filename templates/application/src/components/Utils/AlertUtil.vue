<template>
    <span
        class="w-100 m-0 alert alert-dismissible fade show fixed-top"
        v-show="$env.state.alertShow"
        :class="'alert-' + $env.state.alertClass"
        >{{ $env.state.alertMessage }}
        <a
            class="close btn"
            aria-label="Close"
            @click="$env.dispatch('hideAlert')"
        >
            <span aria-hidden="true">&times;</span>
        </a></span
    >
</template>
