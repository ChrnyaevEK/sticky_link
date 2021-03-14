<template>
    <div class="w-100 h-100">
        <SimpleText
            v-for="widget of filterWidget(SimpleText)"
            :key="widget.type + widget.id"
            :parent="true"
            :base="base"
            :widget="widget"
        >
        </SimpleText>
        <URL v-for="widget of filterWidget(URL)" :key="widget.type + widget.id" :widget="widget" :base="base"> </URL>
        <Counter v-for="widget of filterWidget(Counter)" :key="widget.type + widget.id" :widget="widget" :base="base">
        </Counter>
        <SimpleList
            v-for="widget of filterWidget(SimpleList)"
            :key="widget.type + widget.id"
            :widget="widget"
            :base="base"
        >
        </SimpleList>
    </div>
</template>

<script>
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };

    export default {
        name: "WidgetList",
        components,
        props: {
            base: null,
        },
        data() {
            return components;
        },
        methods: {
            filterWidget(klass) {
                return this.$store.state.widgets.filter(function(widget) {
                    return widget.type == klass.type;
                });
            },
        },
    };
</script>
