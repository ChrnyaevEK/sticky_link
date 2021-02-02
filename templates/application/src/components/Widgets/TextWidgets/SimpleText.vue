<template>
    <WidgetBase v-bind="{ ...$props, ...$attrs }"></WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    // import API from "../../../common.js";
    export default {
        name: "SimpleText",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        components: {
            WidgetBase,
        },
    };
</script>
