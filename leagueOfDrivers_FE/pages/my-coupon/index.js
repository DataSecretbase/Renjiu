//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    coupons:[]
  },
  onLoad: function () {
    getMyCoupons();
  },
  onShow : function () {
    this.getMyCoupons();
  },
  getMyCoupons: function () {
    var that = this;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/coupons/my',
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      method: "POST",
      data: {
        token: wx.getStorageSync('token'),
        status: 0
      },
      success: function (res) {
        console.log(res)
        if (res.data.code == 0) {
          var coupons = res.data.data;
          if (coupons.length > 0) {
            that.setData({
              coupons: coupons
            });
          }
        }
      }
    })
  },
  goBuy:function(){
    wx.reLaunch({
      url: '/pages/index/index'
    })
  }

})
