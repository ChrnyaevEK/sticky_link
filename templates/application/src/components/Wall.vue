<template>
    <div class="flex-grow-1 row w-100">
        <div class="col-12 col-md-2">
            <div class="font-weight-bold p-2">Widgets</div>
            <div id="wall-widget-selector" role="tablist" aria-multiselectable="true" class="border-top border-bottom">
                <div class="card border-0">
                    <div class="card-header p-2 bg-light" role="tab" id="text-widgets-header" title="Help to place text information">
                        <a data-toggle="collapse" data-parent="#wall-widget-selector" href="#text-widgets-body" aria-expanded="true" aria-controls="text-widgets-body">
                            Text widgets
                        </a>
                    </div>
                    <div id="text-widgets-body" class="collapse in" role="tabpanel" aria-labelledby="text-widgets-header">
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Textarea with minimum format options">Simple text</div>
                            <a @click.stop="addBlankWidget(SimpleText)" class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></a>
                        </div>
                        <!-- <div class="card-body p-2 row">
                            <div class="col-10" title="Textarea with Markdown support">Rich text (markdown)</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></div>
                        </div> -->
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Active link">URL</div>
                            <a @click.stop="addBlankWidget(URL)" class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></a>
                        </div>
                    </div>
                </div>
                <!-- <div class="card border-0">
                    <div class="card-header p-2 bg-light" role="tab" id="support-elements-header" title="Help to form layout and divide information into to logical groups">
                        <a data-toggle="collapse" data-parent="#wall-widget-selector" href="#support-elements-body" aria-expanded="true" aria-controls="support-elements-body">
                            Support elements
                        </a>
                    </div>
                    <div id="support-elements-body" class="collapse in" role="tabpanel" aria-labelledby="support-elements-header">
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Blank card with a lot of customization available. Primary used as a background">Card</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="A line that divides data to form logical groups">Divider</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></div>
                        </div>
                    </div>
                </div> -->
                <div class="card border-0">
                    <div class="card-header p-2 bg-light" role="tab" id="interactive-elements-header" title="Elements to interact with user">
                        <a data-toggle="collapse" data-parent="#wall-widget-selector" href="#interactive-elements-body" aria-expanded="true" aria-controls="interactive-elements-body">
                            Interactive elements
                        </a>
                    </div>
                    <div id="interactive-elements-body" class="collapse in" role="tabpanel" aria-labelledby="interactive-elements-header">
                        <!-- <div class="card-body p-2 row">
                            <div class="col-10" title="Programmable button">Action button</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></div>
                        </div> -->
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Simple numeric counter, that remember the last state and allows only addition and subtraction">Counter</div>
                            <a @click.stop="addBlankWidget(Counter)" class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></a>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="List of items">Simple list</div>
                            <a @click.stop="addBlankWidget(SimpleList)" class="col-2 btn bg-light p-0"><i class="fas fa-plus"></i></a>
                        </div>
                    </div>
                </div>
            </div>
            <!-- <div class="font-weight-bold p-2">Global setup</div>
            <div id="wall-global-setup-selector" role="tablist" aria-multiselectable="true" class="border-top border-bottom">
                <div class="card border-0">
                    <div class="card-header p-2 bg-light" role="tab" id="event-header" title="Executed when certain event fired (events are setup up latter)">
                        <a data-toggle="collapse" data-parent="#wall-widget-selector" href="#event-body" aria-expanded="true" aria-controls="event-body">
                            Event dependent actions
                        </a>
                    </div>
                    <div id="event-body" class="collapse in" role="tabpanel" aria-labelledby="event-header">
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Call supplied URL with occasional payload">Webhook</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Redirect visitor to another page (Caution! A visitor may not see the content of this page)">Redirect</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Show popup">Popup</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Lock page and ask for a password to continue">Lock page</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Make widget visible or usable">Discover widget</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Execute a custom JavaScript code in a separate iFrame">JavaScript</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                    </div>
                </div>
                <div class="card border-0">
                    <div class="card-header p-2 bg-light" role="tab" id="layout-header" title="Setup elements positions for different screen widths (layouts)">
                        <a data-toggle="collapse" data-parent="#wall-widget-selector" href="#layout-body" aria-expanded="true" aria-controls="layout-body">
                            Layout
                        </a>
                    </div>
                    <div id="layout-body" class="collapse in" role="tabpanel" aria-labelledby="layout-header">
                        <div class="card-body p-2 row">
                            <div class="col-10" title="General settings for layout">General settings</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="Less than 576px">Extra small</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="More or equal to 540px">Small</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="More or equal to 720px">Medium</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                        <div class="card-body p-2 row">
                            <div class="col-10" title="More or equal to 960px">Large</div>
                            <div class="col-2 btn bg-light p-0"><i class="fas fa-chevron-right"></i></div>
                        </div>
                    </div>
                </div>
            </div>-->
            <Profile></Profile>
        </div>
        <div class="col-12 col-md-10" id="wall-widget-list">
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
    import Profile from "./Profile";
    import { API, registerIdSystem, Shared } from "../common.js";
    var components = {
        SimpleText,
        URL,
        Counter,
        SimpleList,
        Profile,
    };
    export default {
        name: "Wall",
        components,
        created() {
            registerIdSystem(this, this.wall.type, this.wall.id);
            Shared.$on("deleteRequest", this.onDeleteRequest);
            this.retrieve();
        },
        props: {
            id: {
                type: Number,
                required: true,
            },
        },
        data() {
            var vm = this;
            return {
                API: new API("wall", vm.id),
                wall: {},
                widgets: [],
                ...components
            };
        },
        methods: {
            retrieve() {
                // this.API.retrieve().then((response) => {
                //     this.wall = response.wall;
                //     this.widgets = response.widgets;
                // });
                Shared.init()
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
                var wAPI = new API(klass.type);
                wAPI.create({
                    wall: this.id,
                }).then((response) => {
                    this.widgets.push(response);
                });
            },
            onDeleteRequest(widget) {
                this.widgets.splice(this.widgets.indexOf(widget), 1);
            },
        },
    };
</script>
