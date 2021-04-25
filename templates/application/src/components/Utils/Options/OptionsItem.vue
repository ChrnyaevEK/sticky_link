<template>
    <div v-if="isHeader" class="row pb-1">
        <div class="col-12  d-flex flex-column justify-content-center">
            <strong>
                <slot name="title"></slot>
            </strong>
            <span class="text-secondary">
                <slot name="description"></slot>
            </span>
        </div>
    </div>
    <div v-else class="row pb-1">
        <div class="col-5 d-flex flex-column justify-content-center">
            <slot name="title"></slot>
        </div>
        <div class="col-7 d-flex justify-content-end">
            <slot name="input"></slot>
        </div>
        <small class="text-muted col-12">
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
