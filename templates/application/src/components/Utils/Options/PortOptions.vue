<template>
    <div>
        <div class="form-group">
            <options-item :isHeader="true">
                <span slot="title">Static link</span>
                <span slot="description"
                    >Port is a static link to this wall. You should use ports for any external navigation, to be able to
                    change target wall online.</span
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
            <options-item :isHeader="true">
                <span slot="title">Description</span>
                <span slot="description">How is this port connected with real world</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.title>Title</label>
                <input
                    slot="input"
                    v-scope:id.title
                    v-model="instance.title"
                    @input="$emit('push')"
                    :disabled="$env.changesLocked"
                    class="form-control"
                    maxlength="200"
                />
                <span slot="help">Give your port a descriptive title</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.wall>Move port to wall...</label>
                <v-select
                    slot="input"
                    class="w-100"
                    v-scope:id.wall
                    :options="walls_as_options"
                    :reduce="(wall) => wall.code"
                    v-model="instance.wall"
                    :key="instance.wall"
                    @input="$emit('push')"
                    :disabled="$env.changesLocked"
                ></v-select>
                <span slot="help">Port will disappear from this wall after update.</span>
            </options-item>
            <options-item>
                <label slot="title" v-scope:for.redirect_url>Redirect URL</label>
                <input
                    slot="input"
                    type="url"
                    v-scope:id.redirect_url
                    v-model="instance.redirect_url"
                    @input="$emit('push')"
                    :disabled="$env.changesLocked"
                    class="form-control"
                />
                <span slot="help">Redirect to any address. If no address specified - redirect to selected wall</span>
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
                this.$io.alert("Copied to clipboard!", "success");
            },
        },
        components: {
            OptionsItem,
            vSelect,
        },
    };
</script>
