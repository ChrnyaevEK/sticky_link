import Vue from "vue";
import VueX from "vuex";
import store from "./store";
import io from "./io";
import router from "./router";
import env from "./env";
import {fitWidget} from "../common";

Vue.use(VueX);


async function withChangesLock(func) {
    await env.dispatch("lockChanges");
    try {
        var res = await func()
    } catch (e) {
        await env.dispatch("unlockChanges");
        throw e
    }
    await env.dispatch("unlockChanges");
    return res
}

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
            try {
                await withChangesLock(async () => {
                    return await store.dispatch("createInstance", {
                        type: "port",
                    })
                });
            } catch (e) {
                return
            }
            Vue.notify({
                text: 'Port was created!',
                type: "success",
            });
        },
        async createWall(context, open) {
            open = open === undefined ? true : open
            try {
                var wall = await withChangesLock(async () => {
                    return await store.dispatch("createInstance", {
                        type: "wall",
                    });
                })
            } catch (e) {
                return
            }
            Vue.notify({
                text: `Wall was created!`,
                type: "success",
            });
            if (open) {
                await router.push({
                    name: "wallEdit",
                    params: {wallId: wall.id}
                });
            }
        },
        async createContainer(context, {wall, next_container}) {
            try {
                await withChangesLock(async () => {
                    return await store.dispatch("createInstance", {
                        type: "container",
                        wall: wall.id,
                        next: next_container.id,
                    });
                })
            } catch (e) {
                return
            }
            Vue.notify({
                text: 'Container was created!',
                type: "success",
            });
        },
        async createWidget(context, {type, container,}) {  // handleCreateWidget
            try {
                await withChangesLock(async () => {
                    return await store.dispatch("createInstance", {
                        type,
                        container: container.id,
                    });
                })
            } catch (e) {
                return
            }
            await store.dispatch("recalculateWidgets", container);
            Vue.notify({
                text: 'Widget was created!',
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
                try {
                    await withChangesLock(async () => {
                        await store.dispatch("deleteInstance", port);
                    })
                } catch (e) {
                    return
                }
                Vue.notify({
                    text: 'Port was deleted!',
                    type: "success",
                });
            }
        },
        async deleteWall(context, wall) {
            if (confirm("Are you sure?")) {
                let id = wall.id
                try {
                    await withChangesLock(async () => {
                        await store.dispatch("deleteInstance", wall);
                    })
                } catch (e) {
                    return
                }
                Vue.notify({
                    text: 'Wall was deleted!',
                    type: "success",
                });
                if (router.currentRoute.params.wallId === id) {
                    await router.push({name: "home"});
                }
            }
        },
        async deleteContainer(context, container) {
            if (confirm("Are you sure?")) {
                try {
                    await withChangesLock(async () => {
                        await store.dispatch("deleteInstance", container);
                    })
                } catch (e) {
                    return
                }
                Vue.notify({
                    text: 'Container was deleted!',
                    type: "success",
                });
                await env.dispatch("closeOptions");
            }
        },
        async deleteWidget(context, widget) {
            if (confirm("Are you sure?")) {
                try {
                    await withChangesLock(async () => {
                        await store.dispatch("deleteInstance", widget);
                    })
                } catch (e) {
                    return
                }
                Vue.notify({
                    text: 'Widget was deleted!',
                    type: "success",
                });
                await env.dispatch("closeOptions");
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
            try {
                await withChangesLock(async () => {
                    await store.dispatch("createInstance", widget);
                })
            } catch (e) {
                return
            }
        },
        async copyWall(context, wall) {
            if (confirm("Are you sure?")) {
                try {
                    await withChangesLock(async () => {
                        await store.dispatch("copyWall", wall);
                    })
                } catch (e) {
                    return
                }
            }
        },
        async copyContainer(context, container) {
            if (confirm("Are you sure?")) {
                try {
                    await withChangesLock(async () => {
                        await store.dispatch("copyContainer", container);
                    })
                } catch (e) {
                    return
                }
            }
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
            try {
                await withChangesLock(async () => {
                    await store.dispatch('addTrustedUser', {username, wall})
                })
            } catch (e) {
                return
            }
            Vue.notify({
                text: "User has been added!",
                type: "success",
            });
        },
        async deleteTrustedUser(context, {username, wall}) {
            try {
                await withChangesLock(async () => {
                    await store.dispatch('deleteTrustedUser', {username, wall})
                })
            } catch (e) {
                return
            }
            Vue.notify({
                text: "User has been removed!",
                type: "success",
            });
        },
        async activatePort(context, portId) {
            try {
                await withChangesLock(async () => {
                    await store.dispatch('activatePort', portId)
                })
            } catch (e) {
                return
            }
            Vue.notify({
                text: "Port has been activated!",
                type: "success",
            });
            await router.push({name: "portSettings", params: {portId}});
        },
    },
})
;
