/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://0.0.0.0:5000'; 