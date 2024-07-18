import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    //  代理配置
    proxy: {
      //  代理所有以  /api  开头的请求
      "/api": {
        target: "http://localhost:6666", //  后端服务实际地址
        changeOrigin: true, //  是否改变域名
        rewrite: (path) => path.replace(/^\/api/, ""), //  重写请求路径，去掉路径中的  /api
      },
    },
  },
});
