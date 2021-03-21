<template>
    <vue-draggable-resizable
        v-if="$env.state.editInstance !== null"
        @mousedown.native.stop
        @mouseup.native.stop
        @mousemove.native.stop
        dragHandle=".options-drag"
        @click.native.stop
        h="auto"
        :w="w"
        :z="100"
        :x="x"
        :y="y"
        :resizable="false"
        :parent="true"
        class="bg-white border overflow-auto shadow rounded options-position options-size p-3"
    >
        <div
            class="form-group d-flex justify-content-between align-items-center options-drag border-bottom cursor-move"
        >
            <strong>Options</strong>
            <a class="btn" @click="$env.dispatch('closeOptions')"><i class="fas fa-times"></i></a>
        </div>
        <template v-if="instance.type != 'wall'">
            <div class="form-group">
                <label :for="_('x')">X coordinate</label>
                <input
                    class="form-control"
                    v-model.number="instance.x"
                    @input="push"
                    type="number"
                    :id="_('x')"
                    step="1"
                    :min="$store.state.settings.widget.min_x"
                />
            </div>

            <div class="form-group">
                <label :for="_('y')">Y coordinate</label>
                <input
                    class="form-control"
                    v-model.number="instance.y"
                    @input="push"
                    type="number"
                    :id="_('y')"
                    step="1"
                    :min="$store.state.settings.widget.min_y"
                />
            </div>

            <div class="form-group">
                <label :for="_('z')">Z coordinate</label>
                <input
                    class="form-control"
                    v-model.number="instance.z"
                    @input="push"
                    type="number"
                    :id="_('z')"
                    step="1"
                    :min="$store.state.settings.widget.min_z"
                    :max="$store.state.settings.widget.max_z"
                />
            </div>

            <div class="form-group">
                <label :for="_('w')">Width</label>
                <input
                    class="form-control"
                    v-model.number="instance.w"
                    @input="push"
                    type="number"
                    :id="_('w')"
                    step="1"
                    :min="$store.state.settings.widget.min_width"
                />
            </div>

            <div class="form-group">
                <label :for="_('h')">Height</label>
                <input
                    class="form-control"
                    v-model.number="instance.h"
                    @input="push"
                    type="number"
                    :id="_('h')"
                    step="1"
                    :min="$store.state.settings.widget.min_height"
                />
            </div>
            <div class="form-group">
                <label :for="_('font_size')">Font size</label>
                <input
                    class="form-control"
                    v-model.number="instance.font_size"
                    @input="push"
                    type="number"
                    step="1"
                    :id="_('font_size')"
                    :min="$store.state.settings.widget.min_font_size"
                    :max="$store.state.settings.widget.max_font_size"
                />
            </div>

            <div class="form-group">
                <label :for="_('font_weight')">Font weight</label>
                <input
                    class="form-control"
                    v-model.number="instance.font_weight"
                    @input="push"
                    type="number"
                    step="100"
                    :id="_('font_weight')"
                    :min="$store.state.settings.widget.min_font_weight"
                    :max="$store.state.settings.widget.max_font_weight"
                />
            </div>

            <div class="form-group">
                <label :for="_('background_color')">Background color</label>
                <input
                    type="color"
                    :id="_('background_color')"
                    v-model="instance.background_color"
                    @input="push"
                    class="form-control"
                />
            </div>

            <div class="form-group">
                <label :for="_('text_color')">Text color</label>
                <input
                    type="color"
                    :id="_('text_color')"
                    v-model="instance.text_color"
                    @input="push"
                    class="form-control"
                />
            </div>
            <div class="form-check">
                <input
                    type="checkbox"
                    :id="_('border')"
                    class="form-check-input"
                    v-model="instance.border"
                    @input="push"
                />
                <label class="form-check-label" :for="_('border')">Border</label>
            </div>
        </template>
        <template v-if="instance.type == 'wall'">
            <div class="form-check">
                <input
                    type="checkbox"
                    :id="_('allow_anonymous_view')"
                    class="form-check-input"
                    v-model="instance.allow_anonymous_view"
                    @input="push"
                />
                <label class="form-check-label" :for="_('allow_anonymous_view')">Allow anonymous view mode</label>
            </div>
        </template>
        <hr />
        <!--Options by widget type========================================================================================================-->
        <!--Simple text-->
        <template v-if="instance.type == SimpleText.type">
            <TextEditor v-model="instance.text_content" @input="push"></TextEditor>
        </template>
        <!--Counter-->
        <template v-if="instance.type == Counter.type">
            <div class="form-group">
                <label :for="_('value')">Value </label>
                <input
                    :id="_('value')"
                    class="form-control"
                    v-model.number="instance.value"
                    @input="push"
                    :aria-describedby="_('valueHelp')"
                />
            </div>
            <div class="form-group">
                <label :for="_('title')">Title </label>
                <input
                    :id="_('title')"
                    class="form-control"
                    v-model.number="instance.title"
                    @input="push"
                    :aria-describedby="_('titleHelp')"
                />
            </div>
        </template>
        <!--URL-->
        <template v-if="instance.type == URL.type">
            <div class="form-group">
                <label :for="_('href')">URL address </label>
                <input :id="_('href')" class="form-control" v-model="instance.href" @input="push" />
            </div>
            <div class="form-group">
                <label :for="_('text')">URL text </label>
                <input :id="_('text')" class="form-control" v-model="instance.text" @input="push" />
            </div>
        </template>
        <!--Simple List-->
        <template v-if="instance.type == SimpleList.type">
            <div class="form-group">
                <label :for="_('title')">Title </label>
                <input
                    :id="_('title')"
                    class="form-control"
                    v-model.number="widget.title"
                    @input="push"
                    :aria-describedby="_('titleHelp')"
                />
            </div>
        </template>

        <!--Options by widget type========================================================================================================-->
        <div class="form-group d-flex justify-content-center">
            <small class="text-secondary">All changes are automatically saved</small>
        </div>
    </vue-draggable-resizable>
</template>

<script>
    // Front end is absolutely passive
    import VueDraggableResizable from "vue-draggable-resizable";
    import "vue-draggable-resizable/dist/VueDraggableResizable.css";
    import $ from "jquery";
    import TextEditor from "./TextEditor";
    import SimpleText from "../Widgets/SimpleText";
    import URL from "../Widgets/URL";
    import Counter from "../Widgets/Counter";
    import SimpleList from "../Widgets/SimpleList";

    export default {
        name: "Options",
        data: function() {
            return {
                SimpleText,
                URL,
                Counter,
                SimpleList,
                w: 400,
                h: 450,
                y: 0,
            };
        },
        computed: {
            instance() {
                return this.$env.state.editInstance;
            },
            x() {
                return window.innerWidth - this.w;
            },
        },
        methods: {
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
                    .removeClass("text-danger");
                $(`.${this.warningClass}`).remove();
            },
            push() {
                if (!this.$env.lockChanges) {
                    this.$store.dispatch("updateOrAddInstance", this.instance).then(
                        () => {
                            this.unsetWarning();
                        },
                        (response) => {
                            this.setWarningFromResponse(response);
                        }
                    );
                }
            },
        },
        components: {
            TextEditor,
            VueDraggableResizable,
        },
    };
</script>

<style scoped>
    .options-size {
        max-height: 600px;
    }
    .options-position {
        position: absolute;
        top: 0;
        left: 0;
    }
</style>
