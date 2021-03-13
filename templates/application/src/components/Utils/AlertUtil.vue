<template>
    <span
        class="w-100 py-1 px-2 m-0 alert alert-dismissible fade show position-absolute"
        style="z-index: 1;"
        v-show="$env.state.alertShow"
        :class="'alert-' + $env.state.alertClass"
        @mouseout="$env.dispatch('hideAlert')"
        >{{ $env.state.alertMessage }}
        <a class="close btn py-1 px-2" aria-label="Close" @click="$env.dispatch('hideAlert')">
            <span aria-hidden="true">&times;</span>
        </a></span
    >
</template>
