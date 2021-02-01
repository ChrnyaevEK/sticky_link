<template>
    <WidgetBase :id="id"></WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    export default {
        name: "SimpleTextWidget",
        props: {
            id: {
                type: String,
                required: true,
            },
        },
        components: {
            WidgetBase,
        },
    };
</script>
