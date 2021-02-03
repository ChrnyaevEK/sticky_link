<template>
    <vue-resizable
        @resize:end="onResizeEnd"
        @drag:end="onDragEnd"
        :fitParent="true"
        class="widget rounded"
        ref="resizable"
        dragSelector=".control-area"
        :width="widget.width"
        :minWidth="widget.minWidth"
        :height="widget.height"
        :minHeight="widget.minHeight"
        :top="widget.top"
        :left="widget.left"
        :class="`bg-${widget.background_color} text-${widget.text_color}`"
    >
        <div @click.stop.prevent @dblclick="onOptionsRequest" class="h-100 w-100">
            <div class="content px-2 control-area">
                <slot name="content">
                    <div class="content-empty d-flex align-items-center justify-content-center">
                        <div>Nothing is here yet... <i class="far fa-frown"></i></div>
                    </div>
                </slot>
            </div>
            <div class="modal fade" :id="_('options')" tabindex="-1" role="dialog" :aria-labelledby="_('options')" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content text-dark">
                        <div class="modal-header">
                            <h5 class="modal-title">Widget options</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <form class="form-inline">
                                <div class="form-group w-50">
                                    <label :for="_('width')">Width</label>
                                    <input class="form-control" v-model="widget.width" :aria-describedby="_('widthHelp')" type="number" name="width" :id="_('width')" step="1">
                                </div>
                                <div class="form-group w-50">
                                    <label :for="_('height')">Height</label>
                                    <input class="form-control" v-model="widget.height" :aria-describedby="_('heightHelp')" type="number" name="height" :id="_('height')" step="1">
                                </div>
                            </form>
                            <form class="form-inline">
                                <div class="form-group w-50">
                                    <label :for="_('left')">Left offset</label>
                                    <input class="form-control" v-model="widget.left" :aria-describedby="_('leftHelp')" type="number" name="left" :id="_('left')" step="1">
                                </div>
                                <div class="form-group w-50">
                                    <label :for="_('top')">Top offset</label>
                                    <input class="form-control" v-model="widget.top" :aria-describedby="_('topHelp')" type="number" name="top" :id="_('top')" step="1">
                                </div>
                            </form>
                            <form>

                                <slot name="options"></slot>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Save</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </vue-resizable>
</template>

<script>
    // Front end is absolutely passive
    import VueResizable from "vue-resizable";
    import { registerIdSystem, WidgetManager } from "../../common.js";
    import $ from "jquery";
    export default {
        name: "WidgetBase",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        data: function() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
            var vm = this;
            return {
                manager: new WidgetManager(vm.widget.type, vm.widget.id),
                optionsModal: this._("options"),
            };
        },
        methods: {
            onResizeEnd: function(event) {
                // [eventName,left,top,width,height]
                this.widget.width = event.width;
                this.widget.height = event.height;
            },
            onDragEnd: function(event) {
                // [eventName,left,top,width,height]
                this.widget.left = event.left;
                this.widget.top = event.top;
            },
            onOptionsRequest: function() {
                $(`#${this.optionsModal}`).modal('show');
            },
        },
        components: {
            VueResizable,
        },
        watch: {
            widget: {
                handler: function() {
                    this.manager.updated(this.widget);
                    this.$refs.resizable.restoreSize()
                },
                deep: true,
            },
        },
    };
</script>

<style scoped>
    .widget {
        position: absolute;
        border-style: solid;
        border-width: 1px;
        border-color: rgb(189, 189, 189);
        margin: 0;
        padding: 0;
    }
    .widget .control-area {
        width: 100%;
        height: 100%;
    }
    .widget .content,
    .widget .content-empty {
        width: 100%;
        height: 100%;
    }
    .widget .sidebar {
        height: 100%;
    }
    .widget .sidebar:hover {
        cursor: grab;
    }
</style>
