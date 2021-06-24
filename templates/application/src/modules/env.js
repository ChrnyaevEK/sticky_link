import Vue from "vue";
import VueX from "vuex";

Vue.use(VueX);

async function nextTick() {
    await new Promise((resolve) => {
        Vue.nextTick(resolve);
    });
}

export default new VueX.Store({
    state: {
        changesLock: false,
        widgetsLock: false,
        editMode: false,
        viewMode: false,
        optionsSource: null,
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
        setOptionsSource(state, source) {
            state.optionsSource = source;
        },
    },
    actions: {
        async setEditMode(context) {
            context.commit("setEditMode");
            await nextTick();
        },
        async setViewMode(context) {
            context.commit("setViewMode");
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
