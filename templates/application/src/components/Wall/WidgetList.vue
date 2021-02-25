<template>
    <div class="w-100 h-100">
        <SimpleText v-for="widget of filterSimpleText" :key="widget.type + widget.id" :parent="true" :WidgetBase="WidgetBase" :widget="widget"> </SimpleText>
        <URL v-for="widget of filterURL" :key="widget.type + widget.id" :widget="widget" :WidgetBase="WidgetBase"> </URL>
        <Counter v-for="widget of filterCounter" :key="widget.type + widget.id" :widget="widget" :WidgetBase="WidgetBase"> </Counter>
        <SimpleList v-for="widget of filterSimpleList" :key="widget.type + widget.id" :widget="widget" :WidgetBase="WidgetBase"> </SimpleList>
    </div>
</template>

<script>
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";

    export default {
        name: "WidgetList",
        components: {
            SimpleText,
            URL,
            Counter,
            SimpleList,
        },
        props: {
            widgets: {
                type: Array,
                required: true,
            },
            WidgetBase: null,
        },
        methods: {
            filterWidgets(klass) {
                return this.widgets.filter(function(widget) {
                    return widget.type == klass.type;
                });
            },
        },
        computed: {
            filterSimpleText: () => {
                return this.filterWidgets(SimpleText);
            },
            filterURL: () => {
                return this.filterWidgets(URL);
            },
            filterCounter: () => {
                return this.filterWidgets(Counter);
            },
            filterSimpleList: () => {
                return this.filterWidgets(SimpleList);
            },
        },
    };
</script>
