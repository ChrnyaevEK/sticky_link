<template>
    <div v-if="isHeader">
        <strong class="mr-1"><slot name="title"></slot></strong>
        <span class="text-secondary"><slot name="description"></slot></span>
    </div>
    <div v-else class="form-group">
        <div class="ml-2 d-flex flex-column">
            <slot name="title"></slot>
            <slot name="input"></slot>
            <small class="text-secondary">
                <slot name="help"></slot>
            </small>
        </div>
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
