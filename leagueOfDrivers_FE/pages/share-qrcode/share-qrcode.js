// pages/share-qrcode/share-qrcode.js
var api = require('../../api.js');
var app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        qrcode: ""
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
        var page = this;
        var access_token = '';
      var scene = decodeURIComponent(options.scene)
        wx.request({
          url:"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxe781c0daf36963a0&secret=1c602456f614fef60a8e74f901d4aa63",
          success: function (res) {
            console.log(res)

            access_token = res.data.access_token
            console.log(access_token)
            console.log('https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + access_token,)
            wx.request({
              url: 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + access_token,
              data: {
                scene: '000',
                page: "pages/share/share"
              },
              method: "POST",
              responseType: 'arraybuffer',  //设置响应类型
              success(res) {
                console.log(res)
                var src2 = wx.arrayBufferToBase64(res.data);  //对数据进行转换操作
                console.log(src2)
                page.setData({
                  src2
                })
              },
              fail(e) {
                console.log(e)
              },
            })
          }
        })
    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {

    },

    /**
     * 生命周期函数--监听页面显示
     */
    onShow: function () {
        var page = this;
        var user_info = wx.getStorageSync("user_info");
        this.setData({
            user_info: user_info,
        });
    },

    click: function () {
        var page = this;
        wx.previewImage({
            current: page.data.qrcode,
            urls: [page.data.qrcode]
        })
    },
    /**
     * 生命周期函数--监听页面隐藏
     */
    onHide: function () {

    },

    /**
     * 生命周期函数--监听页面卸载
     */
    onUnload: function () {

    },

    /**
     * 页面相关事件处理函数--监听用户下拉动作
     */
    onPullDownRefresh: function () {

    },

    /**
     * 页面上拉触底事件的处理函数
     */
    onReachBottom: function () {

    },
})