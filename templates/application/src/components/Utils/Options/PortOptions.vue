<template>
    <div>
        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Port</span>
                <span slot="description"
                    >is a static link to wall. You should use ports for any external navigation, to be able to change
                    target wall online.</span
                >
            </options-item>
            <div class="col-12 text-center">
                <a :href="`/ext/${instance.id}/`" target="_blank">{{ origin }}/port/{{ instance.id }}/</a>
                <a @click.stop.prevent="copyToClipboard(`${origin}/port/${instance.id}/`)" class="cursor-pointer"
                    ><i class="fas fa-copy mx-3 text-muted"></i
                ></a>
            </div>
        </div>
        <div class="form-group">
            <options-item>
                <label slot="title" v-scope:for.title>Title</label>
                <input
                    slot="input"
                    v-scope:id.title
                    v-model="instance.title"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                    maxlength="200"
                />
            </options-item>
            <options-item :isHeader="true">
                <span slot="title">Target wall</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.authenticated_wall>Authenticated user</label>
                <v-select
                    slot="input"
                    class="w-100"
                    v-scope:id.authenticated_wall
                    :options="walls_as_options"
                    :reduce="(wall) => wall.code"
                    v-model="instance.authenticated_wall"
                    :key="instance.authenticated_wall"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                ></v-select>
                <span slot="help">Select wall to open for authenticated users</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.anonymous_wall>Not authenticated user</label>
                <v-select
                    slot="input"
                    class="w-100"
                    v-scope:id.anonymous_wall
                    :options="walls_as_options"
                    :reduce="(wall) => wall.code"
                    v-model="instance.anonymous_wall"
                    :key="instance.anonymous_wall"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                ></v-select>
                <span slot="help"
                    >Select wall to open for not authenticated users (or nothing to prevent N/A access from this
                    port)</span
                >
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.redirect_url>Redirect URL</label>
                <input
                    type="url"
                    slot="input"
                    v-scope:id.redirect_url
                    v-model="instance.redirect_url"
                    @input="$emit('push')"
                    :disabled="$env.state.changesLock"
                    class="form-control"
                />
                <span slot="help">If no wall specified - redirected user to this URL. </span>
            </options-item>
        </div>
    </div>
</template>
<script>
    // Front end is absolutely passive
    import OptionsItem from "./OptionsItem";
    import vSelect from "vue-select";
    import { copyToClipboard } from "../../../common";

    export default {
        name: "WallOptions",
        props: {
            instance: {
                type: Object,
                required: true,
            },
        },
        computed: {
            origin() {
                return window.location.origin;
            },
            walls_as_options() {
                if (!this.$store.state.walls) {
                    return [];
                }
                let result = [];
                for (let wall of this.$store.state.walls) {
                    result.push({
                        label: wall.title,
                        code: wall.id,
                    });
                }
                return result;
            },
        },
        methods: {
            copyToClipboard(text) {
                copyToClipboard(text);
                this.$notify({ text: "Copied to clipboard!", type: "success" });
            },
        },
        components: {
            OptionsItem,
            vSelect,
        },
    };
</script>
