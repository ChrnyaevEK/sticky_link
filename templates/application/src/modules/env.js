import Vue from "vue";
import VueX from "vuex";

Vue.use(VueX);

// async function nextTick() {
//     await new Promise((resolve) => {
//         Vue.nextTick(resolve);
//     });
// }

export default new VueX.Store({
    state: {
        changesLock: false,
        widgetsLock: false,
        editMode: false,
        viewMode: false,
    },
    mutations: {
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
    },
    actions: {
        setEditMode(context) {
            context.commit("setEditMode");
        },
        setViewMode(context) {
            context.commit("setViewMode");
        },
        lockChanges(context) {
            context.commit("setChangesLock", true);
        },
        unlockChanges(context) {
            context.commit("setChangesLock", false);
        },
        lockWidgets(context) {
            context.commit("setWidgetsLock", true);
        },
        unlockWidgets(context) {
            context.commit("setWidgetsLock", false);
        },
        openOptions(context, instance) {
            context.commit("setTargetInstance", instance);
        },
        closeOptions(context) {
            context.commit("setTargetInstance", null);
        },
    },
});
