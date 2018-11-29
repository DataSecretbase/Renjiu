// pages/authorize/index.js
var app = getApp();
Page({
  /**
  * 页面的初始数据
  */
  data: {

  },
  /**
  * 生命周期函数--监听页面加载
  */
  onLoad: function (options) {

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
  /**
  * 用户点击右上角分享
  */
  onShareAppMessage: function () {

  },
  GetUserInfo: function (e) {
    if (!e.detail.userInfo) {
      return;
    }
    wx.setStorageSync('userInfo', e.detail.userInfo)
    this.login();
  },
  login: function () {  
    var that = this;
    var token = wx.getStorageSync('token');
    if (!token) {
    wx.login({
      success: function (res) {
        console.log(res.code)
        var code = res.code
        wx.getUserInfo({
          success: function (r) {
            console.log(r.encryptedData)
            wx.request({
              //url:that.globalData.baseUrl +'/user/wxapp/login',
              url: 'https://qgdxsw.com:8000/league/api/v1/auth/login/',
              header: { "Content-Type": "application/x-www-form-urlencoded" },
              method: 'POST',
              data: {
                code: code,
                iv: r.iv,
                encrypteddata: r.encryptedData
              },

              success: function (res) {

                console.log(res)
                if (!res.data.account) {
                  // 登录错误
                  wx.hideLoading();
                  wx.showModal({
                    title: '提示',
                    content: '无法登录，请重试',
                    showCancel: false
                  })
                  return;
                }else{
                  wx.setStorageSync('token', res.data.token)
                  wx.setStorageSync('account', res.data.account)
                  wx.setStorageSync('uid', res.data.username)                  
                  wx.showModal({
                    title: '提示',
                    content: '登录成功，请返回',
                    showCancel: false
                  })
                }
                console.log(res.data.token)
              }
            })
          }
        })
      }
      
    })
    }
  },
  sendTempleMsg: function (orderId, trigger, template_id, form_id, page, postJsonString) {
    var that = this;
    wx.request({
      url: that.globalData.baseUrl + '/template-msg/put',
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      data: {
        token: wx.getStorageSync('token'),
        type: 0,
        module: 'order',
        business_id: orderId,
        trigger: trigger,
        template_id: template_id,
        form_id: form_id,
        url: page,
        postJsonString: postJsonString
      },
      success: (res) => {
        //console.log('*********************');
        //console.log(res.data);
        //console.log('*********************');
      }
    })
  },
  registerUser: function () {
    var that = this;
    wx.login({
      success: function (res) {
        var code = res.code; // 微信登录接口返回的 code 参数，下面注册接口需要用到
        wx.getUserInfo({
          success: function (res) {
            var iv = res.iv;
            var encryptedData = res.encryptedData;
            // 下面开始调用注册接口
            wx.request({
              url: 'https://api.it120.cc/' + app.globalData.subDomain + '/user/wxapp/register/complex',
              data: { code: code, encryptedData: encryptedData, iv: iv }, // 设置请求的 参数
              success: (res) => {
                wx.hideLoading();
                that.login();
              }
            })
          }
        })
      }
    })
  }
}) 