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
        <AlertUtil></AlertUtil>
        <router-view></router-view>
        <div class="w-100 p-1 d-flex bg-white border-top">
            <WallSelectCreate @createWall="onCreateWall" @deleteWall="onDeleteWall"></WallSelectCreate>
            <div class="d-flex w-100 overflow-auto">
                <button @click.stop="env.$emit('addWidget', SimpleText)" class="mr-1 btn btn-sm bg-light border text-nowrap" title="Add new widget of type Simple text" :disabled="!$env.state.lockWidgets">
                    Simple text
                </button>
                <button @click.stop="env.$emit('addWidget', URL)" class="mr-1 btn btn-sm bg-light border text-nowrap" title="Add new widget of type URL" :disabled="!$env.state.lockWidgets">
                    URL
                </button>
                <button @click.stop="env.$emit('addWidget', Counter)" class="mr-1 btn btn-sm bg-light border text-nowrap" title="Add new widget of type Counter" :disabled="!$env.state.lockWidgets">
                    Counter
                </button>
                <button @click.stop="env.$emit('addWidget', SimpleList)" class="mr-1 btn btn-sm bg-light border text-nowrap" title="Add new widget of type Simple list" :disabled="!$env.state.lockWidgets">
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

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
        SaveUtil,
        AlertUtil,
        WallSelectCreate,
    };
    export default {
        components,
        data() {
            return components;
        },
        methods: {
            onCreateWall() {
                this.$store.dispatch("createWall").then((wall) => {
                    this.$router.push({
                        name: "wallEdit",
                        params: {
                            wallId: wall.id,
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
                    this.$store
                        .dispatch("deleteWall", {
                            id: this.$route.params.wallId,
                        })
                        .then(() => {
                            this.$router.push(
                                this.$store.state.walls.length
                                    ? {
                                          name: "wallEdit",
                                          params: {
                                              wallId: this.$store.state.walls[0].id,
                                          },
                                      }
                                    : {
                                          name: "appEmpty",
                                      }
                            );
                            this.$env.dispatch("showAlert", {
                                msg: "Wall has been deleted!",
                                klass: "success",
                            });
                        });
                }
            },
            createWidget(klass){
                this.$env.dispatch('lockWidgets')
                this.$store.dispatch('createWidget', klass)
            }
        },
    };
</script>

<style scoped>
    .wall-placeholder {
        position: relative;
    }
</style>
