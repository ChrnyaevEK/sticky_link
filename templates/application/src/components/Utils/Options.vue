<template>
    <div>
        <div class="text-right">
            <a class="btn" @click="$env.dispatch('closeOptions')"><i class="fas fa-times"></i></a>
        </div>
        <wall-options v-if="instance.type === types.Wall" :instance="instance" @push="handlePush"></wall-options>
        <container-options
            v-else-if="instance.type === types.Container"
            :instance="instance"
            @push="handlePush"
        ></container-options>
        <widgets-options v-else :instance="instance" @push="handlePush"></widgets-options>
        <div class="form-group">
            <button
                :disabled="$env.state.changesLock"
                class="btn btn-sm btn-danger w-100"
                @click.stop="handleInstanceDelete"
            >
                Delete
            </button>
        </div>
        <div class="form-group text-center">
            <small class="text-secondary">All changes are automatically saved</small>
        </div>
    </div>
</template>

<script>
    import $ from "jquery";
    import WallOptions from "./Options/Wall";
    import ContainerOptions from "./Options/Container";
    import WidgetsOptions from "./Options/WidgetsOptions";
    import { types } from "../../common";

    export default {
        name: "Options",
        data: function() {
            return {
                types,
                warningClass: "options-warning",
                warningClassField: "options-warning-field",
            };
        },
        computed: {
            instance() {
                return Object.assign({}, this.$env.state.optionsSource);
            },
        },
        methods: {
            async handleInstanceDelete() {
                if (confirm("Are you sure?")) {
                    let type = this.instance.type;

                    await this.$store.dispatch("deleteInstance", this.instance);

                    this.$env.dispatch("closeOptions");
                    if (type === "wall") {
                        this.$env.dispatch("handleWallDeleted");
                    }
                }
            },
            async handlePush() {
                try {
                    await this.$store.dispatch("updateOrAddInstance", this.instance);
                } catch (err) {
                    return this.setWarningFromResponse(err);
                }
                this.unsetWarning();
            },
        },
        components: {
            WallOptions,
            ContainerOptions,
            WidgetsOptions,
        },
    };
</script>

<style scoped>
    .options-size {
        max-height: 600px;
        min-width: 200px;
        max-width: 400px;
        width: 50% !important;
    }
    .options-position {
        position: fixed;
        top: 0;
        right: 0;
    }
    .options {
        overflow-y: auto;
        overflow-x: hidden;
    }
</style>
