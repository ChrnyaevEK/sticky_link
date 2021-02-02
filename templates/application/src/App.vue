<template>
    <div>
        <Wall :id="1"></Wall>
    </div>
</template>

<script>
import Wall from "./components/Wall";
export default {
    name: "App",
    components: {
        Wall,
    },
};
</script>
