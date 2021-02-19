<template>
    <div class="w-100 h-100">
        <SimpleText v-for="widget of filterWidgets(SimpleText)" :key="widget.type + widget.id" :widget="widget"> </SimpleText>
        <URL v-for="widget of filterWidgets(URL)" :key="widget.type + widget.id" :widget="widget"> </URL>
        <Counter v-for="widget of filterWidgets(Counter)" :key="widget.type + widget.id" :widget="widget"> </Counter>
        <SimpleList v-for="widget of filterWidgets(SimpleList)" :key="widget.type + widget.id" :widget="widget"> </SimpleList>
    </div>
</template>

<script>
    import SimpleText from "./Widgets/SimpleText";
    import URL from "./Widgets/URL";
    import Counter from "./Widgets/Counter";
    import SimpleList from "./Widgets/SimpleList";
    import { API, Context, UpdateManager } from "../common.js";

    Context.$on("addBlankWall", () => {
        new API("wall").create().then((response) => {
            Context.$emit('wallCreated', response)
        });
    });

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };

    export default {
        components,
        created() {
            Context.$on("widgetDeleted", this.onWidgetDeleted);
            Context.$on("widgetCreated", this.onWidgetCreated);
            this.initiateWall(this.$route.params.wall_id);
        },
        data() {
            return {
                Context,
                manager: {},
                wall: {},
                widgets: [],
                ...components,
            };
        },
        methods: {
            initiateWall(id) {
                this.$set(this, "manager", new UpdateManager("wall", id));
                this.manager.retrieve().then((response) => {
                    this.$set(this, "wall", response.wall);
                    this.$set(this, "widgets", response.widgets);
                });
            },
            onDeleteWall() {
                if (confirm("Are you sure? Wall will be permanently removed!")) {
                    this.manager.delete();
                    Context.$emit('wallDeleted', this.wall)
                }
            },
            filterWidgets(klass) {
                return this.widgets.filter(function(widget) {
                    return widget.type == klass.type;
                });
            },
            onWidgetCreated(widget) {
                this.widgets.push(widget);
            },
            onWidgetDeleted(widget) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
            },
        },
        watch: {
            $route(to) {
                this.initiateWall(to.params.wall_id);
            },
        },
    };
</script>
