const CompressionPlugin = require('compression-webpack-plugin')

module.exports = {
  transpileDependencies: ["vuetify"],

  devServer: {
    open: (function () {
      process.platform === "win32";
      process.arch === "x64";
    })(),
    // open: process.arch === "x64",
    // host: '127.0.0.1',
    hot: true,
    http2:false,
    port: 8080,
    https: false,

    // mock接口设置
    // before: require("./src/mock"),
    
    // 设置代理，
    proxy: {
      "/api": {
        // 目标 API 地址
        // target: "https://11f3944d-a24c-4d9e-a922-b061437033c2.mock.pstmn.io/", // 接口的域名
        // target: "http://rap2api.taobao.org/app/mock/271997/",
        target: "http://127.0.0.1:5000",
        // target: "https://yapi.baidu.com/mock/17108/",
        // port:38080,
        // 将主机标头的原点更改为目标URL
        changeOrigin: true,
        // ws:true,
        pathRewrite: {
          "^/api": ""
        },
      },
      // "/": {
      //   target: "http://localhost:5000", // 接口的域名
      //   // 将主机标头的原点更改为目标URL
      //   changeOrigin: true,
      //   pathRewrite: {
      //     "^/": "/"
      //   }
      // }
    }
  },

  css: {
    extract: false
  },

  chainWebpack: config => {
    // config.entry('main').add('@vue/cli-plugin-babel/preset')

    config
      .plugin('html')
      .tap(args => {
        args[0].title = '召集令系统'
        return args
      })
  },

  configureWebpack: config => {
    // babel-polyfill 设置浏览器兼容性，兼容ie11~9
    // config.entry.app = ["@vue/babel-preset-app", "./src/main.js"];
    // 生产环境使用gzip
    if (process.env.NODE_ENV === 'production') {
      return {
        plugins: [
          new CompressionPlugin({
            algorithm: 'gzip',
            test: /\.(js|css|html|jpg|png|jpeg)$/, // 匹配文件名
            threshold: 10240, // 对超过10k的数据压缩
            deleteOriginalAssets: false, // 不删除源文件
            minRatio: 0.8 // 压缩比
          })
        ]
      }
    }
  },

  assetsDir: 'static',
  productionSourceMap: false,
  lintOnSave: false
}