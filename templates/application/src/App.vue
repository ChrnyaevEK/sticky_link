<template>
    <div class="w-100 h-100 overflow-auto">
        <div class="w-100 p-1 d-flex border-bottom justify-content-between bg-white fixed-top">
            <small class="text-info">Widgets are not available. Select or create a wall to use widgets</small>
            <small class="text-secondary">
                <strong v-if="Context.saving" class="text-secondary">Saving...</strong>
                <strong v-else-if="Context.saved" class="text-success">Saved!</strong>
                <strong v-else>Auto save</strong>
            </small>
        </div>
        <router-view></router-view>
        <div class="w-100 p-1 d-flex bg-white fixed-bottom border-top">
            <div class="btn-group dropup p-1">
                <button class="btn btn-sm dropdown-toggle" type="button" id="wall-list" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Walls
                </button>
                <div class="dropdown-menu" aria-labelledby="wall-list">
                    <router-link class="dropdown-item btn-sm" v-for="wall of Context.walls" :key="wall.id" :to="`/app/wall/${wall.id}`">{{ wall.title }}</router-link>
                </div>
            </div>
            <div class="d-flex p-1 w-100 overflow-auto">
                <a @click.stop="Context.$emit('addBlankWidget', SimpleText)" class="btn btn-sm bg-light border mx-1 text-nowrap">Simple text</a>
                <a @click.stop="Context.$emit('addBlankWidget', URL)" class="btn btn-sm bg-light border mx-1 text-nowrap">URL</a>
                <a @click.stop="Context.$emit('addBlankWidget', Counter)" class="btn btn-sm bg-light border mx-1 text-nowrap">Counter</a>
                <a @click.stop="Context.$emit('addBlankWidget', SimpleList)" class="btn btn-sm bg-light border mx-1 text-nowrap">Simple list</a>
            </div>
        </div>
    </div>
</template>

<script>
    import SimpleText from "./components/Widgets/SimpleText";
    import URL from "./components/Widgets/URL";
    import Counter from "./components/Widgets/Counter";
    import SimpleList from "./components/Widgets/SimpleList";
    import { Context } from "./common.js";

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };
    export default {
        components,
        created() {
            Context.$on("wallDeleted", this.onWallDeleted);
            Context.$on("wallCreated", this.onWallCreated);
            Context.initUser();
        },
        data() {
            return {
                Context,
                ...components,
            };
        },
        methods: {
            onWallCreated() {
                console.log("wall created");
            },
            onWallDeleted() {
                console.log("wall created");
            },
        },
    };
</script>

<style scoped>
    .widget-table {
        display: table;
    }
    .widget-table-cell {
        display: table-cell;
        vertical-align: middle;
    }
    .w-90 {
        width: 90% !important;
    }
    .h-90 {
        height: 90% !important;
    }
</style>
