<template>
    <div v-if="$env.state.optionsSource" class="w-100">
        <div class="form-group d-flex justify-content-between align-items-center options-drag cursor-move">
            <strong>Options</strong>
            <a class="btn" @click="$env.dispatch('closeOptions')"><i class="fas fa-times"></i></a>
        </div>
        <hr />
        <wall-options v-if="instance.type == types.Wall" :instance="instance" @push="handlePush"></wall-options>
        <container-options
            v-else-if="instance.type == types.Container"
            :instance="instance"
            @push="handlePush"
        ></container-options>
        <port-options v-else-if="instance.type == types.Port" :instance="instance" @push="handlePush"></port-options>
        <widgets-options v-else :instance="instance" @push="handlePush"></widgets-options>
        <div class="form-group">
            <button :disabled="$env.state.changesLock" class="btn btn-danger w-100" @click.stop="handleInstanceDelete">
                Delete
            </button>
        </div>
        <div class="form-group text-center">
            <small class="text-secondary">All changes are automatically saved</small>
        </div>
    </div>
</template>

<script>
    // Front end is absolutely passive
    import $ from "jquery";
    import WallOptions from "./Options/WallOptions";
    import ContainerOptions from "./Options/ContainerOptions";
    import PortOptions from "./Options/PortOptions";
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
                    if (type == "wall") {
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
            setWarningFromResponse(response) {
                this.unsetWarning();
                for (var [field, error] of Object.entries(response.responseJSON)) {
                    error = $(`<p class="${this.warningClass} col-12 text-danger">${error[0]}</p>`);
                    $(this.$el)
                        .find(`[for*="${field}"]`)
                        .addClass(`text-danger ${this.warningClassField}`)
                        .closest(".row")
                        .append(error);
                }
            },
            unsetWarning() {
                $(`.${this.warningClassField}`).removeClass("text-danger");
                $(`.${this.warningClass}`).remove();
            },
        },
        components: {
            WallOptions,
            ContainerOptions,
            PortOptions,
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
