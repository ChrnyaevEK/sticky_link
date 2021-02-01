function generateId(property){
    return `${property}-${this.id}`
}

export function registerIdSystem(vm){
    vm._= function(property){
        return generateId.call(vm, property)
    }
}

export default {
    registerIdSystem
}