<template>
    <div>
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
    import { API, Context, registerIdSystem, UpdateManager } from "../common.js";

    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };
    export default {
        components,
        created() {
            registerIdSystem(this, this.wall);
            Context.$on("deleteWidget", this.onDeleteRequest);
            Context.$on("addBlankWidget", this.onAddBlankWidget);
            Context.$on("deleteWall", this.onDeleteWall);
            Context.$on("addBlankWall", this.onAddBlankWall);
        },
        data() {
            var manager = new UpdateManager(this.wall.type, this.wall.id);
            return {
                Context,
                manager,
                ...components,
            };
        },
        props: {
            wall: {
                type: Object,
                required: true,
            },
            widgets: {
                type: Array,
                default: () => []
            },
        },
        methods: {
            onDeleteWall(wall) {
                if (confirm("Are you sure? Wall will be permanently removed!")) {
                    this.manager.delete();
                    Context.walls.splice(Context.walls.indexOf(wall), 1);
                    Context.$emit('wallDeleted')
                }
            },
            onAddBlankWall() {
                this.manager.create().then((response) => {
                    Context.walls.push(response);
                    Context.$emit('wallCreated')
                });
            },
            filterWidgets(klass) {
                return this.widgets.filter(function(widget) {
                    return widget.type == klass.type;
                });
            },
            onAddBlankWidget(klass) {
                new API(klass.type)
                    .create({
                        wall: this.wall.id,
                    })
                    .then((response) => {
                        this.widgets.push(response);
                    });
            },
            onDeleteWidget(widget) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
            },
        },
    };
</script>
