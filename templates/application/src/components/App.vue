<template>
    <div class="w-100 h-100 d-flex flex-column">
        <nav class="navbar navbar-expand-md navbar-light bg-light border-bottom">
            <router-link class="navbar-brand" :to="{ name: 'home' }">{{ $store.state.app.title }}</router-link>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <router-link class="nav-link" :to="{ name: 'home' }">Home </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            :to="{
                                name: $env.edit ? 'wallView' : 'wallEdit',
                                params: { wallId: $route.params.wallId },
                            }"
                            >{{ $env.edit ? "View" : "Edit" }}
                        </router-link>
                    </li>
                    <li class="nav-item">
                        <router-link
                            class="nav-link"
                            :to="{ name: $store.state.user.is_authenticated ? 'logout' : 'login' }"
                            >{{ $store.state.user.is_authenticated ? "Logout" : "Login" }}</router-link
                        >
                    </li>
                </ul>
            </div>
            <div v-show="!$store.state.wall" class="mx-5 text-secondary">
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
        <div class="h-100 workspace d-flex flex-column justify-content-between align-items-center overflow-hidden">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
            <div class="w-100 px-5 select-create">
                <SelectCreate @wallCreated="onCreateWall" v-if="$env.edit"></SelectCreate>
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
                    name: "wall",
                    params: {
                        wallId: wall.id,
                    },
                });
            },
        },
    };
</script>

<style scoped>
    .select-create {
        position: absolute;
        bottom: 0;
    }
</style>
