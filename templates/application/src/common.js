const transform = require("lodash.transform");
const isEqual = require("lodash.isequal");
const isArray = require("lodash.isarray");
const isObject = require("lodash.isobject");

export function difference(origObj, newObj) {
    function changes(newObj, origObj) {
        return transform(newObj, function(result, value, key) {
            if (!isEqual(value, origObj[key])) {
                result[key] =
                    !isArray(value) && isObject(value) && isObject(origObj[key]) ? changes(value, origObj[key]) : value;
            }
        });
    }
    return changes(newObj, origObj);
}

export async function sleep(milliseconds) {
    return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

export function deepCopy(data) {
    return JSON.parse(JSON.stringify(data));
}

export function copyToClipboard(text) {
    let input = document.body.appendChild(document.createElement("input"));
    input.value = text;
    input.focus();
    input.select();
    document.execCommand('copy');
    input.parentNode.removeChild(input);
  }

export const types = {
    Wall: "wall",
    Container: "container",
    SimpleText: "simple_text",
    URL: "url",
    Counter: "counter",
    SimpleList: "simple_list",
    SimpleSwitch: "simple_switch",
    Port: 'port',
};

export default {
    types,
    difference,
    sleep,
};
