<template>
    <vue-resizable
        @resize:end="onResizeEnd"
        @drag:end="onDragEnd"
        :fitParent="true"
        class="widget rounded bg-white"
        ref="resizable"
        :dragSelector="_('#sidebar')"
        :width="width"
        :minWidth="minWidth"
        :height="height"
        :minHeight="minHeight"
    >
        <div class="d-flex justify-content-between control-area">
            <div class="content mx-1">
                <slot name="content">
                    <div class="content-empty d-flex align-items-center justify-content-center">
                        <div class="text-secondary">Nothing is here yet... <i class="far fa-frown"></i></div>
                    </div>
                </slot>
            </div>
            <div :id="_('sidebar')" class="sidebar bg-light">
                <div class="dropdown">
                    <span class="btn" :id="_('widget-options')" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i class="fas fa-ellipsis-v"></i></span>
                    <div class="dropdown-menu" :aria-labelledby="_('widget-options')">
                        <a class="dropdown-item" href="#">Edit</a>
                        <a class="dropdown-item" href="#">Disable</a>
                        <a class="dropdown-item" href="#">Delete</a>
                        <slot name="options"></slot>
                    </div>
                </div>
            </div>
        </div>
    </vue-resizable>
</template>

<script>
    // Front end is absolutely passive
    import VueResizable from "vue-resizable";
    import { registerIdSystem } from "../../common.js";
    export default {
        name: "WidgetBase",
        props: {
            id: {
                type: Number,
                required: true,
            },
            width: {
                type: Number,
                default: 200, // Fallback value
            },
            minWidth: {
                type: Number,
                default: 200, // Fallback value
            },
            height: {
                type: Number,
                default: 100, // Fallback value
            },
            minHeight: {
                type: Number,
                default: 100, // Fallback value
            },
            zIndex: {
                // TODO
                type: Number,
                required: false,
            },
            left: {
                // TODO
                type: Number,
                required: false,
            },
            top: {
                // TODO
                type: Number,
                required: false,
            },
            textColor: {
                // TODO
                type: String,
                required: false,
            },
            backgroundColor: {
                // TODO
                type: String,
                required: false,
            },
            dateOfCreation: {
                // TODO
                type: String,
                required: false,
            },
            lastUpdate: {
                // TODO
                type: String,
                required: false,
            },
        },
        created: function() {
            registerIdSystem(this); // Create _ function to generate ids
        },
        methods: {
            onResizeEnd: function(eventName, left, top, width, height) {
                console.log(eventName, left, top, width, height);
            },
            onDragEnd: function(eventName, left, top, width, height) {
                console.log(eventName, left, top, width, height);
            },
        },
        components: {
            VueResizable,
        },
    };
</script>

<style scoped>
    .widget {
        position: absolute;
        border-style: solid;
        border-width: 1px;
        border-color: rgb(189, 189, 189);
        margin: 0;
        padding: 0;
    }
    .widget .control-area {
        width: 100%;
        height: 100%;
    }
    .widget .content,
    .widget .content-empty {
        width: 100%;
        height: 100%;
    }
    .widget .sidebar {
        height: 100%;
    }
    .widget .sidebar:hover {
        cursor: grab;
    }
</style>
