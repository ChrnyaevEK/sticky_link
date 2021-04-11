<template id="simple-list-template">
    <WidgetBaseResizable :widget="widget">
        <span class="w-100 text"
            >{{ widget.title }} <small class="text-muted">{{ widget.items.length }}</small></span
        >
        <div class="form-group w-100 h-100 overflow-auto border-bottom border-top py-1">
            <div
                class="d-flex text-break mb-1"
                :class="{ border: widget.inner_border }"
                v-for="(val, i) of widget.items"
                :key="i"
            >
                <span class="w-100 p-1">
                    {{ val }}
                </span>
                <button @click.stop="removeItem(i)" :disabled="$env.widgetsLocked || $env.changesLocked" class="btn">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
        <div class="d-flex">
            <input
                type="text"
                :id="_('item-input')"
                v-model="item"
                @keyup.enter="addItem"
                class="form-control"
                :disabled="$env.widgetsLocked || $env.changesLocked"
            />
            <button @click.stop="addItem" :disabled="$env.widgetsLocked || $env.changesLocked" class="btn">
                <i class="fas fa-plus"></i>
            </button>
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
                if (this.item && !this.$env.widgetsLocked) {
                    var items = this.widget.items ? deepCopy(this.widget.items) : [];
                    items.push(this.item);
                    this.item = undefined;
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { items }));
                }
            },
            removeItem(i) {
                if (this.widget.items && !this.$env.widgetsLocked) {
                    var items = deepCopy(this.widget.items);
                    items.splice(i, 1);
                    this.$store.dispatch("updateOrAddInstance", Object.assign({}, this.widget, { items }));
                }
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
    input,
    input:active,
    input:focus {
        background-color: inherit;
    }
</style>
