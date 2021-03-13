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
        <div class="w-100 h-100 d-flex flex-column">
            <AlertUtil></AlertUtil>
            <router-view></router-view>
        </div>        
        <div class="w-100 p-1 d-flex bg-white border-top">
            <WallSelectCreate @createWall="onCreateWall" @deleteWall="onDeleteWall"></WallSelectCreate>
            <div class="d-flex w-100 overflow-auto">
                <button
                    @click.stop="createWidget(SimpleText)"
                    class="mr-1 btn btn-sm bg-light border text-nowrap"
                    title="Add new widget of type Simple text"
                    :disabled="$env.state.lockChanges"
                >
                    Simple text
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
                    Simple list
                </button>
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
            };
        },
        beforeRouteUpdate(to, from, next) {
            // from here all walls are valid
            this.$store.dispatch("fetchWidgets", to.params.wallId).then(next);
        },
        methods: {
            onCreateWall() {
                this.$store.dispatch("createWall").then((response) => {
                    this.$router.push({
                        name: "wallEdit",
                        params: {
                            wallId: response.id,
                        },
                    });
                    this.$env.dispatch("showAlert", {
                        msg: "New wall has been created!",
                        klass: "success",
                    });
                });
            },
            onDeleteWall() {
                if (confirm("Are you sure? Wall will be permanently removed!")) {
                    let wall = this.$store.state.walls.filter((w) => w.id == this.$route.params.wallId)[0];
                    this.$store.dispatch("deleteInstance", wall).then(()=>{
                        this.$env.dispatch("resolveWallDeleted");
                    })
                }
            },
            createWidget(klass) {
                this.$store
                    .dispatch("createWidget", {
                        type: klass.type,
                        wall: this.$route.params.wallId,
                    })
            },
        },
    };
</script>

<style scoped>
    .wall-placeholder {
        position: relative;
    }
</style>
