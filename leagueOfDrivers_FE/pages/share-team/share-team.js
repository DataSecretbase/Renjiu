// pages/share-team/share-team.js
var api = require('../../api.js');
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    status:1,
    first_count:0,
    second_count:0,
    third_count:0,
    list:Array
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var page = this;
    var share_setting = wx.getStorageSync("share_setting");
    page.setData({
      share_setting: share_setting,
    });
    page.GetList(options.status || 1);
  },
  GetList: function (status) {
    var page = this;
    page.setData({
      status: parseInt(status || 1),
    });
    if(page.data.list){
      return
    }
    var account = wx.getStorageSync("account")

    app.request({
      url: api.share.get_team,
      data: {
        status: page.data.status,
      },
      method:'GET',
      success: function (res) {
        console.log(res)
        page.setData({
          user: res.team[0],
          first_count: res.team[1].length,
          second_count: res.team[2].length,
          third_count: res.team[3].length,
          list: res.team,
        });
      },
    });
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
  
  }
})