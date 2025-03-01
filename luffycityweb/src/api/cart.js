import http from "../utils/http.js"
import {reactive, computed} from "vue";

const cart = reactive({
    cart_list: [],
    cart_selected_list: [],
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
    get_cart_selected_list(token){
        return http.get("/cart/order/", {
            headers: {
                Authorization: "jwt " + token
            }
        });
    },
    course_select_change(course_id, selected, token){
        return http.patch("/cart/", {
            course_id: course_id,
            selected: selected
        }, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    course_select_all_change(selected, token){
        return http.put("/cart/", {
            selected: selected
        }, {
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    cart_delete(course_id, token){
        return http.delete("/cart/", {
            params:{
                course_id,  // course_id: course_id,的简写
            },
            headers: {
                Authorization: "jwt " + token
            }
        })
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
    }),
    total_selected_discount_price: computed(()=>{
        let total = 0;
        cart.cart_selected_list.forEach(course=>{
            if(course.discount.price >= 0){
                total += course.discount.price
            }else{
                total += course.price;
            }
        })
        return total;
    }),
    total_selected_price: computed(()=>{
        let total = 0;
        cart.cart_selected_list.forEach(course=>{
            total += course.price;
        })
        return total;
    })
})

export default cart;