<template>
    <div>
        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Position</span>
                <span slot="description">Describe widget position with coordinates x,y,z</span>
            </options-item>
            <options-item>
                <label v-scope:for.x slot="title">X</label>
                <input
                    slot="input"
                    v-scope:id.x
                    :step="$store.state.app.grid"
                    v-model.number="instance.x"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    min="0"
                />
            </options-item>
            <options-item>
                <label v-scope:for.y slot="title">Y</label>
                <input
                    slot="input"
                    v-scope:id.y
                    :step="$store.state.app.grid"
                    v-model.number="instance.y"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    min="0"
                />
            </options-item>
            <options-item>
                <label v-scope:for.z slot="title">Z</label>
                <input
                    slot="input"
                    v-scope:id.z
                    :step="$store.state.app.grid"
                    v-model.number="instance.z"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    min="0"
                    max="100"
                />
                <span slot="help">Widget with higher value will lay on top of the others</span>
            </options-item>
        </div>

        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Size</span>
                <span slot="description">Describe widget size. Size will be recalculated to fit parent.</span>
            </options-item>
            <options-item>
                <label v-scope:for.w slot="title">Width</label>
                <input
                    slot="input"
                    v-scope:id.w
                    :step="$store.state.app.grid"
                    v-model.number="instance.w"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    min="50"
                />
            </options-item>

            <options-item>
                <label v-scope:for.h slot="title">Height</label>
                <input
                    slot="input"
                    v-scope:id.h
                    v-model.number="instance.h"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    step="1"
                    min="50"
                />
            </options-item>
        </div>

        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Font</span>
                <span slot="description">Global font settings. Text editor may override this values.</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.font_size>Size</label>
                <input
                    slot="input"
                    v-scope:id.font_size
                    v-model.number="instance.font_size"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    step="1"
                    min="6"
                    max="40"
                />
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.font_weight>Weight</label>
                <input
                    slot="input"
                    v-scope:id.font_weight
                    v-model.number="instance.font_weight"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="number"
                    step="100"
                    min="100"
                    max="900"
                />
                <span slot="help">Describe how bold the font is</span>
            </options-item>
        </div>

        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Appearance</span>
                <span slot="description">Global settings. Text editor may override this values.</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.background_color>Background color</label>
                <input
                    slot="input"
                    v-scope:id.background_color
                    v-model="instance.background_color"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="color"
                />
            </options-item>

            <options-item>
                <label slot="title" v-scope:for.text_color>Text color</label>
                <input
                    slot="input"
                    v-scope:id.text_color
                    v-model="instance.text_color"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="color"
                />
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.border>Border</label>
                <input
                    slot="input"
                    v-scope:id.border
                    v-model="instance.border"
                    @change="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-check-input"
                    type="checkbox"
                />
                <span slot="help">Control if widget has border</span>
            </options-item>
        </div>

        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Description</span>
                <span slot="description">Add some information about the widget</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.title>Title</label>
                <input
                    slot="input"
                    v-scope:id.title
                    v-model="instance.title"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                />
                <span slot="help">Name you widget</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.help>Help text</label>
                <input
                    slot="input"
                    v-scope:id.help
                    v-model="instance.help"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    maxlength="200"
                />
                <span slot="help">Describe your widget</span>
            </options-item>
        </div>

        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Synchronization</span>
                <span slot="description"
                    >Setup synchronization with another widget of the <strong>same type</strong>. Only value fields are
                    synchronized, not size or position</span
                >
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.sync_id>Synchronize with ...</label>
                <input
                    slot="input"
                    v-scope:id.sync_id
                    v-model="instance.sync_id"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    type="text"
                    maxlength="20"
                />
                <span slot="help">Pass <strong>Sync Id</strong> of the widget you want to synchronize with</span>
            </options-item>
            <options-item>
                <label slot="title">Sync Id</label>
                <button slot="input" class="w-100 btn btn-sm border" @click="copyToClipboard(instance.id)">
                    {{ instance.id }}
                    <i class="fas fa-copy mx-3 text-muted"></i>
                </button>
                <span slot="help"><strong>Sync Id</strong> of this widget</span>
            </options-item>
        </div>

        <hr />

        <counter-options
            v-if="instance.type == types.Counter"
            :instance="instance"
            @push="$emit('push')"
            :disabled="$env.state.changesLock"
        ></counter-options>
        <url-options
            v-if="instance.type == types.URL"
            :instance="instance"
            @push="$emit('push')"
            :disabled="$env.state.changesLock"
        ></url-options>
        <simple-text-options
            v-if="instance.type == types.SimpleText"
            :instance="instance"
            @push="$emit('push')"
            :disabled="$env.state.changesLock"
        ></simple-text-options>
        <simple-list-options
            v-if="instance.type == types.SimpleList"
            :instance="instance"
            @push="$emit('push')"
            :disabled="$env.state.changesLock"
        ></simple-list-options>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import OptionsItem from "./OptionsItem";
    import CounterOptions from "./CounterOptions";
    import SimpleListOptions from "./SimpleListOptions";
    import SimpleTextOptions from "./SimpleTextOptions";
    import UrlOptions from "./UrlOptions";
    import { copyToClipboard, types } from "../../../common";

    export default {
        name: "WidgetsOptions",
        props: {
            instance: {
                type: Object,
                required: true,
            },
        },
        data: () => {
            return {
                types,
            };
        },
        methods: {
            copyToClipboard(text) {
                copyToClipboard(text);
                this.$notify({ text: "Copied to clipboard!", type: "success" });
            },
        },
        components: {
            OptionsItem,
            CounterOptions,
            SimpleListOptions,
            SimpleTextOptions,
            UrlOptions,
        },
    };
</script>
