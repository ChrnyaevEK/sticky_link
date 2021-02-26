<template>
    <vue-editor :value="value" :editorOptions="editorOptions" :editorToolbar="customToolbar" @input="$emit('input', $event)"></vue-editor>
</template>
<script>
    import { VueEditor } from "vue2-editor";
    var formats = ["bold", "color", "font", "code", "italic", "link", "size", "strike", "script", "underline", "blockquote", "header", "indent", "list", "align", "direction", "code-block"];
    export default {
        components: {
            VueEditor,
        },
        props: ["value"],
        data() {
            return {
                customToolbar: [
                    [{ font: [] }, { size: [] }, { header: ["1", "2", "3", "4", "5", "6"] }],
                    ["bold", "italic", "underline", "strike"],
                    [{ color: [] }, { script: "super" }, { script: "sub" }],
                    ["blockquote", "code-block"],
                    [{ list: "ordered" }, { list: "bullet" }, { indent: "-1" }, { indent: "+1" }],
                    ["direction", { align: [] }],
                    ["link", "clean"],
                ],
                editorOptions: {
                    placeholder: "Lorem ipsum dolor sit amet",
                    formats,
                },
            };
        },
    };
</script>
