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
                            v-show="$store.state.user.is_authenticated"
                            class="nav-link"
                            :to="{
                                name: $env.edit ? 'wallView' : 'wallEdit',
                                params: $route.params,
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
            <SaveUtil></SaveUtil>
            <div class="mx-5 text-secondary d-sm-none">
                <span v-if="!$env.wall && $store.state.user.is_authenticated">
                    Select or create a <span class="text-success font-weight-bold">wall</span> to continue
                </span>
            </div>
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
        <AlertUtil></AlertUtil>
        <router-view></router-view>
    </div>
</template>

<script>
    import SaveUtil from "./Utils/SaveUtil";
    import AlertUtil from "./Utils/AlertUtil";
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
        },
        created() {
            $(document).keyup((e) => {
                if (e.keyCode === 27) this.$env.closeOptions(); // esc
            });
        },
    };
</script>
