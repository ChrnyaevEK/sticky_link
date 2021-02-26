<template>
    <div class="w-100 h-100 d-flex flex-column">
        <span class=" w-100 p-1 bg-white border-bottom">
            <a href="/" class="m-3"> Sticky link </a>
            <router-link
                class="mr-3"
                :to="{
                    name: 'wallView',
                    params: { wallId: $route.params.wallId },
                }"
            >
                View
            </router-link>
            <SaveUtil></SaveUtil>
        </span>
        <span class="w-100 m-0 alert alert-dismissible fade show" v-show="showAlert" :class="'alert-' + alertClass || 'info'"
            >{{ alertMessage }}
            <a class="close btn" aria-label="Close" @click="showAlert = false">
                <span aria-hidden="true">&times;</span>
            </a></span
        >
        <router-view></router-view>
        <div class="w-100 p-1 d-flex bg-white border-top">
            <WallSelectCreate></WallSelectCreate>
            <div class="d-flex w-100 overflow-auto">
                <button
                    @click.stop="Context.$emit('addBlankWidget', SimpleText)"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Simple text"
                    :disabled="lockWidgetCreation"
                >
                    Simple text
                </button>
                <button @click.stop="Context.$emit('addBlankWidget', URL)" class="mr-1 btn btn-sm bg-light border text-nowrap" title="Add new widget of type URL" :disabled="lockWidgetCreation">
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
    import SaveUtil from "../Utils/SaveUtil";
    import WallSelectCreate from "../Utils/WallSelectCreate";
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";
    import { Context } from "../../common.js";

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
        SaveUtil,
        WallSelectCreate,
    };
    export default {
        components,
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
                    name: "wallEdit",
                    params: {
                        wallId: wall.id,
                    },
                });
                Context.$emit("showAlert", `New wall has been created!`, "success");
            },
            onWallDeleted(wall) {
                Context.$emit("showAlert", `Wall "${wall.title}" has been deleted!`, "success");
                this.$router.push(Context.walls.length ? {
                    name: "wallEdit",
                    params: {
                        wallId: Context.walls[0].id,
                    },
                }: {
                    name: "app"
                });
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
