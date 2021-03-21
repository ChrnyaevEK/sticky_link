<template>
    <div class="w-100 h-100">
        <component
            v-for="widget of $store.state.widgets"
            :is="typed(widget)"
            :parent="true"
            :base="base"
            :key="widget.type + widget.id"
            :widget="widget"
        >
        </component>
    </div>
</template>

<script>
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";

    export default {
        name: "WidgetList",
        props: {
            base: null,
        },
        methods: {
            typed(widget) {
                return [SimpleText, URL, Counter, SimpleList].filter((klass) => widget.type == klass.type)[0];
            },
        },
    };
</script>
