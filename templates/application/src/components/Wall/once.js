import { Context, UpdateManager } from "../../common.js";
Context.$on("addBlankWall", () => {
    new UpdateManager("wall").create().then((response) => {
        Context.walls.push(response);
        Context.$emit("wallCreated", response);
    });
});
