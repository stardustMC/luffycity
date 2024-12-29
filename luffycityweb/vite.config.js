import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from "unplugin-vue-components/resolvers";

// https://vite.dev/config/
export default defineConfig({
  plugins: [
      vue(),
      Components({
          resolvers: [ElementPlusResolver(), ]
      })
  ],
  // server:{
  //     host: 'www.luffycity.cn', port: 3000
  // }
})
