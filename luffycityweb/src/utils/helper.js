// 给小于10的数字左边补0
function format0(num){
    return num<10?"0"+num: num;
}

// 将秒数转化为XX时XX分XX秒
function format_seconds(seconds){
    let text = "";

    const hour = (seconds / 3600).toFixed();
    if(hour > 0) text += hour.toString() + "时";

    const minute = ((seconds % 3600) / 60).toFixed();
    if(minute > 0) text += minute.toString() + "分";

    const second = seconds % 60;
    text += second.toString() + "秒";
    return text;
}

export {format0, format_seconds}