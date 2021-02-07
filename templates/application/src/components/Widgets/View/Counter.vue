<template id="counter">
    <WidgetBase v-bind="{ ...$props, ...$attrs }">
        <template slot="content">
            <div class="d-flex flex-column w-100 h-100">
                <button @dblclick.stop.prevent class="btn btn-light" @click.stop="widget.value+=1"><i class="fa fa-chevron-up"></i></button>
                <div class="d-flex justify-content-center align-items-center h-100">
                    <span class="text-truncate text-wrap text-center text-break">
                        {{ widget.value }}
                    </span>
                </div>
                <button @dblclick.stop.prevent class="btn btn-light" @click.stop="widget.value-=1"><i class="fa fa-chevron-down"></i></button>
            </div>
        </template>
        <template slot="options">
            <div class="form-group">
                <label :for="_('value')"
                    >Value
                </label>
                <input :id="_('value')" class="form-control" v-model.number="widget.value" :aria-describedby="_('valueHelp')" />
            </div>
        </template>
    </WidgetBase>
</template>

<script>
    import WidgetBase from "../WidgetBase.vue";
    import { registerIdSystem } from "../../../common.js";
    export default {
        type: 'counter',
        name: "Counter",
        template: "#counter",
        props: {
            widget: {
                type: Object,
                required: true,
            },
        },
        methods:{
            test(){
                console.log(31241)
            }
        },
        created() {
            registerIdSystem(this, this.widget.type, this.widget.id); // Create _ function to generate ids
        },
        components: {
            WidgetBase,
        },
    };
</script>
