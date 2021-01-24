<template>
    <div class="container">
        <div class="card">
            <div class="card-body">
                <h4 class="card-title"><LoremIpsum add="1s"></LoremIpsum></h4>
                <div class="collapse" id="container-header-collapse">
                    <div class="row">
                        <div class="col-xs-12">
                            <p class="card-text">
                                <LoremIpsum add="1p"></LoremIpsum>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="text-right">
                    <a
                        class="btn btn-primary float-end"
                        data-toggle="collapse"
                        href="#container-header-collapse"
                        aria-expanded="false"
                        aria-controls="contentId"
                    >
                        Expand
                    </a>
                </div>
            </div>
            <!-- Cards here -->
        </div>
    </div>
</template>

<script>
// import SimpleTextCard from "./Cards/SimpleTextCard";
import LoremIpsum from "vue-lorem-ipsum";
export default {
    name: "Workspace",
    data: function(){
        return {
            meta: {},
            entries: [

            ]
        }
    },
    components: {
        LoremIpsum,
        // SimpleTextCard,
    },
};
</script>
