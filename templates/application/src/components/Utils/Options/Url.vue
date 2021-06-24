<template>
    <div class="form-group">
        <options-item :isHeader="true">
            <span slot="title">URL</span>
        </options-item>
        <options-item>
            <label slot="title" v-scope:for.href>URL address</label>
            <input
                slot="input"
                v-scope:id.href
                v-model="instance.href"
                @input="$emit('push')"
                :disabled="$env.state.changesLock"
                class="form-control"
            />
        </options-item>
        <options-item>
            <label slot="title" class="form-check-label" v-scope:for.open_in_new_window>New window</label>
            <input
                slot="input"
                v-scope:id.open_in_new_window
                v-model="instance.open_in_new_window"
                @change="$emit('push')"
                :disabled="$env.state.changesLock"
                type="checkbox"
            />
        </options-item>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import OptionsItem from "../Options.Item";
    export default {
        name: "UrlOptions",
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
