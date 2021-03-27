<template>
    <div class="m-2 p-1 w-100 shadow d-flex justify-content-between border">
        <div class="btn-group dropup bg-white">
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
            <div class="mr-1 dropdown-menu" aria-labelledby="wall-list" v-if="$store.state.walls">
                <router-link
                    class="dropdown-item btn btn-sm"
                    v-for="wall of $store.state.walls"
                    :key="wall.id"
                    :class="{ active: wall.id == $route.params.wallId, 'text-secondary': !wall.title }"
                    :to="{
                        name: 'wall',
                        params: { wallId: wall.id },
                    }"
                    >{{ wall.title || "[no title]" }}</router-link
                >
            </div>
            <a
                v-if="createWall"
                class="mr-1 btn btn-sm btn-success border"
                @click="createWall"
                title="Add new wall"
                :disabled="$env.changesLocked"
            >
                <i class="fas fa-plus"></i>
            </a>
            <a
                v-if="deleteWall"
                class="mr-1 btn btn-sm btn-danger border"
                @click.stop="deleteWall"
                title="Delete current wall"
                :disabled="$env.changesLocked"
            >
                <i class="fas fa-trash"></i>
            </a>
        </div>
        <span class="overflow-auto d-flex" v-if="$store.state.wall">
            <button
                @click.stop="createInstance('container')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add Container to hold widgets"
                :disabled="$env.changesLocked"
            >
                Container
            </button>
            <button
                @click.stop="createInstance('simple_text')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Simple text"
                :disabled="$env.changesLocked"
            >
                Text
            </button>
            <button
                @click.stop="createInstance('url')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type URL"
                :disabled="$env.changesLocked"
            >
                URL
            </button>
            <button
                @click.stop="createInstance('counter')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Counter"
                :disabled="$env.changesLocked"
            >
                Counter
            </button>
            <button
                @click.stop="createInstance('simple_list')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Simple list"
                :disabled="$env.changesLocked"
            >
                List
            </button>
            <button
                @click.stop="createInstance('simple_switch')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Switch"
                :disabled="$env.changesLocked"
            >
                Switch
            </button>
        </span>
    </div>
</template>
<script>
    export default {
        name: "SelectCreate",
        props: {
            allowDeleteWall: {
                type: Boolean,
                default: true,
            },
        },
        methods: {
            async createInstance(type) {
                switch (type) {
                    case "container":
                        if (this.$store.state.wall && this.$store.state.containers) {
                            var index = 0;
                            for (var container of this.$store.state.containers) {
                                if (container.index > index) {
                                    index = container.index + 1;
                                }
                            }
                            var wallId = this.$store.state.wall.id;
                            await this.$store.dispatch("createInstance", { type, wall: wallId, index });
                        }
                        break;
                    default:
                        var containerId = this.$store.state.container.id;
                        await this.$store.dispatch("createInstance", { type, container: containerId });
                        break;
                }
            },
            async createWall() {
                var wall = await this.$store.dispatch("createInstance", { type: "wall" });
                this.$emit("wallCreated", wall);
            },
            async deleteWall() {
                if (this.$store.state.wall && confirm("Are you sure? Wall will be permanently removed!")) {
                    await this.$store.dispatch("deleteInstance", this.$store.state.wall);
                    this.$emit("wallDeleted");
                }
            },
        },
    };
</script>
