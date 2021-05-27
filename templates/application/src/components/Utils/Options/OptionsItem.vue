<template>
    <div v-if="isHeader" class="pb-1">
        <span class="mr-1">
            <slot name="title"></slot>
        </span>
        <span class="text-secondary">
            <slot name="description"></slot>
        </span>
    </div>
    <div v-else class="form-group">
        <slot name="title"></slot>
        <slot name="input"></slot>
        <small class="text-secondary">
            <slot name="help"></slot>
        </small>
    </div>
</template>
<script>
    export default {
        name: "Option",
        props: {
            isHeader: {
                type: Boolean,
                default: false,
            },
        },
    };
</script>
