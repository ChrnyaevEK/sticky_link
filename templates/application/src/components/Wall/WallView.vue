<template>
    <div class="w-100 h-100">
        <WidgetList ref="widgets" :widgets="widgets" :WidgetBase="WidgetBaseSimple"></WidgetList>
        <span class="wall-title col-12 col-md-4 col-lg-3">
            <span class="font-weight-bold text-primary">{{ wall.title }}</span>
        </span>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseSimple from '../Widgets/WidgetBaseSimple'
    import { API, Context, UpdateManager } from "../../common.js";
    import { validateWall } from "./wall.js";

    export default {
        components: {WidgetList},
        beforeRouteEnter(to, from, next) {
            if (validateWall(to.params.wallId)) {
                this.initiateWall(to.params.wallId).then(next);
            } else {
                next({
                    name: "app",
                });
            }
        },
        beforeRouteUpdate(to, from, next) {
            if (validateWall(to.params.wallId)) {
                this.initiateWall(to.params.wallId).then(next);
            } else {
                next({
                    name: "app",
                });
            }
        },
        data() {
            return {
                Context,
                manager: {},
                wall: {},
                widgets: [],
                ready: false,
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
    .wall-title {
        position: absolute;
        bottom: 0;
        left: auto;
    }
</style>
