<template>
    <div class="w-100 h-100 d-flex flex-column">
        <span class=" w-100 p-1 bg-white border-bottom">
            <a href="/" class="m-3"> Sticky link </a>
            <router-link
                class="mr-3"
                :to="{
                    name: 'wall',
                    params: { wallId: $route.params.wallId },
                    query: { mode: Context.edit },
                }"
                >Edit</router-link
            >
            <SaveUtil></SaveUtil>
        </span>
        <router-view></router-view>
    </div>
</template>

<script>
    import { Context } from "../common.js";
    import SaveUtil from "../Utils/SaveUtil";
    export default {
        components: { SaveUtil },
        beforeRouteEnter(to, from, next) {
            Context.initUser().then(next);
        },
        beforeRouteUpdate(to, from, next) {
            Context.initUser().then(next);
        },
        data() {
            return {
                Context,
            };
        },
    };
</script>
