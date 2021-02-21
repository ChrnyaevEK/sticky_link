<template>
    <div class="w-100 h-100">
        <SimpleText
            v-for="widget of filterWidgets(SimpleText)"
            :key="widget.type + widget.id"
            :parent="true"
            :widget="widget"
        >
        </SimpleText>
        <URL
            v-for="widget of filterWidgets(URL)"
            :key="widget.type + widget.id"
            :widget="widget"
        >
        </URL>
        <Counter
            v-for="widget of filterWidgets(Counter)"
            :key="widget.type + widget.id"
            :widget="widget"
        >
        </Counter>
        <SimpleList
            v-for="widget of filterWidgets(SimpleList)"
            :key="widget.type + widget.id"
            :widget="widget"
        >
        </SimpleList>
    </div>
</template>

<script>
    import SimpleText from "./Widgets/SimpleText";
    import URL from "./Widgets/URL";
    import Counter from "./Widgets/Counter";
    import SimpleList from "./Widgets/SimpleList";
    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };

    export default {
        name: "WidgetList",
        components,
        data() {
            return components;
        },
        props: {
            widgets: {
                type: Array,
                required: true,
            },
        },
        methods: {
            filterWidgets(klass) {
                return this.widgets.filter(function(widget) {
                    return widget.type == klass.type;
                });
            },
        },
    };
</script>
