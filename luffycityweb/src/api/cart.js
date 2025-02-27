import http from "../utils/http.js"
import {reactive, computed} from "vue";

const cart = reactive({
    cart_list: [],
    add_course_to_cart(course_id, token){
        return http.post("/cart/", {
            course_id: course_id
        }, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    get_cart_list(token){
        return http.get("/cart/", {
            headers: {
                Authorization: "jwt " + token
            }
        });
    },
    total_price: computed(()=>{
        let total = 0;
        cart.cart_list.forEach(course=>{
            if(course.selected){
                if(course.discount.price >= 0){
                    total += course.discount.price;
                }else{
                    total += course.price;
                }
            }
        })
        return total;
    })
})

export default cart;