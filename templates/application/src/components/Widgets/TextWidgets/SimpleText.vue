<template>
    <WidgetBase v-bind="{ ...$props, ...$attrs }">

    </WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    // import API from "../../../common.js";
    export default {
        name: "SimpleText",
        props: {
            max_length: {
                type: Number,
                required: false,
            },
            text_content: {
                type: String,
                required: false,
            },
        },
        components: {
            WidgetBase,
        },
    };
</script>
