// 给小于10的数字左边补0
export function format0(num){
    return num<10?"0"+num: num;
}