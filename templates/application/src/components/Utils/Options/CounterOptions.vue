<!-- ---------------------------------------------- -->

<template>
    <div>
        <options-item :isHeader="true">
            <span slot="title">Counter</span>
        </options-item>
        <options-item>
            <label slot="title" v-scope:for.value>Value</label>
            <input
                slot="input"
                v-scope:id.value
                v-model.number="instance.value"
                @input="$emit('push')"
                :disabled="$env.changesLocked"
                class="form-control"
                type="number"
            />
            <span slot="help">Set counter value</span>
        </options-item>
        <options-item>
            <label slot="title" v-scope:for.vertical>Vertical orientation</label>
            <input
                slot="input"
                v-scope:id.vertical
                v-model="instance.vertical"
                @change="$emit('push')"
                :disabled="$env.changesLocked"
                class="form-check-input"
                type="checkbox"
            />
            <span slot="help">Counter will be vertical if true, else horizontal</span>
        </options-item>
        <options-item>
            <label slot="title" v-scope:for.step>Step</label>
            <input
                slot="input"
                v-scope:id.step
                v-model.number="instance.step"
                @input="$emit('push')"
                :disabled="$env.changesLocked"
                class="form-control"
                type="number"
            />
            <span slot="help">Value will changed with defined step</span>
        </options-item>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import OptionsItem from "./OptionsItem";

    export default {
        name: "CounterOptions",
        components: {
            OptionsItem,
        },
        props: {
            instance: {
                type: Object,
                required: true,
            },
        },
    };
</script>
