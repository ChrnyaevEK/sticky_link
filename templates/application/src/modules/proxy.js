import Vue from "vue";
import VueX from "vuex";
import store from "./store";
import io from "./io";
import router from "./router";

Vue.use(VueX);

async function nextTick() {
    await new Promise((resolve) => {
        Vue.nextTick(resolve);
    });
}

export default new VueX.Store({
    strict: false,
    state: {
        port: null,
        wall: null,
        container: null,
        widget: null,
    },
    mutations: {
        setWallById(state, id) {
            state.wall = store.state.walls ? store.state.walls.filter((w) => w.id === id)[0] : null;
        },
        setContainerById(state, id) {
            state.container = store.state.containers ? store.state.containers.filter((c) => c.id === id)[0] : null;
        },
        setPortById(state, id) {
            state.port = store.state.ports ? store.state.ports.filter((p) => p.id === id)[0] : null;
        },
        setWidgetById(state, id) {
            state.widget = store.state.widgets ? store.state.widgets.filter((w) => w.id === id)[0] : null;
        },
    },
    actions: {
        async setWallById(context, id) {
            context.commit("setWallById", id);
            await nextTick();
        },
        async setPortById(context, id) {
            context.commit("setPortById", id);
            await nextTick();
        },
        async setContainerById(context, id) {
            context.commit("setContainerById", id);
            await nextTick();
        },
        async setWidgetById(context, id) {
            context.commit("setWidgetById", id);
            await nextTick();
        },
        async createPort() {
            let port = await store.dispatch("createInstance", {
                type: "port",
            });
            Vue.notify({
                text: `Port ${port.title} was created!`,
                type: "success",
            });
        },
        async createWall() {
            let wall = await store.dispatch("createInstance", {
                type: "wall",
            });
            Vue.notify({
                text: `Wall ${wall.title || "Untitled"} was created!`,
                type: "success",
            });
            await router.push({
                name: "wallEdit",
                params: {wallId: wall.id}
            });
        },
        async createContainer(context) {
            let index = 0;
            for (let container of store.state.containers) {
                if (container.index > index) {
                    index = container.index + 1;
                }
            }
            let container = await store.dispatch("createInstance", {
                type: "container",
                wall: context.state.wall.id,
                index,
            });
            Vue.notify({
                text: `Container ${container.title} was created!`,
                type: "success",
            });
        },
        async createWidget(context, type) {  // handleCreateWidget
            let widget = await store.dispatch("createInstance", {
                type,
                container: context.state.container.id,
            });
            await store.dispatch("recalculateWidgets", context.state.container);
            Vue.notify({
                text: `Widget ${widget.type} ${widget.title} was created!`,
                type: "success",
            });
        },
        async updatePort(context, warningTarget) {
            return await context.dispatch('$_update', {
                instance: context.state.port,
                warningTarget,
            })
        },
        async updateWall(context, warningTarget) {
            return await context.dispatch('$_update', {
                instance: context.state.wall,
                warningTarget,
            })
        },
        async updateContainer(context, warningTarget) {
            return await context.dispatch('$_update', {
                instance: context.state.container,
                warningTarget,
            })
        },
        async updateWidget(context, warningTarget) {
            return await context.dispatch('$_update', {
                instance: context.state.widget,
                warningTarget,
            })
        },
        deleteWall(context) {
            router.push({name: context.state.editMode ? "wallEdit" : "wallView"});
        },
        async $_update(context, {instance, warningTarget}) {
            try {
                await this.$store.dispatch("updateOrAddInstance", instance);
            } catch (e) {
                return io.setWarning(e, warningTarget);
            }
            io.unsetWarning(warningTarget);
        },
    },
});
