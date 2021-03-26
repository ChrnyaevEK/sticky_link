<template>
    <vue-draggable-resizable
        v-if="$env.state.editInstance !== null"
        @mousedown.native.stop
        @mouseup.native.stop
        @mousemove.native.stop
        dragHandle=".options-drag"
        @click.native.stop
        @touchstart.native.stop.prevent
        h="auto"
        :z="100"
        :resizable="false"
        :parent="false"
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
                    :id="_('x')"
                    v-model.number="instance.x"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="10"
                    min="0"
                />
            </div>

            <div class="form-group">
                <label :for="_('y')">Y coordinate</label>
                <input
                    :id="_('y')"
                    v-model.number="instance.y"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="10"
                    min="0"
                />
            </div>

            <div class="form-group">
                <label :for="_('z')">Z coordinate</label>
                <input
                    :id="_('z')"
                    v-model.number="instance.z"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="1"
                    min="0"
                    max="10"
                />
            </div>

            <div class="form-group">
                <label :for="_('w')">Width</label>
                <input
                    :id="_('w')"
                    v-model.number="instance.w"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="1"
                    min="50"
                />
            </div>

            <div class="form-group">
                <label :for="_('h')">Height</label>
                <input
                    :id="_('h')"
                    v-model.number="instance.h"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="1"
                    min="50"
                />
            </div>
            <div class="form-group">
                <label :for="_('font_size')">Font size</label>
                <input
                    :id="_('font_size')"
                    v-model.number="instance.font_size"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="1"
                    min="6"
                    max="40"
                />
            </div>

            <div class="form-group">
                <label :for="_('font_weight')">Font weight</label>
                <input
                    :id="_('font_weight')"
                    v-model.number="instance.font_weight"
                    @input="push"
                    class="form-control"
                    type="number"
                    step="100"
                    min="100"
                    max="900"
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
            <div class="form-group">
                <label :for="_('help')">Help text</label>
                <input
                    :id="_('help')"
                    class="form-control"
                    v-model="instance.help"
                    @input="push"
                    maxlength="200"
                />
            </div>
            <div class="form-check">
                <input
                    type="checkbox"
                    :id="_('border')"
                    class="form-check-input"
                    v-model="instance.border"
                    @change="push"
                />
                <label class="form-check-label" :for="_('border')">Border</label>
            </div>
        </template>
        <template v-if="instance.type == 'wall'">
            <div class="form-group">
                <label :for="_('title')">Title </label>
                <input :id="_('title')" class="form-control" v-model="instance.title" @input="push" />
            </div>
            <div class="form-check">
                <input
                    type="checkbox"
                    :id="_('allow_anonymous_view')"
                    class="form-check-input"
                    v-model="instance.allow_anonymous_view"
                    @change="push"
                />
                <label class="form-check-label" :for="_('allow_anonymous_view')">Allow anonymous view mode</label>
            </div>
            <div class="form-check">
                <input
                    type="checkbox"
                    :id="_('lock_widgets')"
                    class="form-check-input"
                    v-model="instance.lock_widgets"
                    @change="push"
                />
                <label class="form-check-label" :for="_('lock_widgets')">Lock widget actions</label>
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
                <input :id="_('value')" class="form-control" v-model.number="instance.value" @input="push" />
            </div>
            <div class="form-group">
                <label :for="_('title')">Title </label>
                <input :id="_('title')" class="form-control" v-model="instance.title" @input="push" />
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
                <input :id="_('title')" class="form-control" v-model="instance.title" @input="push" />
            </div>
        </template>
        <!--Simple Switch-->
        <template v-if="instance.type == SimpleSwitch.type">
            <div class="form-group">
                <label :for="_('title')">Title </label>
                <input :id="_('title')" class="form-control" v-model="instance.title" @input="push" />
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
    import SimpleSwitch from "../Widgets/SimpleSwitch";

    export default {
        name: "Options",
        data: function() {
            return {
                SimpleText,
                URL,
                Counter,
                SimpleList,
                SimpleSwitch,
            };
        },
        computed: {
            instance() {
                return this.$env.state.editInstance;
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
        min-width: 200px;
        max-width: 400px;
        width: 50% !important;
    }
    .options-position {
        position: fixed;
        top: 0;
        right: 0;
    }
</style>
