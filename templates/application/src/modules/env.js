import Vue from "vue";
import VueX from "vuex";
import store from "./store";
import router from "./router";

Vue.use(VueX);

async function nextTick() {
    await new Promise((resolve) => {
        Vue.nextTick(resolve);
    });
}

export default new VueX.Store({
    state: {
        wall: null,
        container: null,
        changesLock: false, // Look resizing, dragging, instance mutations
        widgetsLock: false,
        editMode: false,
        viewMode: false,
        optionsSource: null,
    },
    mutations: {
        setWallByWallId(state, wall) {
            state.wall = wall;
        },
        setContainerByContainerId(state, containerId) {
            state.container = store.state.containers
                ? store.state.containers.filter((c) => c.id == containerId)[0]
                : null;
        },
        setEditMode(state) {
            state.editMode = true;
            state.viewMode = false;
        },
        setViewMode(state) {
            state.editMode = false;
            state.viewMode = true;
        },
        setChangesLock(state, lock) {
            state.changesLock = lock;
        },
        setWidgetsLock(state, lock) {
            state.widgetsLock = lock;
        },
        setOptionsSource(state, source) {
            state.optionsSource = source;
        },
        //this.edit && this.wall && this.wall.lock_widgets
    },

    actions: {
        async handleCreateWidget(context, type) {
            let widget = await store.dispatch("createInstance", {
                type,
                container: context.state.container.id,
            });
            store.dispatch("recalculateWidgets", context.state.container);
            Vue.notify({
                text: `Widget ${widget.type} ${widget.title || "Untitled"} was created!`,
                type: "success",
            });
        },
        async handleCreateContainer(context) {
            let index = 0;
            for (let container of store.state.containers) {
                if (container.index > index) {
                    index = container.index + 1;
                }
            }
            let container = await store.dispatch("createInstance", {
                wall: context.state.wall.id,
                type: "container",
                index,
            });
            Vue.notify({
                text: `Container ${container.title || "Untitled"} was created!`,
                type: "success",
            });
        },
        async handleCreatePort(context) {
            let port = await store.dispatch("createInstance", {
                wall: context.state.wall.id,
                type: "port",
            });
            context.dispatch("openOptions", port);
            Vue.notify({
                text: `Port ${port.title || "Untitled"} was created!`,
                type: "success",
            });
        },
        async handleCreateWall() {
            let wall = await store.dispatch("createInstance", {
                type: "wall",
            });
            Vue.notify({
                text: `Wall ${wall.title || "Untitled"} was created!`,
                type: "success",
            });
            router.push({
                name: "wallEdit",
                params: {
                    wallId: wall.id,
                },
            });
        },
        handleWallDeleted(context) {
            router.push({ name: context.state.editMode ? "wallEdit" : "wallView" });
        },
        async setEditMode(context) {
            context.commit("setEditMode");
            await nextTick();
        },
        async setViewMode(context) {
            context.commit("setViewMode");
            await nextTick();
        },
        async setWallByWallId(context, wallId) {
            context.commit(
                "setWallByWallId",
                store.state.walls ? store.state.walls.filter((w) => w.id == wallId)[0] : null
            );
            await nextTick();
        },
        async setContainerByContainerId(context, containerId) {
            context.commit("setContainerByContainerId", containerId);
            await nextTick();
        },
        async lockChanges(context) {
            context.commit("setChangesLock", true);
        },
        async unlockChanges(context) {
            context.commit("setChangesLock", false);
            await nextTick();
        },
        async lockWidgets(context) {
            context.commit("setWidgetsLock", true);
            await nextTick();
        },
        async unlockWidgets(context) {
            context.commit("setWidgetsLock", false);
            await nextTick();
        },
        async openOptions(context, instance) {
            context.commit("setOptionsSource", instance);
            await nextTick();
        },
        async closeOptions(context) {
            context.commit("setOptionsSource", null);
            await nextTick();
        },
    },
});
