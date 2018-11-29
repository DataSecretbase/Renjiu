const app = getApp()

Page({
  data: {
    balance: 0,
    freeze: 0,
    score: 0,
    score_sign_continuous: 0
  },
  onLoad() {

  },
  onShow() {
    let that = this;
    let userInfo = wx.getStorageSync('userInfo')
    if (!userInfo) {
      wx.navigateTo({
        url: "/pages/tologin/index"
      })
    } else {
      that.setData({
        userInfo: userInfo,
        version: app.globalData.version
      })
    }
  },
  getUserInfo: function (cb) {
    var that = this
    wx.login({
      success: function () {
        wx.getUserInfo({
          success: function (res) {
            that.setData({
              userInfo: res.userInfo
            });
          }
        })
      }
    })
  },
  getProductList(e) {
    var _id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: "/pages/product_list/index?id=" + _id
    })
  },
  allOrder(e) {
    var _id = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: "/pages/order-list/index?id=" + _id
    })
  },
  aboutUs: function () {
    wx.showModal({
      title: '关于我们',
      content: '本系统基于开源小程序商城系统 https://github.com/developertqw2017/Renjiu.git 搭建，祝大家使用愉快！',
      showCancel: false
    })
  },
  relogin: function () {
    var that = this;
    app.globalData.token = null;
    app.login();
    wx.showModal({
      title: '提示',
      content: '重新登陆成功',
      showCancel: false,
      success: function (res) {
        if (res.confirm) {
          that.onShow();
        }
      }
    })
  },
  recharge: function () {
    wx.navigateTo({
      url: "/pages/recharge/index"
    })
  },
  withdraw: function () {
    wx.navigateTo({
      url: "/pages/withdraw/index"
    })
  }
})