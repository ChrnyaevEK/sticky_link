<template id="simple-list-widget">
    <WidgetBase v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column h-100 w-100">
                <span class="w-100 text">{{ widget.title }}</span>
                <small class="w-100 text">{{ widget.description }}</small>
                <div class="form-group w-drag h-100 overflow-auto">
                    <div class="border p-1 my-1" v-for="(val, i) of widget.items" :key="i">
                        <div class="d-flex text-break">
                            <span class="w-100">
                                {{ val }}
                            </span>
                            <a @click.stop="removeItem(i)" class="col-2 btn w-drag"><i class="fas fa-times"></i></a>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="d-flex">
                        <input @dblclick.stop type="text" id="_('item-input')" v-model="item" @keyup.enter="addItem" class="form-control" />
                        <a @click.stop="addItem" class="col-2 btn w-drag"><i class="fas fa-plus"></i></a>
                    </div>
                </div>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('title')"
                    >Title
                </label>
                <input :id="_('title')" class="form-control" v-model.number="widget.title" :aria-describedby="_('titleHelp')" />
            </div>            
            <div class="form-group">
                <label :for="_('description')"
                    >Description
                </label>
                <input :id="_('description')" class="form-control" v-model.number="widget.description" :aria-describedby="_('descriptionHelp')" />
            </div>
        </template>
    </WidgetBase>
</template>

<script>
    import WidgetBase from "./WidgetBase";
    import { registerIdSystem } from "../../common.js";
    export default {
        type: "simple_list",
        name: "SimpleList",
        template: "#simple-list-widget",
        data() {
            return {
                item: "", // Item to add
            };
        },
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        components: {
            WidgetBase,
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
            removeItem(i){
                this.widget.items.splice(i, 1)
            }
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