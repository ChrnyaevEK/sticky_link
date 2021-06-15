<template>
    <div>
        <options-item :isHeader="true">
            <span slot="title">Content</span>
        </options-item>
        <options-item>
            <div class="mb-3 d-flex flex-column" slot="input">
                <div class="d-flex mb-1">
                    <input
                        class="form-control-file"
                        v-scope:id.content
                        :disabled="$env.state.changesLock"
                        type="file"
                    />
                    <button class="btn btn-sm text-success mx-2" @click="upload"><i class="fas fa-upload"></i></button>
                </div>
                <div class="d-flex justify-content-between mb-1" v-if="instance.source && instance.source.file">
                    <a :href="sourceURL" target="_blank" class="text-truncate">{{ instance.source.name }}</a>
                    <button class="btn btn-sm text-danger mx-2" @click="remove"><i class="fas fa-trash"></i></button>
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
        computed: {
            sourceURL() {
                if (this.instance.source && this.instance.source.file) {
                    return process.env.VUE_APP_API_HOST + "/source/" + this.instance.source.id + "/";
                }
                return false;
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
                        var data = new FormData(); //Create form data objects to facilitate file transfer to the back end
                        data.append("file", file); //To add (encapsulate) a file object to a formdata object
                        return this.$store.dispatch("uploadSource", {
                            instance: this.instance,
                            name: file.name,
                            data,
                        });
                    }
                    return (this.error = "File is larger than 10Mb");
                }
                return (this.error = "File not selected");
            },
            remove() {
                return this.$store.dispatch("removeSource", this.instance);
            },
        },
    };
</script>
