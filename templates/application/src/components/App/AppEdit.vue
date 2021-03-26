<template>
    <div class="w-100 h-100 d-flex flex-column">
        <nav class="navbar navbar-expand-md navbar-light bg-light">
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
                                name: 'wallView',
                                params: { wallId: $route.params.wallId },
                            }"
                            >View
                        </router-link>
                    </li>
                    <li></li>
                </ul>
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
        <AlertUtil></AlertUtil>
        <div class="h-100 container d-flex flex-column justify-content-between align-items-center">
            <router-view></router-view>
            <div class="m-2 p-1 w-100 shadow d-flex justify-content-between">
                <WallSelectCreate @createWall="onCreateWall" @deleteWall="onDeleteWall" :deleteWall="Boolean($store.state.walls)"></WallSelectCreate>
                <span class="overflow-auto d-flex">
                    <button
                        @click.stop="createWidget(SimpleText)"
                        class="mr-1 btn btn-sm bg-light border text-nowrap"
                        title="Add new widget of type Simple text"
                        :disabled="$env.state.lockChanges"
                    >
                        Text
                    </button>
                    <button
                        @click.stop="createWidget(URL)"
                        class="mr-1 btn btn-sm bg-light border text-nowrap"
                        title="Add new widget of type URL"
                        :disabled="$env.state.lockChanges"
                    >
                        URL
                    </button>
                    <button
                        @click.stop="createWidget(Counter)"
                        class="mr-1 btn btn-sm bg-light border text-nowrap"
                        title="Add new widget of type Counter"
                        :disabled="$env.state.lockChanges"
                    >
                        Counter
                    </button>
                    <button
                        @click.stop="createWidget(SimpleList)"
                        class="mr-1 btn btn-sm bg-light border text-nowrap"
                        title="Add new widget of type Simple list"
                        :disabled="$env.state.lockChanges"
                    >
                        List
                    </button>
                    <button
                        @click.stop="createWidget(SimpleSwitch)"
                        class="mr-1 btn btn-sm bg-light border text-nowrap"
                        title="Add new widget of type Switch"
                        :disabled="$env.state.lockChanges"
                    >
                        Switch
                    </button>
                </span>
            </div>
        </div>
    </div>
</template>

<script>
    import SaveUtil from "../Utils/SaveUtil";
    import AlertUtil from "../Utils/AlertUtil";
    import WallSelectCreate from "../Utils/WallSelectCreate";
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";
    import SimpleSwitch from "../Widgets/SimpleSwitch";

    export default {
        components: {
            SaveUtil,
            AlertUtil,
            WallSelectCreate,
        },
        data() {
            return {
                SimpleText,
                URL,
                Counter,
                SimpleList,
                SimpleSwitch,
            };
        },
        methods: {
            async onCreateWall() {
                var wall = await this.$store.dispatch("createWall");
                this.$env.dispatch("resolveWallCreated", wall);
            },
            async onDeleteWall() {
                if (confirm("Are you sure? Wall will be permanently removed!")) {
                    let wall = this.$store.state.walls.filter((w) => w.id == this.$route.params.wallId)[0]; // Order is important
                    await this.$store.dispatch("deleteInstance", wall);
                    this.$env.dispatch("resolveWallDeleted", wall);
                }
            },
            createWidget(klass) {
                this.$store.dispatch("createWidget", {
                    type: klass.type,
                    wall: this.$route.params.wallId,
                });
            },
        },
    };
</script>
