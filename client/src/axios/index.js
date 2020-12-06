import axios from "axios";

const service = axios.create({
    // baseURL: baseURL,
    // timeout: 3000
    headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        // "x-csrftoken": window.cookies['csrftoken']
    },
    withCredentials: true
})
export default service;