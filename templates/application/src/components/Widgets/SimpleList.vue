<template id="simple-list-template">
    <WidgetBaseResizable :widget="widget">
        <div class="h-100 d-flex flex-column">
            <div class="text-secondary text-truncate" :title="widget.title">
                {{ widget.title }}
            </div>
            <div class="flex-grow-1" :class="$env.state.editMode ? 'overflow-hidden' : 'overflow-auto'">
                <div
                    class="d-flex mb-1 align-items-start"
                    :class="{ border: widget.inner_border }"
                    v-for="(val, i) of widget.items"
                    :key="i"
                >
                    <div class="d-flex flex-grow-1 p-1 text-break">
                        <span class="mr-1 text-secondary text-nowrap">{{ i + 1 }}.</span>
                        <span>{{ val }}</span>
                    </div>
                    <button
                        @click.stop="removeItem(i)"
                        :disabled="$env.state.widgetsLock || $env.state.changesLock"
                        class="btn btn-sm text-danger"
                    >
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="d-flex">
                <input
                    type="text"
                    v-scope:id.item-input
                    v-model="item"
                    @keyup.enter="addItem"
                    class="form-control"
                    :disabled="$env.state.widgetsLock || $env.state.changesLock"
                />
                <button @click.stop="addItem" :disabled="$env.state.widgetsLock || $env.state.changesLock" class="btn">
                    <i class="fas fa-plus"></i>
                </button>
            </div>
        </div>
    </WidgetBaseResizable>
</template>

<script>
    import { deepCopy } from "../../common";
    import WidgetBaseResizable from "../Widgets/WidgetBaseResizable";

    export default {
        type: "simple_list",
        name: "SimpleList",
        template: "#simple-list-template",
        components: { WidgetBaseResizable },
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
        },
        methods: {
            addItem() {
                if (this.item && !this.$env.state.widgetsLock) {
                    var items = this.widget.items ? deepCopy(this.widget.items) : [];
                    items.push(this.item);
                    this.item = undefined;
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { items }));
                }
            },
            removeItem(i) {
                if (this.widget.items && !this.$env.state.widgetsLock) {
                    var items = deepCopy(this.widget.items);
                    items.splice(i, 1);
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { items }));
                }
            },
        },
    };
</script>

<style scoped>
    input,
    input:active,
    input:focus {
        background-color: inherit;
    }
</style>
