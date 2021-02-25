<template>
    <div class="btn-group dropup bg-white">
        <a class="btn btn-sm dropdown-toggle" id="wall-list" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" title="Select any wall to open for edition">
            Walls
        </a>
        <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
            <router-link
                class="dropdown-item btn btn-sm"
                v-for="wall of Context.walls"
                :key="wall.id"
                :class="{ active: wall.id == $route.params.wallId }"
                :to="{
                    name: 'wall',
                    params: { wallId: wall.id },
                    query: { mode: Context.edit },
                }"
                >{{ wall.title }}</router-link
            >
        </div>
        <a class="mr-1 btn btn-sm btn-success border" @click="Context.$emit('addBlankWall')" title="Add new wall">
            <i class="fas fa-plus"></i>
        </a>
    </div>
</template>
<script>
    import { Context } from "../common.js";
    export default {
        data() {
            return { Context };
        },
    };
</script>
