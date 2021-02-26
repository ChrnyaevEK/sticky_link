<template>
    <div class="w-100 h-100 wall-container" v-if="dataReady">
        <WidgetList ref="widgets" :widgets="widgets" :base="WidgetBaseSimple"></WidgetList>
        <span class="wall-title col-12 col-md-4 col-lg-3">
            <span class="font-weight-bold text-primary">{{ wall.title }}</span>
        </span>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseSimple from "../Widgets/WidgetBaseSimple";
    import { Context, UpdateManager } from "../../common.js";

    export default {
        components: { WidgetList },
        created() {
            var manager = new UpdateManager("wall", this.$route.params.wallId);
            return manager.retrieve().then((response) => {
                this.$set(this, "manager", manager);
                this.$set(this, "wall", response.wall);
                this.$set(this, "widgets", response.widgets);
                this.dataReady = true
            });
        },
        data() {
            return {
                Context,
                WidgetBaseSimple,
                manager: undefined,
                wall: undefined,
                widgets: undefined,
                dataReady: false,
            };
        },
        methods: {
            initiateWall(id) {
                this.$set(this, "manager", new UpdateManager("wall", id));
                return this.manager.retrieve().then((response) => {
                    this.$set(this, "wall", response.wall);
                    this.$set(this, "widgets", response.widgets);
                });
            },
        },
    };
</script>

<style scoped>
    .wall-container {
        position: relative;
    }
    .wall-title {
        position: absolute;
        bottom: 0;
        left: auto;
    }
</style>
