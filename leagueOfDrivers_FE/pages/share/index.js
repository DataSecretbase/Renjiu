// pages/share/index.js
var api = require("../../api.js");
var app = getApp();
Page({

    /**
     * 页面的初始数据
     */
    data: {
        total_price: 0,
        price: 0,
        cash_price: 0,
        total_cash: 0,
        team_count: 0,
        order_money: 0
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function (options) {
      var page = this;
      var page = this;
      var userInfo = wx.getStorageSync("userInfo");
      var isshareuser;
      console.log(api.share)
      app.request({
        url: api.share.isshareuser,
        success: function (res) {
          console.log(res)
          if (res.code != 0) {
            wx.showModal({
              title: "您还不是分销商！",
              content: '请先前往“个人中心->成为分销商”处进行申请成为分销商',
              showCancel: false,
              success: function (res) {
                if (res.confirm) {
                  wx.redirectTo({
                    url: '/pages/my/index',
                  })
                }
              }
            });
          }
        },
        complete: function () {
          wx.hideLoading();
        }
      });
        page.setData({
          userInfo: userInfo,
        });
        wx.showLoading({
          title: "正在加载",
          mask: true,
        });
        app.request({
          url: api.share.get_info,
          success: function (res) {
            console.log("res")

              console.log(res)
              page.setData({
                userprofile: res[0].user,
                total_price: res[0].total_price,
                price: res[0].price,
                cash_price: res[0].cash_price,
                total_cash: res[0].total_cash,
                team_count: res[0].team_count,
                order_money: res[0].order_money
              });
            wx.setStorageSync("ShareUserProfile", res);
          },
          complete: function () {
            wx.hideLoading();
          }
        });
      wx.hideLoading();

      
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

})