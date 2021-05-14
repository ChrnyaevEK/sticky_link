<template>
    <div class="form-group">
        <options-item :isHeader="true">
            <span slot="title">Description</span>
            <span slot="description">Tell more about this wall</span>
        </options-item>
        <options-item>
            <label v-scope:for.title slot="title">Title</label>
            <input
                slot="input"
                @input="$emit('push')"
                :disabled="$env.state.changesLock"
                v-model="instance.title"
                v-scope.id:title
                class="form-control"
                maxlength="200"
            />
            <span slot="help">Give your wall a title</span>
        </options-item>
        <options-item>
            <label v-scope:for.description slot="title">Description</label>
            <input
                slot="input"
                v-scope:id.description
                @input="$emit('push')"
                :disabled="$env.state.changesLock"
                v-model="instance.description"
                class="form-control"
                maxlength="500"
            />
            <span slot="help">Give your wall a brief description</span>
        </options-item>
        <options-item>
            <label v-scope:for.allow_anonymous_view slot="title">Allow anonymous view</label>
            <input
                slot="input"
                v-scope:id.allow_anonymous_view
                v-model="instance.allow_anonymous_view"
                @change="$emit('push')"
                :disabled="$env.state.changesLock"
                class="form-check-input"
                type="checkbox"
            />
            <span slot="help">Any one will be able to view this wall</span>
        </options-item>
        <options-item>
            <label v-scope:for.lock_widgets slot="title">Lock widget actions</label>
            <input
                slot="input"
                v-scope:id.lock_widgets
                v-model="instance.lock_widgets"
                @change="$emit('push')"
                :disabled="$env.state.changesLock"
                class="form-check-input"
                type="checkbox"
            />
            <span slot="help">Lock widgets to prevent miss-click in edit mode</span>
        </options-item>
    </div>
</template>
<script>
    // Front end is absolutely passive
    import OptionsItem from "./OptionsItem";
    export default {
        name: "WallOptions",
        props: {
            instance: {
                type: Object,
                required: true,
            },
        },
        components: {
            OptionsItem,
        },
    };
</script>
