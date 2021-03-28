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
                                name: 'wall',
                                query: { view: $env.edit ? true : undefined },
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
        <div class="h-100 container d-flex flex-column justify-content-between align-items-center overflow-hidden">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
            <SelectCreate @wallCreated="onCreateWall" v-if="$env.edit"></SelectCreate>
        </div>
    </div>
</template>

<script>
    import SaveUtil from "./Utils/SaveUtil";
    import AlertUtil from "./Utils/AlertUtil";
    import SelectCreate from "./Utils/SelectCreate";
    import router from "../router";

    export default {
        components: {
            SaveUtil,
            AlertUtil,
            SelectCreate,
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
