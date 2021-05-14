<template>
    <div class="p-1 w-100 shadow d-flex justify-content-between border bg-white">
        <div class="btn-group dropup">
            <div v-if="$store.state.walls">
                <a
                    class="btn btn-sm dropdown-toggle"
                    id="wall-list"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                    title="Select wall to edit"
                >
                    Walls
                </a>
                <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                    <router-link
                        class="dropdown-item btn btn-sm"
                        v-for="wall of $store.state.walls"
                        :key="wall.id"
                        :class="{ active: wall.id == $env.state.wall.id, 'text-secondary': !wall.title }"
                        :to="{
                            name: 'wallEdit',
                            params: { wallId: wall.id },
                        }"
                        >{{ wall.title }}</router-link
                    >
                </div>
            </div>
            <button
                class="mr-1 btn btn-sm btn-success text-white border"
                @click="createWall"
                title="Add new wall"
                :disabled="$env.state.changesLock"
            >
                <i class="fas fa-plus"></i>
            </button>
            <button
                v-if="$env.state.wall"
                class="mr-1 btn btn-sm btn-default"
                @click.stop="$env.dispatch('openOptions', $env.state.wall)"
                :disabled="$env.state.changesLock"
            >
                <i class="fas fa-ellipsis-v"></i>
            </button>
            <div v-if="$store.state.ports && $env.state.wall">
                <a
                    class="btn btn-sm dropdown-toggle"
                    id="wall-list"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                    title="Select port to edit"
                >
                    Ports
                </a>
                <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
                    <a
                        class="dropdown-item btn btn-sm"
                        v-for="port of $store.state.ports"
                        :key="port.id"
                        @click="portSelected(port)"
                        :title="`Visit counter: ${port.visited}`"
                        >{{ port.title }} <small>{{ port.visited }}</small>
                    </a>
                </div>
            </div>
            <button
                v-if="$store.state.ports && $env.state.wall"
                class="mr-1 btn btn-sm btn-success text-white border"
                @click="createPort"
                title="Add new port"
                :disabled="$env.state.changesLock"
            >
                <i class="fas fa-plus"></i>
            </button>
        </div>
        <span class="overflow-auto scrollbar-hidden d-flex" v-if="$env.state.wall">
            <button
                @click.stop="createInstance('container')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add Container to hold widgets"
                :disabled="$env.state.changesLock"
            >
                Container
            </button>
            <button
                @click.stop="createInstance('simple_text')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Simple text"
                :disabled="$env.state.changesLock"
            >
                Text
            </button>
            <button
                @click.stop="createInstance('url')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type URL"
                :disabled="$env.state.changesLock"
            >
                URL
            </button>
            <button
                @click.stop="createInstance('counter')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Counter"
                :disabled="$env.state.changesLock"
            >
                Counter
            </button>
            <button
                @click.stop="createInstance('simple_list')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Simple list"
                :disabled="$env.state.changesLock"
            >
                List
            </button>
            <button
                @click.stop="createInstance('simple_switch')"
                class="mr-1 btn btn-sm bg-light border text-nowrap"
                title="Add new widget of type Switch"
                :disabled="$env.state.changesLock"
            >
                Switch
            </button>
        </span>
    </div>
</template>
<script>
    export default {
        name: "SelectCreate",
        methods: {
            async createInstance(type) {
                switch (type) {
                    case "container":
                        if (this.$env.state.wall) {
                            let index = 0;
                            for (let container of this.$store.state.containers) {
                                if (container.index > index) {
                                    index = container.index + 1;
                                }
                            }
                            await this.$store.dispatch("createInstance", { type, wall: this.$env.state.wall.id, index });
                        }
                        break;
                    default:
                        await this.$store.dispatch("createInstance", { type, container: this.$env.state.container.id });
                        this.$store.dispatch("recalculateWidgets", this.$env.state.container);
                        break;
                }
            },
            async createWall() {
                var wall = await this.$store.dispatch("createInstance", { type: "wall" });
                this.$emit("wallCreated", wall);
            },
            async createPort() {
                var port = await this.$store.dispatch("createInstance", { type: "port", wall: this.$env.state.wall.id });
                this.$emit("portSelected", port);
            },
            portSelected(port) {
                this.$emit("portSelected", port);
            },
        },
    };
</script>
