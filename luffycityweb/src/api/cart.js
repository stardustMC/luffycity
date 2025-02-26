import http from "../utils/http.js"
import {reactive} from "vue";

const cart = reactive({
    add_course_to_cart(course_id, token){
        return http.post("/cart/", {
            course_id: course_id
        }, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    }
})

export default cart;