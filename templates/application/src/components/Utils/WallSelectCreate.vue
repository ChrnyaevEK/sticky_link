<template>
    <div class="btn-group dropup bg-white">
        <a
            class="btn btn-sm dropdown-toggle"
            id="wall-list"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
            title="Select any wall to open for edition"
        >
            Walls
        </a>
        <div class="mr-1 dropdown-menu" aria-labelledby="wall-list">
            <router-link
                class="dropdown-item btn btn-sm"
                v-for="wall of $store.state.walls"
                :key="wall.id"
                :class="{ active: wall.id == $route.params.wallId, 'text-secondary': !wall.title}"
                :to="{
                    name: 'wallEdit',
                    params: { wallId: wall.id },
                }"
                >{{ wall.title || '[no title]' }}</router-link
            >
        </div>
        <a
            v-if="createWall"
            class="mr-1 btn btn-sm btn-success border"
            @click="$emit('createWall')"
            title="Add new wall"
            :disabled="$env.lockChanges"
        >
            <i class="fas fa-plus"></i>
        </a>
        <a
            v-if="deleteWall"
            class="mr-1 btn btn-sm btn-danger border"
            @click.stop="$emit('deleteWall')"
            title="Delete current wall"
            :disabled="$env.lockChanges"
        >
            <i class="fas fa-trash"></i>
        </a>
    </div>
</template>
<script>
    export default {
        props: {
            createWall: {
                type: Boolean,
                default: true,
            },
            deleteWall: {
                type: Boolean,
                default: true,
            },
        },
    };
</script>
