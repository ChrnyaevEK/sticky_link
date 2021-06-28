import Vue from "vue";
import VueX from "vuex";
import store from "./store";
import io from "./io";
import router from "./router";
import env from "./env";
import {fitWidget} from "../common";

Vue.use(VueX);


export default new VueX.Store({
    strict: false,
    state: {
        targetInstanceUid: null,  // Options
    },
    mutations: {
        setTargetInstance(state, uid) {
            state.targetInstanceUid = uid;
        },
        unsetTargetInstance(state) {
            state.targetInstanceUid = null;
        },
    },
    actions: {
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
        async createWall(context, open) {
            open = open === undefined ? true : open
            await env.dispatch("lockChanges");
            let wall = await store.dispatch("createInstance", {
                type: "wall",
            });
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: `Wall ${wall.title || "Untitled"} was created!`,
                type: "success",
            });
            if (open) {
                await router.push({
                    name: "wallEdit",
                    params: {wallId: wall.id}
                });
            }
        },
        async createContainer(context, wall) {
            await env.dispatch("lockChanges");
            let index = 0;
            for (let container of store.state.containers) {
                if (container.index > index) {
                    index = container.index + 1;
                }
            }
            let container = await store.dispatch("createInstance", {
                type: "container",
                wall: wall.id,
                index,
            });
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: `Container ${container.title} was created!`,
                type: "success",
            });
        },
        async createWidget(context, {type, container,}) {  // handleCreateWidget
            await env.dispatch("lockChanges");
            let widget = await store.dispatch("createInstance", {
                type,
                container: container.id,
            });
            await store.dispatch("recalculateWidgets", container);
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: `Widget ${widget.type} ${widget.title} was created!`,
                type: "success",
            });
        },
        async updatePort(context, {port, warningTarget}) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: port,
                warningTarget,
            })
            io.save(false);

        },
        async updateWall(context, {wall, warningTarget}) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: wall,
                warningTarget,
            })
            await env.dispatch(wall.lock_widgets ? 'lockWidgets' : 'unlockWidgets');
            io.save(false);
        },
        async updateContainer(context, {container, warningTarget}) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: container,
                warningTarget,
            })
            io.save(false);

        },
        async updateWidget(context, {widget, warningTarget}) {
            io.save(true);
            await context.dispatch('$_update', {
                instance: widget,
                warningTarget,
            })
            io.save(false);
        },
        async deletePort(context, port) {
            if (confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                await store.dispatch("deleteInstance", port);
                await env.dispatch("closeOptions");
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async deleteWall(context, wall) {
            if (confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                let id = wall.id
                await store.dispatch("deleteInstance", wall);
                await env.dispatch("closeOptions");
                if (router.currentRoute.params.wallId === id) {
                    await router.push({name: "home"});
                }
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async deleteContainer(context, container) {
            if (confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                await store.dispatch("deleteInstance", container);
                await env.dispatch("closeOptions");
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async deleteWidget(context, widget) {
            if (confirm("Are you sure?")) {
                await env.dispatch("lockChanges"); // Lock changes to prevent update for deleted instance
                await store.dispatch("deleteInstance", widget);
                await env.dispatch("closeOptions");
                await env.dispatch("unlockChanges"); // Unlock changes
            }
        },
        async copyWidget(context, widget) {
            widget = {
                ...widget,
                x: widget.x + store.state.app.grid,
                y: widget.y + store.state.app.grid,
            };
            for (let container of store.state.containers) {
                if (widget.container === container.id) {
                    widget = fitWidget(widget, container);
                    break;
                }
            }
            await store.dispatch("createInstance", widget);
        },
        async $_update(context, {instance, warningTarget}) {
            try {
                await store.dispatch("updateOrAddInstance", instance);
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
        setTargetInstanceUid(context, uid) {
            context.commit('setTargetInstance', uid)
        },
        unsetTargetInstanceUid(context) {
            context.commit('unsetTargetInstance')
        },
        async deleteTargetInstance(context, instance) {
            if (instance) {
                switch (instance.type) {
                    case 'container':
                        await context.dispatch('deleteContainer', instance)
                        break;
                    default:
                        await context.dispatch('deleteWidget', instance)
                        break;
                }
            }
        },
        async updateTargetInstance(context, {instance, warningTarget}) {
            if (instance) {
                switch (instance.type) {
                    case 'container':
                        await context.dispatch('updateContainer', {
                            container: instance,
                            warningTarget
                        })
                        break;
                    default:
                        await context.dispatch('updateWidget', {
                            widget: instance,
                            warningTarget
                        })
                        break;
                }
            }
        },
        async fetchTrustedUser(context, username) {
            return await store.dispatch('fetchTrustedUser', username)
        },
        async addTrustedUser(context, {username, wall}) {
            await env.dispatch("lockChanges");
            await store.dispatch('addTrustedUser', {username, wall})
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: "User has been added!",
                type: "success",
            });
        },
        async deleteTrustedUser(context, {username, wall}) {
            await env.dispatch("lockChanges");
            await store.dispatch('deleteTrustedUser', {username, wall})
            await env.dispatch("unlockChanges");
            Vue.notify({
                text: "User has been removed!",
                type: "success",
            });
        }
    },
})
;
