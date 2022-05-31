// html:页面
// css:美化
// javascript:动作行为

// js读取cookie的方法
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 保存imageID
var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}



function generateImageCode() {
    // 形成图片验证码的链接的后段地址,设置到页面中,让浏览器请求验证码图片
    // 1:生成验证码编号(两种方式:时间戳uuid全局唯一标识符)
    imageCodeId = generateUUID();
    // 设置图片url
    var url = "http://127.0.0.1:8000/user/imgcode/" + imageCodeId
    $(".image-code img").attr("src", url)
}



$(document).ready(function () {
    generateImageCode()
})
