<template>
    <div>
        <vue-resizable
            @resize:end="onResizeEnd"
            @drag:end="onDragEnd"
            class="widget"
            ref="resizable"
            dragSelector=".widget-drag"
            :fitParent="true"
            :width="widget.width"
            :height="widget.height"
            :top="widget.top"
            :left="widget.left"
        >
            <div @dblclick.stop.prevent="optionsVisible = true" class="h-100 w-100">
                <div class="widget-quick-access" v-show="quickAccessVisible">
                    <a class="widget-drag btn btn-light"><i class="fas fa-expand-arrows-alt"></i></a>
                </div>
                <div class="content p-1 control-area" :style="style">
                    <slot name="content"></slot>
                </div>
            </div>
        </vue-resizable>
        <vue-resizable 
            :width="400" 
            :height="600" 
            dragSelector=".widget-drag" 
            class="bg-light" 
            v-show="optionsVisible"
        >
            <div class="overflow-auto m-0 p-0 h-100">
                <div class="widget-quick-access" v-show="quickAccessVisible">
                    <a class="widget-drag btn btn-light"><i class="fas fa-expand-arrows-alt"></i></a>
                </div>
                <div class="modal-header">
                    <h5 class="card-title">Widget options</h5>
                    <button type="button" class="close" aria-label="Close" @click.stop="optionsVisible = false">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <div class="row">
                            <div class="col-12 col-md-6">
                                <label :for="_('width')">Width</label>
                                <input class="form-control" v-model.number="widget.width" type="number" :id="_('width')" step="1" />
                            </div>
                            <div class="col-12 col-md-6">
                                <label :for="_('height')">Height</label>
                                <input class="form-control" v-model.number="widget.height" type="number" :id="_('height')" step="1" />
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12 col-md-6">
                                <label :for="_('left')">Left offset</label>
                                <input class="form-control" v-model.number="widget.left" type="number" :id="_('left')" step="1" />
                            </div>
                            <div class="col-12 col-md-6">
                                <label :for="_('top')">Top offset</label>
                                <input class="form-control" v-model.number="widget.top" type="number" :id="_('top')" step="1" />
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12">
                                <label :for="_('z_index')">Z-Index (overlay)</label>
                                <input class="form-control" v-model.number="widget.z_index" type="number" :id="_('z_index')" step="1" />
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12 col-md-6">
                                <label :for="_('font_size')">Font size</label>
                                <input
                                    class="form-control"
                                    v-model.number="widget.font_size"
                                    type="number"
                                    step="1"
                                    :id="_('font_size')"
                                    :min="Shared.settings.min_font_size"
                                    :max="Shared.settings.max_font_size"
                                />
                            </div>
                            <div class="col-12 col-md-6">
                                <label :for="_('font_weight')">Font weight</label>
                                <input
                                    class="form-control"
                                    v-model.number="widget.font_weight"
                                    type="number"
                                    step="100"
                                    :id="_('font_weight')"
                                    :min="Shared.settings.min_font_weight"
                                    :max="Shared.settings.max_font_weight"
                                />
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label :for="_('background_color')">Background color</label>
                        <input type="color" v-model="widget.background_color" class="form-control" />
                    </div>
                    <div class="form-group">
                        <label :for="_('text_color')">Text color</label>
                        <input type="color" v-model="widget.text_color" class="form-control" />
                    </div>
                    <slot name="options"></slot>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-danger" @click.stop="deleteWidget">Delete</button>
                    <button type="button" class="btn btn-light border" data-dismiss="modal">Close</button>
                </div>
            </div>
        </vue-resizable>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import VueResizable from "vue-resizable";
    import { registerIdSystem, WidgetManager, Shared } from "../../common.js";
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
                manager: new WidgetManager(vm.widget.type, vm.widget.id, this.unsetWarning, this.setWarningFromResponse),
                optionsModal: this._("options"),
                Shared: Shared,
                warningClass: "widget-options-warning", // Show warning messages
                quickAccessClass: "widget-quick-access",
                quickAccessVisible: false,
                optionsVisible: false,
            };
        },
        methods: {
            onResizeEnd(event) {
                // [eventName,left,top,width,height]
                this.widget.width = event.width;
                this.widget.height = event.height;
            },
            onDragEnd(event) {
                // [eventName,left,top,width,height]
                this.widget.left = event.left;
                this.widget.top = event.top;
            },
            setWarningFromResponse(response) {
                for (var [field, error] of Object.entries(response.responseJSON)) {
                    $(`[for='${this._(field)}']`)
                        .addClass("text-danger")
                        .append(
                            $(`
                        <p class="${this.warningClass}"><small>${error[0]}</small></p>
                    `)
                        );
                }
            },
            unsetWarning() {
                $(`.${this.warningClass}`)
                    .parent()
                    .removeClass("text-dander");
                $(`.${this.warningClass}`).remove();
            },
            deleteWidget() {
                if (confirm("Are you sure?")) {
                    $(`#${this.optionsModal}`).modal("hide");
                    Shared.$emit("deleteRequest", this.widget);
                    this.manager.delete();
                }
            },
        },
        components: {
            VueResizable,
        },
        computed: {
            style() {
                return `
                    z-index: ${this.widget.z_index};
                    background-color: ${this.widget.background_color};
                    color: ${this.widget.text_color};
                    font-size:${this.widget.font_size}px;
                    font-weight:${this.widget.font_weight};
                `;
            },
        },
        watch: {
            widget: {
                handler: function() {
                    this.manager.updated(this.widget);
                },
                deep: true,
            },
        },
        mounted() {
            $(this.$el)
                .mouseenter(() => {
                    this.quickAccessVisible = true;
                })
                .mouseleave(() => {
                    this.quickAccessVisible = false;
                });
        },
    };
</script>

<style scoped>
    .widget {
        position: absolute !important;
        margin: 0;
        padding: 0;
        border-style: solid;
        border-width: 1px;
        border-color: #dadada;
    }
    .control-area {
        width: 100%;
        height: 100%;
        position: absolute;
    }
    .content {
        width: 100%;
        height: 100%;
    }
    .sidebar {
        height: 100%;
    }
    .sidebar:hover {
        cursor: grab;
    }
    .widget-quick-access {
        position: absolute;
        display: flex;
        justify-content: flex-end;
        padding: 2px 2px 0 2px;
        z-index: 2;
        width: 100%;
    }
    .widget-quick-access a {
        margin: 0 0 0 2px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 2rem;
        width: 2rem;
    }
</style>
