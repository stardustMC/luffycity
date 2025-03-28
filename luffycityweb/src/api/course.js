import http from "../utils/http.js"
import {reactive, ref} from "vue"

const courses = reactive({
    current_category: 0,
    current_direction: 0,
    category_list: [],
    direction_list: [],
    course_list: [],
    hotword_list: [],
    chapter_list: [],
    ordering: "-id",
    course_id: 1,
    info: {},
    page: 1,
    size: 5,
    count: 0,
    has_prev: false,
    has_next: false,
    timer: 0,
    text: "",
    // todo: request fails when current page number exceeds, this happens when query parameter changes while page not set to default 1
    get_categories(){
        return http.get(`/courses/category/${this.current_direction}/`);
    },
    get_directions(){
        return http.get("/courses/directions/");
    },
    get_courses(){
        let params = {
            page: this.page,
            size: this.size,
        };
        if(this.ordering){
            params.ordering = this.ordering;
        }
        return http.get(`/courses/${this.current_direction}/${this.current_category}/`, {
            params,
        })
    },
    get_course(){
        return http.get(`/courses/${this.course_id}/`);
    },
    get_chapter_list(){
        return http.get(`/courses/${this.course_id}/chapters/`);
    },
    start_timer(){
        clearInterval(this.timer);
        setInterval(()=>{
            this.course_list.forEach(course=>{
            if(course.discount.expire && course.discount.expire > 0){
                course.discount.expire--;
            }
        })
        }, 1000);
    },
    search_courses(){
        let params = {
            page: this.page,
            size: this.size,
            text: this.text
        };
        if(this.ordering){
            params.ordering = this.ordering;
        }
        return http.get(`/courses/search/`, {
            params,
        });
    },
    get_hot_words(){
        return http.get(`/courses/hot_words/`);
    }
})

export default courses;