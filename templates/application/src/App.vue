<template>
    <div class="w-100 h-100 d-flex flex-column" >
        <span class=" w-100 p-1 bg-white border-bottom">
            <span
                class="text-secondary"
                v-if="$route.params.wallId === undefined"
                >This is Ground Control! Try to select or create a
                <span class="text-success font-weight-bold">wall</span>...</span
            >
            <span v-else>
                <a href="/" class="m-3"> Sticky link </a>
                <router-link
                    class="mr-3"
                    v-if="$route.query.mode == Context.edit"
                    :to="{
                        name: 'wall',
                        params: { wallId: $route.params.wallId },
                        query: { mode: Context.view },
                    }"
                >
                    View
                </router-link>
                <router-link
                    class="mr-3"
                    v-if="$route.query.mode == Context.view"
                    :to="{
                        name: 'wall',
                        params: { wallId: $route.params.wallId },
                        query: { mode: Context.edit },
                    }"
                    >Edit</router-link
                >
                <span class="mr-3 small font-weight-bold text-secondary">
                    <span v-if="Context.saving">Saving...</span>
                    <span v-else-if="Context.saved" class="text-success"
                        >Saved!</span
                    >
                    <span v-else>Auto save</span>
                </span>
            </span>
        </span>
        <span
            class="w-100 m-0 alert alert-dismissible fade show"
            v-show="showAlert"
            :class="'alert-' + alertClass || 'info'"
            >{{ alertMessage }}
            <a class="close btn" aria-label="Close" @click="showAlert = false">
                <span aria-hidden="true">&times;</span>
            </a></span
        >
        <router-view
            v-if="$route.params.wallId !== undefined"
            class="wall-placeholder"
        ></router-view>
        <div
            v-else
            id="major-tom"
            class="w-100 h-100 h1 text-info d-flex justify-content-center align-items-center"
        >
            <i
                class="fas fa-user-astronaut"
                title="Now it's time to leave the capsule if you dare... Go for a wall!"
            ></i>
        </div>
        <div
            v-if="
                $route.query.mode == Context.edit ||
                    $route.query.mode == undefined
            "
            class="w-100 p-1 d-flex bg-white border-top"
        >
            <div class="btn-group dropup">
                <a
                    class="btn btn-sm dropdown-toggle"
                    id="wall-list"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                    title="Select any wall to open for edition"
                >
                    Walls
                </a>
                <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                    <router-link
                        class="dropdown-item btn btn-sm"
                        v-for="wall of Context.walls"
                        :key="wall.id"
                        :class="{ active: wall.id == $route.params.wallId }"
                        :to="{
                            name: 'wall',
                            params: { wallId: wall.id },
                            query: { mode: Context.edit },
                        }"
                        >{{ wall.title }}</router-link
                    >
                </div>
                <a
                    class="mr-1 btn btn-sm btn-success border"
                    @click="Context.$emit('addBlankWall')"
                    title="Add new wall"
                >
                    <i class="fas fa-plus"></i>
                </a>
                <a
                    v-if="$route.params.wallId !== undefined"
                    class="mr-1 btn btn-sm btn-danger border"
                    @click.stop="Context.$emit('deleteWall')"
                    title="Delete current wall"
                >
                    <i class="fas fa-trash"></i>
                </a>
            </div>
            <div
                class="d-flex w-100 overflow-auto"
                v-if="$route.params.wallId !== undefined"
            >
                <button
                    @click.stop="Context.$emit('addBlankWidget', SimpleText)"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Simple text"
                    :disabled="lockWidgetCreation"
                >
                    Simple text
                </button>
                <button
                    @click.stop="Context.$emit('addBlankWidget', URL)"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type URL"
                    :disabled="lockWidgetCreation"
                >
                    URL
                </button>
                <button
                    @click.stop="Context.$emit('addBlankWidget', Counter)"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Counter"
                    :disabled="lockWidgetCreation"
                >
                    Counter
                </button>
                <button
                    @click.stop="Context.$emit('addBlankWidget', SimpleList)"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Simple list"
                    :disabled="lockWidgetCreation"
                >
                    Simple list
                </button>
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
        beforeRouteEnter(to, from, next) {
            Context.initUser().then(next);
        },
        beforeRouteUpdate(to, from, next) {
            Context.initUser().then(next);
        },
        created() {
            Context.$on("wallDeleted", this.onWallDeleted);
            Context.$on("wallCreated", this.onWallCreated);
            Context.$on("routeRequest", this.onRouteRequest);
            Context.$on("showAlert", this.onShowAlert);
            Context.$on("lockWidgetCreation", this.onLockWidgetCreation);
            Context.$on("unlockWidgetCreation", this.onUnlockWidgetCreation);
        },
        data() {
            return {
                Context,
                ...components,
                showAlert: false,
                alertMessage: "",
                alertClass: "",
                lockWidgetCreation: false,
            };
        },
        methods: {
            onWallCreated(wall) {
                this.$router.push({
                    name: "wall",
                    params: {
                        wallId: wall.id,
                    },
                    query: {
                        mode: Context.edit,
                    },
                });
                Context.$emit(
                    "showAlert",
                    `New wall has been created!`,
                    "success"
                );
            },
            onWallDeleted(wall) {
                Context.$emit(
                    "showAlert",
                    `Wall "${wall.title}" has been deleted!`,
                    "success"
                );
                this.validateState();
            },
            onShowAlert(alertMessage, alertClass) {
                this.alertMessage = alertMessage;
                this.alertClass = alertClass;
                this.showAlert = true;
            },
            onLockWidgetCreation() {
                this.lockWidgetCreation = true;
            },
            onUnlockWidgetCreation() {
                this.lockWidgetCreation = false;
            },
            onRouteRequest(callback) {
                callback(this.$route);
            },
        },
    };
</script>

<style scoped>
    .wall-placeholder {
        position: relative;
    }
</style>
