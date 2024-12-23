import http from "../utils/http.js"
import {reactive} from "vue";


const nav = reactive({
    nav_header_list: [],
    nav_footer_list: [],
    get_nav_header_list(){
        return http.get("/home/nav/header/");
    },
    get_nav_footer_list(){
        return http.get("/home/nav/footer/")
    }
});

export default nav;