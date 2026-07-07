import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

// criando uma url base

const api = axios.create({
    baseURL:import.meta.env.VITE_API_URL
})

// interceptador para sempre verificar durante a requisiçao se o usuário tem o token validado
api.interceptors.request.use(
    (config) =>{
        const token = localStorage.getItem(ACCESS_TOKEN);
        if(token){
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error)=>{
        return Promise.reject(error)
    }
)


export default api