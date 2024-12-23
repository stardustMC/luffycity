import http from "../utils/http.js"
import {reactive} from "vue";


const banner = reactive({
    banner_list: [],
    get_banner_list(){
        return http.get("/home/banner/");
    },
});

export default banner;