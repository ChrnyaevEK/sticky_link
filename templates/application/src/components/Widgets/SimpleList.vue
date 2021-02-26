<template id="simple-list-template">
    <component
        :is="base"
        v-bind="{ ...$props, ...$attrs }"
    >
        <template slot="content">
            <div class="d-flex flex-column h-100 w-100">
                <span class="w-100 text mx-1">{{ widget.title }}</span>
                <small class="w-100 text mx-1">{{ widget.description }}</small>
                <div class="form-group h-100 overflow-auto">
                    <div
                        class="border d-flex text-break m-1"
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
                <div class="p-1 border-top">
                    <div class="d-flex">
                        <input
                            @dblclick.stop
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
            </div>
        </template>
    </component>
</template>

<script>
    import { registerIdSystem, Context  } from "../../common.js";
    export default {
        type: "simple_list",
        name: "SimpleList",
        template: "#simple-list-template",
        data() {
            return {
                item: "", // Item to add
                Context,
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
            }
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        methods: {
            addItem() {
                if (this.item) {
                    if (!this.widget.items) {
                        this.$set(this.widget, "items", []);
                    }
                    this.widget.items.push(this.item);
                    this.item = "";
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
</style>
