<template>
    <div class="w-100 h-100 d-flex flex-column">
        <nav class="navbar navbar-expand-md navbar-light border-bottom">
            <a class="navbar-brand" :href="homeUrl">{{ $store.state.app.title }}</a>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a class="nav-link" :href="homeUrl">Home</a>
                    </li>
                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            :to="{
                                name: $env.edit ? 'wallView' : 'wallEdit',
                                params: $route.param,
                            }"
                            >{{ $env.edit ? "View" : "Edit" }}
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" :href="$store.state.user.is_authenticated ? logoutUrl : loginUrl">{{
                            $store.state.user.is_authenticated ? "Logout" : "Login"
                        }}</a>
                    </li>
                </ul>
            </div>
            <div v-show="!$env.wall" class="mx-5 text-secondary">
                <span v-if="$store.state.user.is_authenticated">
                    Select or create a <span class="text-success font-weight-bold">wall</span> to continue
                </span>
            </div>
            <SaveUtil></SaveUtil>
            <button
                class="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
        </nav>
        <div class="h-100 bg-light d-flex flex-column justify-content-between align-items-center overflow-hidden">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
            <div class="w-100 px-5 select-create-pos">
                <SelectCreate @wallCreated="onCreateWall" v-if="$env.edit && $store.state.user.is_authenticated"></SelectCreate>
            </div>
        </div>
    </div>
</template>

<script>
    import SaveUtil from "./Utils/SaveUtil";
    import AlertUtil from "./Utils/AlertUtil";
    import SelectCreate from "./Utils/SelectCreate";
    import router from "../modules/router";
    import $ from "jquery";

    export default {
        data() {
            return {
                homeUrl: process.env.VUE_APP_HOME,
                loginUrl: "/accounts/login/",
                logoutUrl: "/accounts/logout/",
            };
        },
        components: {
            SaveUtil,
            AlertUtil,
            SelectCreate,
        },
        created() {
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.closeOptions(); // esc
            });
        },
        methods: {
            onCreateWall(wall) {
                this.$io.alert("New wall has been created!", "success");
                router.push({
                    name: "wallEdit",
                    params: {
                        wallId: wall.id,
                    },
                });
            },
        },
    };
</script>

<style scoped>
    .select-create-pos {
        position: absolute;
        bottom: 0;
    }
</style>
