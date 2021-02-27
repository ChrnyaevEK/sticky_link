import { Context, UpdateManager } from "../../common.js";
Context.$on("addBlankWidget", function(klass) {
    Context.$emit("lockWidgetCreation");
    Context.$emit("routeRequest", ($route) => {
        new UpdateManager(klass.type)
            .create({ wall: $route.params.wallId })
            .then((response) => {
                Context.$emit("widgetCreated", response);
            })
            .always(() => {
                Context.$emit("unlockWidgetCreation");
            });
    });
});