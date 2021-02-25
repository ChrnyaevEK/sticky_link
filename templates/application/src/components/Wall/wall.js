function validateWall(id) {
    return Context.walls.some((w) => {
        return String(w.id) == id;
    });
}

function deleteWall(id) {
    for (var i = 0; i < Context.walls.length; i++) {
        if (Context.walls[i].id == id) {
            Context.walls.splice(i, 1);
            break;
        }
    }
}

function updateWall(id, obj) {
    for (var wall of Context.walls) {
        if (wall.id == id) {
            Object.assign(wall, obj);
        }
    }
}

export default {
    validateWall,
    deleteWall,
    updateWall,
};
