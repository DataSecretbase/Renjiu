// pages/share-money/share-money.js
var api = require('../../api.js');
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    block:false,
    active:'',
    total_price:0,
    price:0,
    cash_price:0,
    un_pay:0,
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

    var page = this;
    var share_setting = wx.getStorageSync("share_setting");
    page.setData({
      share_setting: share_setting,
    });
    wx.showLoading({
      title: "正在加载",
      mask: true,
    });
    var ShareUserProfile = wx.getStorageSync("ShareUserProfile");
    if(ShareUserProfile){
      console.log(ShareUserProfile)
      page.setData({
        total_price: ShareUserProfile[0].total_price,
        price: ShareUserProfile[0].price,
        cash_price: ShareUserProfile[0].cash_price,
        un_pay: ShareUserProfile[0].un_pay
      });
    }else{
      app.request({
        url: api.share.get_info,
        success: function (res) {
          console.log("rq")
            page.setData({
              total_price: res[0].total_price,
              price: res[0].price,
              cash_price: res[0].cash_price,
              un_pay: res[0].un_pay
            });
          
        },
        complete: function () {
          wx.hideLoading();
        }
      });
    }
    wx.hideLoading();
  },
  tapName:function(e){
    var page = this;
    var active = '';
    if (!page.data.block){
      active = 'active';
    }
    page.setData({
      block:!page.data.block,
      active: active
    });

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
