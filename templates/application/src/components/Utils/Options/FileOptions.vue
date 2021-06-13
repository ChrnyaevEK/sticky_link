<template>
    <div>
        <options-item :isHeader="true">
            <span slot="title">Content</span>
        </options-item>
        <options-item>
            <div class="mb-3 d-flex flex-column" slot="input">
                <div class="d-flex">
                    <input v-scope:id.content :disabled="$env.state.changesLock" type="file" />
                    <button class="btn btn-success mr-1" @click="upload"><i class="fas fa-upload"></i></button>
                    <button class="btn btn-danger"><i class="fas fa-trash"></i></button>
                </div>
                <div class="text-danger" v-show="error">{{ error }}</div>
            </div>
        </options-item>
    </div>
</template>

<script>
    import OptionsItem from "./OptionsItem";
    import $ from "jquery";
    export default {
        name: "FileOptions",
        components: {
            OptionsItem,
        },
        props: {
            instance: {
                type: Object,
                required: true,
            },
        },
        data() {
            return {
                error: null,
            };
        },
        methods: {
            upload() {
                var file = $("#" + this._("content")).get(0).files[0];
                if (file != undefined) {
                    if (file.size <= this.$store.state.meta.file_size_max) {
                        this.error = null;
                        var data = new FormData(); //Create formdata objects to facilitate file transfer to the back end
                        data.append("file", file); //To add (encapsulate) a file object to a formdata object
                        return this.$store.dispatch('uploadContent', {
                            name: file.name,
                            content: data,
                        })
                    }
                    return (this.error = "File is larger than 10Mb");
                }
                return (this.error = "File not selected");
            },
        },
    };
</script>
