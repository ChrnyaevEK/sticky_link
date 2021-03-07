<template id="simple-list-template">
    <component :is="base" v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column h-100 w-100">
                <span class="w-100 text"
                    >{{ widget.title }}
                    <small class="text-muted">{{
                        widget.items.length
                    }}</small></span
                >
                <div
                    class="form-group h-100 overflow-auto  border-bottom  border-top"
                >
                    <div
                        class="border d-flex text-break my-1"
                        v-for="(val, i) of widget.items"
                        :key="i"
                    >
                        <span class="w-100 p-1">
                            {{ val }}
                        </span>
                        <a @click.stop="removeItem(i)" class="btn"
                            ><i class="fas fa-times"></i
                        ></a>
                    </div>
                </div>
                <div class="d-flex">
                    <input
                        type="text"
                        :id="_('item-input')"
                        v-model="item"
                        @keyup.enter="addItem"
                        class="form-control"
                    />
                    <a @click.stop="addItem" class="btn"
                        ><i class="fas fa-plus"></i
                    ></a>
                </div>
            </div>
        </template>
    </component>
</template>

<script>
    export default {
        type: "simple_list",
        name: "SimpleList",
        template: "#simple-list-template",
        data() {
            return {
                item: undefined, // Item to add
            };
        },
        props: {
            widget: {
                type: Object,
                required: true,
            },
            base: {
                type: Object,
                required: true,
            },
        },
        methods: {
            addItem() {
                if (this.item) {
                    if (!this.widget.items) {
                        this.widget.items = [];
                    }
                    this.widget.items.push(this.item);
                    this.item = undefined;
                }
            },
            removeItem(i) {
                this.widget.items.splice(i, 1);
            },
        },
    };
</script>

<style scoped>
    .overflow-auto::-webkit-scrollbar {
        display: none;
    }

    /* Hide scrollbar for IE, Edge and Firefox */
    .overflow-auto {
        -ms-overflow-style: none; /* IE and Edge */
        scrollbar-width: none; /* Firefox */
    }
    input, input:active, input:focus {
        background-color: inherit;
    }
</style>
