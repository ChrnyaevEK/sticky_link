<template>
    <vue-draggable-resizable
        v-if="$env.openOptionsFor !== null"
        dragHandle=".options-drag"
        @click.native.stop
        @touchstart.native.stop.prevent
        h="auto"
        :z="101"
        :resizable="false"
        :parent="false"
        class="bg-white border shadow options options-position options-size p-2 m-1 scrollbar-hidden"
    >
        <div class="form-group d-flex justify-content-between align-items-center options-drag cursor-move">
            <strong>Options</strong>
            <a class="btn" @click="$env.closeOptions()"><i class="fas fa-times"></i></a>
        </div>
        <hr />
        <template v-if="instance.type == types.Wall">
            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column">
                        <strong>Description</strong>
                        <span class="text-secondary">Tell more about this wall</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('title')">Title </label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('title')"
                            :disabled="$env.changesLocked"
                            @input="push"
                            v-model="instance.title"
                            class="form-control"
                            maxlength="200"
                        />
                    </div>
                    <small class="text-muted col-12">Give your wall a title</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('description')">Description</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('description')"
                            :disabled="$env.changesLocked"
                            @input="push"
                            v-model="instance.description"
                            class="form-control"
                            maxlength="500"
                        />
                    </div>
                    <small class="text-muted col-12">Give your wall a brief description</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i
                            ><label class="form-check-label" :for="_('allow_anonymous_view')"
                                >Allow anonymous view</label
                            ></i
                        >
                    </div>
                    <div class="col-7">
                        <div class="form-check">
                            <input
                                :id="_('allow_anonymous_view')"
                                :disabled="$env.changesLocked"
                                v-model="instance.allow_anonymous_view"
                                @change="push"
                                class="form-check-input"
                                type="checkbox"
                            />
                        </div>
                    </div>
                    <small class="text-muted col-12">Any one will be able to view this wall</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label class="form-check-label" :for="_('lock_widgets')">Lock widget actions</label></i>
                    </div>
                    <div class="col-7">
                        <div class="form-check">
                            <input
                                :id="_('lock_widgets')"
                                :disabled="$env.changesLocked"
                                v-model="instance.lock_widgets"
                                @change="push"
                                class="form-check-input"
                                type="checkbox"
                            />
                        </div>
                    </div>
                    <small class="text-muted col-12">Lock widgets to prevent miss-click in edit mode </small>
                </div>
            </div>
        </template>
        <template v-else-if="instance.type == types.Container">
            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column">
                        <strong>Size</strong>
                        <span class="text-secondary">Describe container size. Container has constant width</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('h')">Height</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('h')"
                            :disabled="$env.changesLocked"
                            :step="$store.state.app.grid"
                            v-model.number="instance.h"
                            @input="push"
                            min="50"
                            class="form-control"
                            type="number"
                        />
                    </div>
                    <small class="text-warning col-12">Widgets will be recalculated to fit the container.</small>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column justify-content-center">
                        <strong>Description</strong>
                        <span class="text-secondary">Describe your container</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('title')">Title </label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('title')"
                            :disabled="$env.changesLocked"
                            v-model="instance.title"
                            @input="push"
                            class="form-control"
                            maxlength="200"
                        />
                    </div>
                    <small class="text-muted col-12">Give your container a title</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('description')">Description </label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('description')"
                            :disabled="$env.changesLocked"
                            @input="push"
                            v-model="instance.description"
                            class="form-control"
                            maxlength="500"
                        />
                    </div>
                    <small class="text-muted col-12">Give your container a description</small>
                </div>
            </div>
        </template>

        <template v-else-if="instance.type == types.Port">
            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column justify-content-center">
                        <strong>Description</strong>
                        <span class="text-secondary">How is this port connected with real world</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('title')">Title </label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('title')"
                            :disabled="$env.changesLocked"
                            v-model="instance.title"
                            @input="push"
                            class="form-control"
                            maxlength="200"
                        />
                    </div>
                    <small class="text-muted col-12">Give your port a descriptive title</small>
                </div>
            </div>
            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column justify-content-center">
                        <strong>Static link</strong>
                        <span class="text-secondary"
                            >Port is a static link to this wall. You should use ports for any external navigation, as
                            other links may change</span
                        >
                    </div>
                </div>
                <div class="row">
                    <div class="col-12 text-center">
                        <a :href="`/ext/${instance.id}/`" target="_blank">{{ origin }}/port/{{ instance.id }}/</a>
                        <a
                            @click.stop.prevent="copyToClipboard(`${origin}/port/${instance.id}/`)"
                            class="cursor-pointer"
                            ><i class="fas fa-copy mx-3 text-muted"></i
                        ></a>
                    </div>
                </div>
            </div>
        </template>

        <template v-else>
            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column">
                        <strong>Position</strong>
                        <span class="text-secondary">Describe widget position with coordinates x,y,z</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('x')">X</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('x')"
                            :disabled="$env.changesLocked"
                            :step="$store.state.app.grid"
                            v-model.number="instance.x"
                            @input="push"
                            class="form-control"
                            type="number"
                            min="0"
                        />
                    </div>
                    <small class="text-muted col-12">Left offset from parent</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('y')">Y</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('y')"
                            :disabled="$env.changesLocked"
                            :step="$store.state.app.grid"
                            v-model.number="instance.y"
                            @input="push"
                            class="form-control"
                            type="number"
                            min="0"
                        />
                    </div>
                    <small class="text-muted col-12">Top offset from parent</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('z')">Z</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('z')"
                            :disabled="$env.changesLocked"
                            v-model.number="instance.z"
                            @input="push"
                            class="form-control"
                            type="number"
                            step="1"
                            min="0"
                            max="100"
                        />
                    </div>
                    <small class="text-muted col-12">Widget with higher value will lay on top of the others</small>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column">
                        <strong>Size</strong>
                        <span class="text-secondary"
                            >Describe widget size. Size will be recalculated to fit parent.</span
                        >
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('w')">Width</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('w')"
                            :disabled="$env.changesLocked"
                            :step="$store.state.app.grid"
                            v-model.number="instance.w"
                            @input="push"
                            class="form-control"
                            type="number"
                            min="50"
                        />
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('h')">Height</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('h')"
                            :disabled="$env.changesLocked"
                            v-model.number="instance.h"
                            @input="push"
                            class="form-control"
                            type="number"
                            step="1"
                            min="50"
                        />
                    </div>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column">
                        <strong>Font</strong>
                        <span class="text-secondary">Global font settings. Text editor may override this values.</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('font_size')">Size</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('font_size')"
                            :disabled="$env.changesLocked"
                            v-model.number="instance.font_size"
                            @input="push"
                            class="form-control"
                            type="number"
                            step="1"
                            min="6"
                            max="40"
                        />
                    </div>
                    <small class="text-muted col-12">Describe how big the font is</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('font_weight')">Weight</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('font_weight')"
                            :disabled="$env.changesLocked"
                            v-model.number="instance.font_weight"
                            @input="push"
                            class="form-control"
                            type="number"
                            step="100"
                            min="100"
                            max="900"
                        />
                    </div>
                    <small class="text-muted col-12">Describe how bold the font is</small>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-12 d-flex flex-column">
                        <strong>Appearance</strong>
                        <span class="text-secondary">Global settings. Text editor may override this values.</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('background_color')">Background color</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('background_color')"
                            :disabled="$env.changesLocked"
                            v-model="instance.background_color"
                            @input="push"
                            class="form-control"
                            type="color"
                        />
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('text_color')">Text color</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('text_color')"
                            :disabled="$env.changesLocked"
                            v-model="instance.text_color"
                            @input="push"
                            class="form-control"
                            type="color"
                        />
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label class="form-check-label" :for="_('border')">Border</label></i>
                    </div>
                    <div class="col-7">
                        <div class="form-check">
                            <input
                                :id="_('border')"
                                :disabled="$env.changesLocked"
                                v-model="instance.border"
                                @change="push"
                                class="form-check-input"
                                type="checkbox"
                            />
                        </div>
                    </div>
                    <small class="text-muted col-12">Control if widget has border</small>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-12  d-flex flex-column">
                        <strong>Description</strong>
                        <span class="text-secondary">Add some information about the widget</span>
                    </div>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('title')">Title </label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('title')"
                            :disabled="$env.changesLocked"
                            v-model="instance.title"
                            @input="push"
                            class="form-control"
                        />
                    </div>
                    <small class="text-muted col-12">Name you widget</small>
                </div>
                <div class="row pb-1">
                    <div class="col-5 d-flex flex-column justify-content-center">
                        <i><label :for="_('help')">Help text</label></i>
                    </div>
                    <div class="col-7">
                        <input
                            :id="_('help')"
                            :disabled="$env.changesLocked"
                            v-model="instance.help"
                            @input="push"
                            class="form-control"
                            maxlength="200"
                        />
                    </div>
                    <small class="text-muted col-12">Describe your widget</small>
                </div>
            </div>

            <hr />

            <!--Options by widget type========================================================================================================-->
            <!--Simple text-->
            <template v-if="instance.type == types.SimpleText">
                <div class="form-group">
                    <div class="row">
                        <div class="col-12  d-flex flex-column">
                            <strong>Content</strong>
                            <span class="text-secondary">Add text content to widget</span>
                        </div>
                    </div>
                    <div class="row pb-1">
                        <div class="col-12">
                            <TextEditor v-model="instance.text_content" @input="push"></TextEditor>
                        </div>
                    </div>
                </div>
            </template>
            <!--Counter-->
            <template v-if="instance.type == types.Counter">
                <div class="form-group">
                    <div class="row">
                        <div class="col-12  d-flex flex-column">
                            <strong>Counter</strong>
                        </div>
                    </div>
                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label :for="_('value')">Value</label></i>
                        </div>
                        <div class="col-7">
                            <input
                                :id="_('value')"
                                :disabled="$env.changesLocked"
                                v-model.number="instance.value"
                                @input="push"
                                class="form-control"
                                type="number"
                            />
                        </div>
                        <small class="text-muted col-12">Set counter value</small>
                    </div>
                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label class="form-check-label" :for="_('vertical')">Vertical orientation</label></i>
                        </div>
                        <div class="col-7">
                            <div class="form-check">
                                <input
                                    :id="_('vertical')"
                                    :disabled="$env.changesLocked"
                                    v-model="instance.vertical"
                                    @change="push"
                                    class="form-check-input"
                                    type="checkbox"
                                />
                            </div>
                        </div>
                        <small class="text-muted col-12">Counter will be vertical if true, else horizontal</small>
                    </div>
                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label :for="_('step')">Step</label></i>
                        </div>
                        <div class="col-7">
                            <input
                                :id="_('step')"
                                :disabled="$env.changesLocked"
                                v-model.number="instance.step"
                                @input="push"
                                class="form-control"
                                type="number"
                            />
                        </div>
                        <small class="text-muted col-12">Value will changed with defined step</small>
                    </div>
                </div>
            </template>
            <!--Simple List-->
            <template v-if="instance.type == types.SimpleList">
                <div class="form-group">
                    <div class="row">
                        <div class="col-12  d-flex flex-column">
                            <strong>Other</strong>
                        </div>
                    </div>

                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label class="form-check-label" :for="_('inner_border')">Items border</label></i>
                        </div>
                        <div class="col-7">
                            <div class="form-check">
                                <input
                                    :id="_('inner_border')"
                                    :disabled="$env.changesLocked"
                                    v-model="instance.inner_border"
                                    @change="push"
                                    class="form-check-input"
                                    type="checkbox"
                                />
                            </div>
                        </div>
                        <small class="text-muted col-12">Set border for items</small>
                    </div>
                </div>
            </template>
            <!--URL-->
            <template v-if="instance.type == types.URL">
                <div class="form-group">
                    <div class="row">
                        <div class="col-12  d-flex flex-column">
                            <strong>URL</strong>
                        </div>
                    </div>
                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label :for="_('href')">URL address </label></i>
                        </div>
                        <div class="col-7">
                            <input
                                :id="_('href')"
                                :disabled="$env.changesLocked"
                                v-model="instance.href"
                                @input="push"
                                class="form-control"
                            />
                        </div>
                    </div>
                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label :for="_('text')">Display text</label></i>
                        </div>
                        <div class="col-7">
                            <input
                                :id="_('text')"
                                :disabled="$env.changesLocked"
                                v-model="instance.text"
                                @input="push"
                                class="form-control"
                            />
                        </div>
                        <small class="text-muted col-12">This text will be shown instead of url address</small>
                    </div>
                    <div class="row pb-1">
                        <div class="col-5 d-flex flex-column justify-content-center">
                            <i><label class="form-check-label" :for="_('open_in_new_window')">New window</label></i>
                        </div>
                        <div class="col-7">
                            <div class="form-check">
                                <input
                                    :id="_('open_in_new_window')"
                                    :disabled="$env.changesLocked"
                                    v-model="instance.open_in_new_window"
                                    @change="push"
                                    class="form-check-input"
                                    type="checkbox"
                                />
                            </div>
                        </div>
                        <small class="text-muted col-12">Open link in a new window</small>
                    </div>
                </div>
            </template>
            <!--Options by widget type========================================================================================================-->
        </template>
        <div class="form-group">
            <button :disabled="$env.changesLocked" class="btn btn-sm btn-danger w-100" @click.stop="onDeleteInstance">
                Delete
            </button>
        </div>
        <div class="form-group text-center">
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
    import { types, copyToClipboard } from "../../common";

    export default {
        name: "Options",
        data: function() {
            return {
                types,
                warningClass: "options-warning",
            };
        },
        computed: {
            instance() {
                return this.$env.makeMutable(this.$env.openOptionsFor);
            },
            origin() {
                return window.location.origin;
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
            async onDeleteInstance() {
                if (confirm("Are you sure?")) {
                    await this.$store.dispatch("deleteInstance", this.instance);
                    this.$env.closeOptions();
                }
            },
            unsetWarning() {
                $(`.${this.warningClass}`)
                    .parent()
                    .removeClass("text-danger");
                $(`.${this.warningClass}`).remove();
            },
            async push() {
                try {
                    await this.$store.dispatch("updateOrAddInstance", this.instance);
                } catch (err) {
                    return this.setWarningFromResponse(err);
                }
                this.unsetWarning();
            },
            copyToClipboard(text) {
                copyToClipboard(text);
                this.$io.alert("Copied to clipboard!", "success");
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
    .options {
        overflow-y: auto;
        overflow-x: hidden;
    }
</style>
