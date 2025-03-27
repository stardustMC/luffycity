import {reactive} from "vue";
import http from "../utils/http.js"

const user = reactive({
    login_type: 0,
    username: "",
    password: "",
    remember: false,
    code: "",
    mobile: "",
    alipay_account:  "darbfc7920@sandbox.com",
    page: 1,
    size: 5,
    courses: [],
    course_count: 0,
    current_course_type: -1,
    course_types: [],
    course_duration(course_id){
        let seconds = 0;
        for(const course of this.courses){
            if(course.id === course_id){
                course.info.lesson_list.forEach(lesson => {
                    let dur = lesson.duration.split(":");
                    seconds += parseInt(dur[0]) * 60 + parseInt(dur[1]);
                });
                return seconds;
            }
        }
    },
    login(){
        return http.post("/users/login/", {
            username: this.username,
            password: this.password
        })
    },
    get_course_list(token){
        let params = {
            course_type: this.current_course_type,
            page: this.page,
            size: this.size,
        }
        return http.get("/users/course/", {
            params,
            headers: {
                Authorization: "jwt " + token
            }
        })
    },
    get_course_type(){
        return http.get("/courses/types/");
    }
})

export default user;