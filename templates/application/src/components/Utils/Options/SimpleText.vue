<template>
    <div class="form-group">
        <options-item :isHeader="true">
            <span slot="title">Content</span>
        </options-item>
        <TextEditor v-model="instance.text_content" @input="$emit('push')" :disabled="$env.state.changesLock"></TextEditor>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import OptionsItem from "../Options.Item";
    import TextEditor from "../TextEditor";

    export default {
        name: "SimpleTextOptions",
        props: {
            instance: {
                type: Object,
                required: true,
            },
        },

        components: {
            TextEditor,
            OptionsItem,
        },
    };
</script>
