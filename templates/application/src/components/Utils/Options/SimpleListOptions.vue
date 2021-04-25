<template>
    <div>
        <options-item :isHeader="true">
            <span slot="title">Simple List</span>
        </options-item>
        <options-item>
            <label slot="title" v-scope:for.inner_border>Items border</label>
            <input
                slot="input"
                v-scope:id.inner_border
                v-model="instance.inner_border"
                @change="$emit('push')"
                :disabled="$env.changesLocked"
                class="form-check-input"
                type="checkbox"
            />
            <span slot="help">Set border for items</span>
        </options-item>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import OptionsItem from "./OptionsItem";

    export default {
        name: "SimpleListOptions",
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
