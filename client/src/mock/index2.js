    // const Mock = require('mockjs'); //mockjs 导入依赖模块
    // const util = require('./util'); //自定义工具模块
    import Mock from 'mockjs';
    import util from './util.js';
    const express = require('express');

    //返回一个函数
    export default new Mock(() => {
        let app = express();

        app.use(function (req, res, next) {
            res.header("Access-Control-Allow-Origin", "*");
            res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
            res.header("Access-Control-Allow-Headers", "X-Requested-With");
            res.header('Access-Control-Allow-Headers', 'Content-Type');
            next();
        });

        let jsonData = util.getJsonFile('./userInfo.json');
        //将json传入 Mock.mock 方法中，生成的数据返回给浏览器

        app.use('api/authUser', function (rep, res) {
            //每次响应请求时读取mock data的json文件
            //util.getJsonFile方法定义了如何读取json文件并解析成数据对象
            var json = util.getJsonFile('./userInfo.json');
            //将json传入 Mock.mock 方法中，生成的数据返回给浏览器
            res.json(Mock.mock(json));
        });
        app.listen('8090', () => {
            console.log('监听端口 8090')
        })

        // Mock.mock('api/authUser', 'post', () => {
        //     return {
        //         status: 200,
        //         msg: "登录成功"
        //     }
        // })

    })

    // module.exports = function (app) {
    //     //监听http请求
    //     // app.post('api/authUser', function (rep, res) {
    //     //     //每次响应请求时读取mock data的json文件
    //     //     //util.getJsonFile方法定义了如何读取json文件并解析成数据对象
    //     //     var json = util.getJsonFile('./userInfo.json');
    //     //     //将json传入 Mock.mock 方法中，生成的数据返回给浏览器
    //     //     res.json(Mock.mock(json));
    //     // });

    // }