<template>
    <vue-draggable-resizable
        v-if="optionsVisible"
        @mousedown.native.stop
        @mouseup.native.stop
        @mousemove.native.stop
        dragHandle=".options-drag"
        :w="400"
        :h="600"
        :z="10"
        :x="widget.x + widget.w"
        :y="widget.y"
        :resizable="false"
        :parent="false"
        class="bg-white border overflow-auto shadow rounded options-position"
    >
        <div class="w-100 h-100 p-3">
            <div class="form-group d-flex justify-content-between align-items-center options-drag border-bottom cursor-move">
                <strong>Options</strong>
                <a class="btn" @click="onCloseOptions"><i class="fas fa-times"></i></a>
            </div>

            <div class="form-group">
                <label :for="_('x')">X coordinate</label>
                <input class="form-control" v-model.number="widget.x" type="number" :id="_('x')" step="1" :min="Context.settings.widget ? Context.settings.widget.min_x : 0" />
            </div>

            <div class="form-group">
                <label :for="_('y')">Y coordinate</label>
                <input class="form-control" v-model.number="widget.y" type="number" :id="_('y')" step="1" :min="Context.settings.widget ? Context.settings.widget.min_y : 0" />
            </div>

            <div class="form-group">
                <label :for="_('z')">Z coordinate</label>
                <input
                    class="form-control"
                    v-model.number="widget.z"
                    type="number"
                    :id="_('z')"
                    step="1"
                    :min="Context.settings.widget ? Context.settings.widget.min_z : 0"
                    :max="Context.settings.widget ? Context.settings.widget.max_z : 0"
                />
            </div>

            <div class="form-group">
                <label :for="_('w')">Width</label>
                <input class="form-control" v-model.number="widget.w" type="number" :id="_('w')" step="1" :min="Context.settings.widget ? Context.settings.widget.min_width : 0" />
            </div>

            <div class="form-group">
                <label :for="_('h')">Height</label>
                <input class="form-control" v-model.number="widget.h" type="number" :id="_('h')" step="1" :min="Context.settings.widget ? Context.settings.widget.min_height : 0" />
            </div>
            <div class="form-group">
                <label :for="_('font_size')">Font size</label>
                <input
                    class="form-control"
                    v-model.number="widget.font_size"
                    type="number"
                    step="1"
                    :id="_('font_size')"
                    :min="Context.settings.widget ? Context.settings.widget.min_font_size : 0"
                    :max="Context.settings.widget ? Context.settings.widget.max_font_size : 0"
                />
            </div>

            <div class="form-group">
                <label :for="_('font_weight')">Font weight</label>
                <input
                    class="form-control"
                    v-model.number="widget.font_weight"
                    type="number"
                    step="100"
                    :id="_('font_weight')"
                    :min="Context.settings.widget ? Context.settings.widget.min_font_weight : 0"
                    :max="Context.settings.widget ? Context.settings.widget.max_font_weight : 0"
                />
            </div>

            <div class="form-group">
                <label :for="_('background_color')">Background color</label>
                <input type="color" :id="_('background_color')" v-model="widget.background_color" class="form-control" />
            </div>

            <div class="form-group">
                <label :for="_('text_color')">Text color</label>
                <input type="color" :id="_('text_color')" v-model="widget.text_color" class="form-control" />
            </div>
            <hr />
            <!--Options by widget type========================================================================================================-->
            <!--Simple text-->
            <template v-if="widget.type == SimpleText.type">
                <div class="form-group">
                    <label :for="_('text_content')">Content of widget </label>
                    <textarea :id="_('text_content')" class="form-control" v-model="widget.text_content" rows="10"></textarea>
                </div>
            </template>
            <!--Counter-->
            <template v-if="widget.type == Counter.type">
                <div class="form-group">
                    <label :for="_('value')">Value </label>
                    <input :id="_('value')" class="form-control" v-model.number="widget.value" :aria-describedby="_('valueHelp')" />
                </div>
                <div class="form-group">
                    <label :for="_('title')">Title </label>
                    <input :id="_('title')" class="form-control" v-model.number="widget.title" :aria-describedby="_('titleHelp')" />
                </div>
            </template>
            <!--URL-->
            <template v-if="widget.type == URL.type">
                <div class="form-group">
                    <label :for="_('href')">URL address </label>
                    <input :id="_('href')" class="form-control" v-model="widget.href" />
                </div>
                <div class="form-group">
                    <label :for="_('text')">URL text </label>
                    <input :id="_('text')" class="form-control" v-model="widget.text" />
                </div>
            </template>
            <!--Simple List-->
            <template v-if="widget.type == SimpleList.type">
                <div class="form-group">
                    <label :for="_('title')">Title </label>
                    <input :id="_('title')" class="form-control" v-model.number="widget.title" :aria-describedby="_('titleHelp')" />
                </div>
            </template>

            <!--Options by widget type========================================================================================================-->
            <div class="form-group d-flex justify-content-center">
                <small class="text-secondary">All changes are automatically saved</small>
            </div>
        </div>
    </vue-draggable-resizable>
</template>

<script>
    // Front end is absolutely passive
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import { registerIdSystem, Context } from "../../common.js";
    import $ from "jquery";
    import SimpleText from "./SimpleText";
    import URL from "./URL";
    import Counter from "./Counter";
    import SimpleList from "./SimpleList";

    export default {
        name: "WidgetOptions",
        created() {
            Context.$on("openWidgetOptions", this.onOpenOptions);
            Context.$on("closeWidgetOptions", this.onCloseOptions);
        },
        data: function() {
            return {
                Context,
                SimpleText,
                URL,
                Counter,
                SimpleList,
                widget: null,
                optionsVisible: false,
            };
        },
        methods: {
            onOpenOptions(widget) {
                registerIdSystem(this, widget); // Create _ function to generate ids
                this.$set(this, "widget", widget);
                this.optionsVisible = true;
            },
            onCloseOptions() {
                this.widget = null;
                this.optionsVisible = false;
            },
            setWarningFromResponse(response) {
                this.unsetWarning();
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
        },
        components: {
            VueDraggableResizable,
        },
    };
</script>

<style scoped>
    .options-position {
        position: absolute;
        top: 0;
    }
</style>
