<template>
    <div class="w-100 h-100 wall-container">
        <WidgetList :base="WidgetBaseSimple"></WidgetList>
        <span class="wall-title col-12 col-md-4 col-lg-3">
            <span class="font-weight-bold text-primary">{{ wall.title }}</span>
        </span>
    </div>
</template>

<script>
    import WidgetList from "./WidgetList";
    import WidgetBaseSimple from "../Widgets/WidgetBaseSimple";

    export default {
        name: "WallView",
        components: { WidgetList },
        data() {
            return {
                WidgetBaseSimple,
                wall:
                    this.$store.state.walls.filter((wall) => wall.id == this.$route.params.wallId)[0] ||
                    this.$store.state.requestedWall,
            };
        },
    };
</script>

<style scoped>
    .wall-container {
        position: relative;
    }
    .wall-title {
        position: fixed;
        bottom: 0;
        left: 0;
    }
</style>
