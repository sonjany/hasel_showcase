import axios from "axios";


const BASE = (import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000").replace(/\/$/, "");

export const api = axios.create({
  baseURL: BASE, //"http://127.0.0.1:8000/api",
  headers: { "Content-Type": "application/json" },
});