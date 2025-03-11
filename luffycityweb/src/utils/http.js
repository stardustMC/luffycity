import axios from 'axios'

const http = axios.create({
    timeout: 5000,
    baseURL: "http://api.luffycity.cn:8000",
    withCredentials: false
})

http.interceptors.request.use((config)=> {
    return config
}, (error)=> {
    console.log("something in request went wrong...");
    return Promise.reject(error)
})

http.interceptors.response.use((response)=> {
    return response
}, (error)=> {
    console.log("server response did not go well...");
    return Promise.reject(error)
})

export default http;