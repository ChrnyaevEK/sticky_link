<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12 col-md-2">
                <div class="font-weight-bold border-bottom p-3">Widgets</div>
                <div id="workspace-widget-selector" role="tablist" aria-multiselectable="true">
                    <div class="card border-0">
                        <div class="card-header p-2 bg-light" role="tab" id="section-1-header">
                            <a data-toggle="collapse" data-parent="#workspace-widget-selector" href="#section-1-body" aria-expanded="true" aria-controls="section-1-body">
                                Text widgets
                            </a>
                        </div>
                        <div id="section-1-body" class="collapse in" role="tabpanel" aria-labelledby="section-1-header">
                            <div class="card-body p-2 row">
                                <div class="col-10">Simple text card</div>
                                <div class="col-2"><i class="fas fa-plus"></i></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-10" id="workspace-widget-list"></div>
        </div>
    </div>
</template>

<script>
    // import SimpleTextCard from "./Cards/SimpleTextCard";
    // import LoremIpsum from "vue-lorem-ipsum";
    export default {
        name: "Workspace",
        data: function() {
            return {
                meta: {},
                entries: [],
            };
        },
        components: {
            // LoremIpsum,
            // SimpleTextCard,
        },
    };
</script>
