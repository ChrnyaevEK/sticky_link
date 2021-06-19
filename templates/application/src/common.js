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
    document.execCommand("copy");
    input.parentNode.removeChild(input);
}

export function timeFormatted(utc) {
    var x = new Date(utc);
    var y = "dd.MM.yyyy hh:mm";
    var z = {
        M: x.getMonth() + 1,
        d: x.getDate(),
        h: x.getHours(),
        m: x.getMinutes(),
        s: x.getSeconds(),
    };
    z;
    x = new Date(Date.UTC(x.getFullYear(), x.getMonth(), x.getDate(), x.getHours(), x.getMinutes(), x.getSeconds()));
    y = y.replace(/(M+|d+|h+|m+|s+)/g, function(v) {
        return ((v.length > 1 ? "0" : "") + eval("z." + v.slice(-1))).slice(-2);
    });

    return y.replace(/(y+)/g, function(v) {
        return x
            .getFullYear()
            .toString()
            .slice(-v.length);
    });
}

export const types = {
    Wall: "wall",
    Container: "container",
    SimpleText: "simple_text",
    URL: "url",
    Counter: "counter",
    SimpleList: "simple_list",
    SimpleSwitch: "simple_switch",
    Port: "port",
    Document: "document",
};

export function downloadImage(data, filename = "download.jpeg") {
    var a = document.createElement("a");
    a.href = data;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

export default {
    types,
    difference,
    sleep,
    timeFormatted,
    downloadImage,
};
