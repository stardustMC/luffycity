import {reactive} from "vue";
import http from "../utils/http.js"

const user = reactive({
    login_type: 0,
    username: "",
    password: "",
    remember: false,
    code: "",
    mobile: "",
    login(){
        return http.post("/users/login/", {
            username: this.username,
            password: this.password
        })
    }
})

export default user;