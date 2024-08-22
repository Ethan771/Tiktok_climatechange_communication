window = global;
delete global;
delete Buffer;
window.requestAnimationFrame = function () {

}

XMLHttpRequest = function () {
}
onwheelx = {
    "_Ax": "0X21"
}
navigator = {}
screen = {
    availHeight: 824,
    availWidth: 1536,
    height: 864,
    width: 1536,
    colorDepth: 24,
    pixelDepth: 24,
    orientation: {
        angle: 0,
        type: "landscape-primary",
        onchange: null
    }
}
document = {}

function setProxy(proxyObjs) {
    for (let i = 0; i < proxyObjs.length; i++) {
        const handler = `{
      get: function(target, property, receiver) {
            console.log("方法:", "get  ", "对象:", "${proxyObjs[i]}", "  属性:", property, "  属性类型：", typeof property, ", 属性值：", target[property], ", 属性值类型：", typeof target[property]);
            return target[property];
      },
      set: function(target, property, value, receiver) {
        console.log("方法:", "set  ", "对象:", "${proxyObjs[i]}", "  属性:", property, "  属性类型：", typeof property, ", 属性值：", value, ", 属性值类型：", typeof target[property]);
        return Reflect.set(...arguments);
      }
    }`;
        eval(`try {
            ${proxyObjs[i]};
            ${proxyObjs[i]} = new Proxy(${proxyObjs[i]}, ${handler});
        } catch (e) {
            ${proxyObjs[i]} = {};
            ${proxyObjs[i]} = new Proxy(${proxyObjs[i]}, ${handler});
        }`);
    }
}

