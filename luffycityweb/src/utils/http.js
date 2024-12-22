import axios from 'axios'

const http = axios.create({
    baseURL: "http://api.luffycity.cn:8000",
    withCredentials: false
})

http.interceptors.request.use((config)=> {
    console.log("before request sent");
    return config
}, (error)=> {
    console.log("something in request went wrong...");
    return Promise.reject(error)
})

http.interceptors.response.use((response)=> {
    console.log("response is about to return");
    return response
}, (error)=> {
    console.log("server response did not go well...");
    return Promise.reject(error)
})

export default http;