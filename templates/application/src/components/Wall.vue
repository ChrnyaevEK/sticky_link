<template>
    <div class="flex-grow-1 row w-100">
        <div class="col-12 col-md-2">
            <p class="d-flex justify-content-between p-2">
                <small class="text-secondary">Auto save</small>
                <small v-show="Shared.saving"><strong class="text-secondary">Saving...</strong></small>
                <small v-show="Shared.saved"><strong class="text-success">Saved!</strong></small>
            </p>

            <div id="wall-widget-selector" role="tablist" aria-multiselectable="true" v-if="currentWall !== undefined">
                <div class="card m-1">
                    <span class="text-secondary px-2">Textual</span>
                    <div id="text-widgets-body" role="tabpanel" aria-labelledby="text-widgets-header">
                        <div class="d-flex justify-content-between align-items-center px-2">
                            <div title="Textarea with minimum format options">Simple text</div>
                            <a @click.stop="addBlankWidget(SimpleText)" class="btn bg-light"><i class="fas fa-plus"></i></a>
                        </div>
                        <div class="d-flex justify-content-between align-items-center px-2">
                            <div title="Active link">URL</div>
                            <a @click.stop="addBlankWidget(URL)" class="btn bg-light"><i class="fas fa-plus"></i></a>
                        </div>
                    </div>
                </div>
                <div class="card m-1">
                    <span class="text-secondary px-2">Interactive</span>
                    <div id="interactive-elements-body" role="tabpanel" aria-labelledby="interactive-elements-header">
                        <div class="d-flex justify-content-between align-items-center px-2">
                            <div title="Simple numeric counter, that remember the last state and allows only addition and subtraction">Counter</div>
                            <a @click.stop="addBlankWidget(Counter)" class="btn bg-light"><i class="fas fa-plus"></i></a>
                        </div>
                        <div class="d-flex justify-content-between align-items-center px-2">
                            <div title="List of items">Simple list</div>
                            <a @click.stop="addBlankWidget(SimpleList)" class="btn bg-light"><i class="fas fa-plus"></i></a>
                        </div>
                    </div>
                </div>
            </div>
            <p class="small px-2 text-info" v-else>
                Widgets are not available. Select or create a wall to use widgets
            </p>
            <div class="card p-1 mx-1 my-3">
                <div class="d-flex justify-content-between align-items-center px-2">
                    <div title="Create new wall">Wall</div>
                    <button type="button" class="btn btn-light" data-toggle="modal" data-target="#new-wall-modal">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
                <hr />
                <div v-if="walls.length" class="d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-center p-1" v-for="wall of walls" :key="wall.id">
                        <a
                            @click.stop.prevent="initWall(wall.id)"
                            href="#"
                            :title="wall.description"
                            class="text-break"
                            :class="currentWall !== undefined && wall.id == currentWall.id ? 'text-primary' : 'text-secondary'"
                            >{{ wall.title }}</a
                        >
                        <a @click.stop.prevent="deleteWall(wall.id)" class="btn text-danger" title="Delete wall"><i class="fas fa-times"></i></a>
                    </div>
                </div>
                <div v-else>
                    <small class="text-info">No walls yet... Use <strong>+</strong> button to create one!</small>
                </div>
                <div class="modal fade" id="new-wall-modal" tabindex="-1" role="dialog" aria-labelledby="modelTitleId" aria-hidden="true">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">New wall</h5>
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div class="modal-body">
                                <div class="alert alert-danger" role="alert" v-show="error"><strong>Error</strong> {{ error }}</div>
                                <div class="form-group">
                                    <label for="new-wall-title" class="label">Title</label>
                                    <input class="form-control" v-model="newWall.title" aria-describedby="newWallTitleHelp" id="new-wall-title" :maxlength="Shared.settings.max_wall_title_length" />
                                    <small id="newWallTitleHelp" class="form-text text-muted" v-if="Shared.settings">
                                        Max title length is {{ newWall.title.length }}/{{ Shared.settings.max_wall_title_length }} symbols</small
                                    >
                                </div>
                                <div class="form-group">
                                    <label for="new-wall-description" class="label">Description</label>
                                    <input
                                        class="form-control"
                                        v-model="newWall.description"
                                        aria-describedby="newWallDescriptionHelp"
                                        id="new-wall-description"
                                        :maxlength="Shared.settings.max_wall_description_length"
                                    />
                                    <small id="newWallDescriptionHelp" class="form-text text-muted" v-if="Shared.settings">
                                        Max description length is {{ newWall.description.length }}/{{ Shared.settings.max_wall_description_length }} symbols
                                    </small>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                <button @click.stop="createWall" type="button" class="btn btn-primary">Create</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-12 col-md-10" id="wall-widget-list" v-if="currentWall !== undefined">
            <SimpleText v-for="widget of filterWidgets(SimpleText)" :key="widget.type + widget.id" :widget="widget"> </SimpleText>
            <URL v-for="widget of filterWidgets(URL)" :key="widget.type + widget.id" :widget="widget"> </URL>
            <Counter v-for="widget of filterWidgets(Counter)" :key="widget.type + widget.id" :widget="widget"> </Counter>
            <SimpleList v-for="widget of filterWidgets(SimpleList)" :key="widget.type + widget.id" :widget="widget"> </SimpleList>
        </div>
    </div>
</template>

<script>
    import SimpleText from "./Widgets/SimpleText";
    import URL from "./Widgets/URL";
    import Counter from "./Widgets/Counter";
    import SimpleList from "./Widgets/SimpleList";
    import { API, Shared } from "../common.js";
    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
    };
    export default {
        components,
        created() {
            Shared.init();
            Shared.$on("deleteRequest", this.onDeleteRequest);
            this.resetNewWall();
            this.initWalls();
        },
        data() {
            return {
                Shared,
                type: "wall",
                api: undefined,
                currentWall: undefined,
                walls: [],
                newWall: undefined,
                widgets: undefined,
                error: undefined, // Error msg
                ...components,
            };
        },
        methods: {
            initWall(wall_id) {
                new API(this.type, wall_id).retrieve().then((response) => {
                    this.api = new API(response.wall.type, response.wall.id);
                    this.currentWall = response.wall;
                    this.widgets = response.widgets;
                });
            },
            initWalls() {
                new API(this.type).list().then((response) => {
                    this.walls = response;
                });
            },
            createWall() {
                new API(this.type).create(this.newWall).then((response) => {
                    this.api = new API(response.type, response.id);
                    this.currentWall = response;
                    this.widgets = [];
                    this.resetNewWall();
                    this.initWalls();
                });
            },
            resetNewWall() {
                this.newWall = {
                    title: "",
                    description: "",
                };
            },
            deleteWall(wall_id) {
                if (confirm("Are you sure? Wall will be permanently removed!")) {
                    new API(this.type, wall_id).delete().then(() => {
                        this.initWalls();
                        if (this.currentWall !== undefined && wall_id == this.currentWall.id) {
                            this.api = undefined;
                            this.currentWall = undefined;
                            this.widgets = undefined;
                        }
                    });
                }
            },
            filterWidgets(klass) {
                try {
                    return this.widgets.filter(function(w) {
                        return w.type == klass.type;
                    });
                } catch (error) {
                    return [];
                }
            },
            addBlankWidget(klass) {
                if (this.currentWall !== undefined) {
                    new API(klass.type)
                        .create({
                            wall: this.currentWall.id,
                            top: 0,
                            left: 0,
                        })
                        .then((response) => {
                            this.widgets.push(response);
                        });
                }
            },
            onDeleteRequest(widget) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
            },
        },
    };
</script>
