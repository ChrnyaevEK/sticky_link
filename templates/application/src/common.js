import Vue from "vue";

const transform = require("lodash.transform");
const isEqual = require("lodash.isequal");
const isArray = require("lodash.isarray");
const isObject = require("lodash.isobject");

export function difference(origObj, newObj) {
    function changes(newObj, origObj) {
        return transform(newObj, function (result, value, key) {
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
    let x = new Date(utc);
    let y = "dd.MM.yyyy hh:mm";
    let z = {
        M: x.getMonth() + 1,
        d: x.getDate(),
        h: x.getHours(),
        m: x.getMinutes(),
        s: x.getSeconds(),
    };
    z;
    x = new Date(Date.UTC(x.getFullYear(), x.getMonth(), x.getDate(), x.getHours(), x.getMinutes(), x.getSeconds()));
    y = y.replace(/(M+|d+|h+|m+|s+)/g, function (v) {
        return ((v.length > 1 ? "0" : "") + eval("z." + v.slice(-1))).slice(-2);
    });

    return y.replace(/(y+)/g, function (v) {
        return x
            .getFullYear()
            .toString()
            .slice(-v.length);
    });
}

export function fitWidget(widget, container) {
    if (widget.x + widget.w >= container.w) {
        let x = container.w - widget.w;
        widget.x = x < 0 ? 0 : x;
    }
    if (widget.y + widget.h >= container.h) {
        let y = container.h - widget.h;
        widget.y = y < 0 ? 0 : y;
    }
    if (widget.h >= container.h) {
        widget.h = container.h;
    }
    return widget;
}

export function getById(source, id) {
    return source ? getReactiveCopy(source.filter((i) => i.id === id)[0]) : null;
}

export function getByUid(source, uid) {
    return source ? getReactiveCopy(source.filter((i) => i.uid === uid)[0]) : null;
}

export function getReactiveCopy(obj) {
    if (obj === undefined) return undefined
    return Vue.observable(Object.assign(deepCopy(obj)))
}

export function downloadImage(data, filename = "download.jpeg") {
    var a = document.createElement("a");
    a.href = data;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

export default {
    difference,
    sleep,
    getByUid,
    getReactiveCopy,
    getById,
    fitWidget,
    timeFormatted,
    downloadImage,
};
