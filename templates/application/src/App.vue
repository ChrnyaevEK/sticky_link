<template>
    <div class="w-100 h-100 d-flex flex-column">
        <div
            class="w-100 p-1 d-flex border-bottom justify-content-between bg-white"
        >
            <span class="small font-weight-bold">
                <span class="text-info" v-if="!validWall"
                    >Widgets are not available. Select or create a wall to use
                    widgets</span
                >
                <span v-else> Sticky link </span>
                <span v-if="Context.saving" class="text-secondary"
                    >Saving...</span
                >
                <span v-else-if="Context.saved" class="text-success"
                    >Saved!</span
                >
                <span v-else class="text-secondary">Auto save</span>
            </span>

            <small>
                <router-link
                    v-if="$route.query.mode == Context.edit"
                    class="mx-1"
                    :to="{
                        name: 'wall',
                        params: { wallId: $route.params.wallId },
                        query: { mode: Context.view },
                    }"
                >
                    View mode
                </router-link>

                <router-link
                    v-if="$route.query.mode == Context.view"
                    :to="{
                        name: 'wall',
                        params: { wallId: $route.params.wallId },
                        query: { mode: Context.edit },
                    }"
                    >Open editor</router-link
                >
            </small>
        </div>
        <router-view style="position: relative;"></router-view>
        <div
            v-if="$route.query.mode == Context.edit"
            class="w-100 p-1 d-flex bg-white border-top"
        >
            <div class="btn-group dropup p-1">
                <button
                    class="btn btn-sm dropdown-toggle"
                    type="button"
                    id="wall-list"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                >
                    Walls
                </button>
                <div class="dropdown-menu" aria-labelledby="wall-list">
                    <router-link
                        class="dropdown-item btn-sm"
                        v-for="wall of Context.walls"
                        :class="wall.id == $route.params.wallId ? 'active' : ''"
                        :key="wall.id"
                        :to="{
                            name: 'wall',
                            params: { wallId: wall.id },
                            query: { mode: Context.edit },
                        }"
                        >{{ wall.title }}</router-link
                    >
                </div>
                <a
                    class="btn btn-sm border"
                    @click="Context.$emit('addBlankWall')"
                >
                    <i class="fas fa-plus"></i>
                </a>
            </div>
            <div class="d-flex p-1 w-100 overflow-auto" v-if="validWall">
                <a
                    @click.stop="Context.$emit('addBlankWidget', SimpleText)"
                    class="btn btn-sm bg-light border mx-1 text-nowrap"
                    >Simple text</a
                >
                <a
                    @click.stop="Context.$emit('addBlankWidget', URL)"
                    class="btn btn-sm bg-light border mx-1 text-nowrap"
                    >URL</a
                >
                <a
                    @click.stop="Context.$emit('addBlankWidget', Counter)"
                    class="btn btn-sm bg-light border mx-1 text-nowrap"
                    >Counter</a
                >
                <a
                    @click.stop="Context.$emit('addBlankWidget', SimpleList)"
                    class="btn btn-sm bg-light border mx-1 text-nowrap"
                    >Simple list</a
                >
            </div>
        </div>
    </div>
</template>

<script>
    import SimpleText from "./components/Widgets/SimpleText";
    import URL from "./components/Widgets/URL";
    import Counter from "./components/Widgets/Counter";
    import SimpleList from "./components/Widgets/SimpleList";
    import { Context } from "./common.js";

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };
    export default {
        components,
        created() {
            Context.$on("wallDeleted", this.onWallDeleted);
            Context.$on("wallCreated", this.onWallCreated);
            Context.$on("routeRequest", this.onRouteRequest);
            Context.initUser().then(this.validateWall);
        },
        data() {
            return {
                Context,
                ...components,
                validWall: false,
            };
        },
        methods: {
            onWallCreated(wall) {
                Context.walls.push(wall);
            },
            onWallDeleted(wall) {
                Context.walls.splice(Context.walls.indexOf(wall), 1);
            },
            onRouteRequest(callback) {
                callback(this.$route);
            },
            validateWall() {
                this.validWall = Context.walls.some((w) => {
                    return String(w.id) == this.$route.params.wallId;
                });
            },
        },
        watch: {
            $route() {
                this.validateWall();
            },
        },
    };
</script>
