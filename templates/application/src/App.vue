<template>
    <div class="clearfix">
        <div class="base-layout-top">
            <div class="status-panel d-flex p-2 w-100 border-bottom justify-content-between">
                <small class="px-2 text-info">Widgets are not available. Select or create a wall to use widgets</small>
                <small class="text-secondary">
                    <strong v-if="Context.saving" class="text-secondary">Saving...</strong>
                    <strong v-else-if="Context.saved" class="text-success">Saved!</strong>
                    <strong v-else>Auto save</strong>
                </small>
            </div>
            <div class="d-flex control-panel p-1 w-100 border-top overflow-auto">
                <a @click.stop="Context.$emit('addBlankWidget', SimpleText)" class="btn btn-sm bg-light border mx-1 text-nowrap">Simple text</a>
                <a @click.stop="Context.$emit('addBlankWidget', URL)" class="btn btn-sm bg-light border mx-1 text-nowrap">URL</a>
                <a @click.stop="Context.$emit('addBlankWidget', Counter)" class="btn btn-sm bg-light border mx-1 text-nowrap">Counter</a>
                <a @click.stop="Context.$emit('addBlankWidget', SimpleList)" class="btn btn-sm bg-light border mx-1 text-nowrap">Simple list</a>
            </div>
        </div>

        <div class="base-layout-bottom">
            <Wall ref="wall" :wall="wall"></Wall>
        </div>
    </div>
</template>

<script>
    import SimpleText from "./components/Widgets/SimpleText";
    import URL from "./components/Widgets/URL";
    import Counter from "./components/Widgets/Counter";
    import SimpleList from "./components/Widgets/SimpleList";
    import Wall from "./components/Wall";
    import { Context } from "./common.js";

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
        Wall,
    };
    export default {
        components,
        created() {
            Context.$on("deleteWall", this.onDeleteWall);
            Context.initUserContext().then(()=>{

            })
        },
        data() {
            return {
                Context,
                ...components,
            };
        },
        methods: {

        },
    };
</script>

<style scoped>
    .base-layout {
        position: absolute;
        width: 100%;
        height: 100%;
    }
    .base-layout-bottom {
        z-index: 0;
    }
    .base-layout-top {
        z-index: 101;
    }
    .control-panel {
        position: absolute;
        bottom: 0;
    }
</style>
