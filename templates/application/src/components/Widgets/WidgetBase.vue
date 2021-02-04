<template>
    <vue-resizable
        @resize:end="onResizeEnd"
        @drag:end="onDragEnd"
        :fitParent="true"
        class="widget"
        ref="resizable"
        dragSelector=".control-area"
        :width="widget.width"
        :minWidth="widget.minWidth"
        :height="widget.height"
        :minHeight="widget.minHeight"
        :top="widget.top"
        :left="widget.left"
    >
        <div @click.stop.prevent @dblclick="onOptionsRequest" class="h-100 w-100">
            <div class="content px-2 control-area" :style="`z-index: ${widget.z_index};`" :class="`bg-${widget.background_color} text-${widget.text_color}`">
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
                            <form>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-12 col-md-6">
                                            <label :for="_('width')">Width</label>
                                            <input class="form-control" v-model.number="widget.width" :aria-describedby="_('widthHelp')" type="number" name="width" :id="_('width')" step="1" />
                                        </div>
                                        <div class="col-12 col-md-6">
                                            <label :for="_('height')">Height</label>
                                            <input class="form-control" v-model.number="widget.height" :aria-describedby="_('heightHelp')" type="number" name="height" :id="_('height')" step="1" />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-12 col-md-6">
                                            <label :for="_('left')">Left offset</label>
                                            <input class="form-control" v-model.number="widget.left" :aria-describedby="_('leftHelp')" type="number" name="left" :id="_('left')" step="1" />
                                        </div>
                                        <div class="col-12 col-md-6">
                                            <label :for="_('top')">Top offset</label>
                                            <input class="form-control" v-model.number="widget.top" :aria-describedby="_('topHelp')" type="number" name="top" :id="_('top')" step="1" />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-12 col-md-6">
                                            <label :for="_('z_index')">Z-Index (overlay)</label>
                                            <input class="form-control" v-model.number="widget.z_index" :aria-describedby="_('ZIndexHelp')" type="number" name="z_index" :id="_('z_index')" step="1" />
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label :for="_('background_color')">Background color</label>
                                    <v-select :id="_('background_color')" v-model="widget.background_color" :reduce="(val) => val.code" :options="colorOptions"></v-select>
                                </div>
                                <div class="form-group">
                                    <label :for="_('text_color')">Text color</label>
                                    <v-select :id="_('text_color')" v-model="widget.text_color" :reduce="(val) => val.code" :options="colorOptions"></v-select>
                                </div>
                                <slot name="options"></slot>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
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
    import { registerIdSystem, WidgetManager, Shared } from "../../common.js";
    import vSelect from "vue-select";
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
                Shared: Shared,
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
                $(`#${this.optionsModal}`).modal("show");
            },
        },
        components: {
            VueResizable,
            vSelect,
        },
        watch: {
            widget: {
                handler: function() {
                    this.manager.updated(this.widget);
                },
                deep: true,
            },
        },
        computed: {
            colorOptions() {
                var res = [];
                for (var opt of Shared.settings.colors) {
                    res.push({
                        label: opt[1],
                        code: opt[0],
                    });
                }
                return res;
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
        position: absolute;
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
