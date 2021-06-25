import Vue from "vue";
import VueX from "vuex";
import store from "./store";
import io from "./io";
import router from "./router";
import env from "./env";

Vue.use(VueX);

async function nextTick() {
    await new Promise((resolve) => {
        Vue.nextTick(resolve);
    });
}

function getById(source, id) {
    return source ? source.filter((i) => i.id === id)[0] : null;
}

export default new VueX.Store({
    strict: false,
    state: {
        port: null,
        wall: null,
        container: null,
        widget: null,
        targetInstance: null,  // Options
    },
    mutations: {
        setWallById(state, id) {
            state.wall = getById(store.state.walls, id);
        },
        setContainerById(state, id) {
            state.container = getById(store.state.containers, id);
        },
        setPortById(state, id) {
            state.port = getById(store.state.ports, id);
        },
        setWidgetById(state, id) {
            state.widget = getById(store.state.widgets, id);
        },
        setTargetInstance(state, instance) {
            state.targetInstance = instance;
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
            await env.dispatch("lockChanges");
            let port = await store.dispatch("createInstance", {
                type: "port",
            });
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: `Port ${port.title} was created!`,
                type: "success",
            });
        },
        async createWall() {
            await env.dispatch("lockChanges");
            let wall = await store.dispatch("createInstance", {
                type: "wall",
            });
            await env.dispatch("unlockChanges");
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
            await env.dispatch("lockChanges");
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
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: `Container ${container.title} was created!`,
                type: "success",
            });
        },
        async createWidget(context, type) {  // handleCreateWidget
            await env.dispatch("lockChanges");
            let widget = await store.dispatch("createInstance", {
                type,
                container: context.state.container.id,
            });
            await store.dispatch("recalculateWidgets", context.state.container);
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: `Widget ${widget.type} ${widget.title} was created!`,
                type: "success",
            });
        },
        async updatePort(context, warningTarget) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: context.state.port,
                warningTarget,
            })
            io.save(false);

        },
        async updateWall(context, warningTarget) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: context.state.wall,
                warningTarget,
            })
            io.save(false);
        },
        async updateContainer(context, warningTarget) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: context.state.container,
                warningTarget,
            })
            io.save(false);

        },
        async updateWidget(context, warningTarget) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: context.state.widget,
                warningTarget,
            })
            io.save(false);
        },
        async deletePort(context) {
            if (context.state.port && confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                await this.$store.dispatch("deleteInstance", context.state.port);
                await env.dispatch("closeOptions");
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async deleteWall(context) {
            if (context.state.wall && confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                let id = context.state.wall.id
                await this.$store.dispatch("deleteInstance", context.state.wall);
                await env.dispatch("closeOptions");
                if (router.currentRoute.params.wallId === id) {
                    await router.push({name: "home"});
                }
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async deleteContainer(context) {
            if (context.state.container && confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                await this.$store.dispatch("deleteInstance", context.state.container);
                await env.dispatch("closeOptions");
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async deleteWidget(context) {
            if (context.state.widget && confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                await this.$store.dispatch("deleteInstance", context.state.widget);
                await env.dispatch("closeOptions");
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async $_update(context, {instance, warningTarget}) {
            try {
                await this.$store.dispatch("updateOrAddInstance", instance);
            } catch (e) {
                return io.setWarning(e, warningTarget);
            }
            io.unsetWarning(warningTarget);
        },
        async uploadSource(context, {data, name, instance}) {
            io.save(true);
            data = await store.dispatch('uploadSource', {data, name, instance});
            io.save(false);
            Vue.notify({
                text: "Uploaded!",
                type: "success",
            });
            return data;
        },
        async removeSource(context, instance) {
            io.save(true);
            await store.dispatch('removeSource', instance);
            Vue.notify({
                text: "Success!",
                type: "success",
            });
            io.save(false);
        },
        setTargetInstance(context, instance) {
            context.commit('setTargetInstance', instance)
        },
        async deleteTargetInstance(context) {
            if (context.state.targetInstance) {
                switch (context.state.targetInstance) {
                    case context.state.wall:
                        await context.dispatch('deleteWall')
                        break;
                    case context.state.port:
                        await context.dispatch('deletePort')
                        break;
                    case context.state.container:
                        await context.dispatch('deleteContainer')
                        break;
                    case context.state.widget:
                        await context.dispatch('deleteWidget')
                        break;
                }
            }
        },
        async updateTargetInstance(context, warningTarget) {
            if (context.state.targetInstance) {
                switch (context.state.targetInstance) {
                    case context.state.wall:
                        await context.dispatch('updateWall', warningTarget)
                        break;
                    case context.state.port:
                        await context.dispatch('updatePort', warningTarget)
                        break;
                    case context.state.container:
                        await context.dispatch('updateContainer', warningTarget)
                        break;
                    case context.state.widget:
                        await context.dispatch('updateWidget', warningTarget)
                        break;
                }
            }
        }
    },
})
;
