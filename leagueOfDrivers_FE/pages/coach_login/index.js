// pages/joinShop/joinShop.js
const web_url = getApp().globalData.web_url;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    imgUrl: [],

    
    input_items: [
      { name: 'username', placeholder: '教练账户' },
      { name: 'password', placeholder: '教练密码' },
    ]
  },
  inputFn: function (e) {
    var that = this;
    var index = e.currentTarget.dataset.id
    if (index == 0) {
      that.setData({
        cpname: e.detail.value
      })
    } else if (index == 1) {
      that.setData({
        project: e.detail.value
      })
    } else if (index == 2) {
      that.setData({
        nickname: e.detail.value
      })
    } else if (index == 3) {
      if (e.detail.value.length !== 11) {
        wx.showToast({
          title: '号码格式不对',
          icon: 'success',
          image: '',
          duration: 800,
          mask: true,
          success: function (res) { },
        })
      }
      that.setData({
        phone: e.detail.value
      })
    } else if (index == 4) {
      that.setData({
        content: e.detail.value
      })
    }
  },
  formSubmit: function (e) {
    var that = this;
    console.log(that.data)
    console.log(wx.getStorageSync('token'))

    wx.request({
      url: 'https://qgdxsw.com:8000/league/coach/login',
      data: {
        //username: e.detail.value.username,
        username: 'tqw233',

        password: 'tqw503417',
        token: wx.getStorageSync('token')
      },
      header: {
        'Content-Type': 'application/json'
      },
      method: 'GET',
      success: function (res) {
        // console.log(that.data.value)
        wx.showToast({
          title: res.data.msg,
          icon: 'success',
          image: '',
          duration: 1000, 
          mask: true,
          success: function (res) { },
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    //获取轮播图
    wx.request({
      url: web_url + '/app.php?c=Message&act=photo',
      data: {},
      header: { 'content-type': 'application/json' },
      method: 'GET',
      dataType: 'json',
      success: function (res) {
        that.setData({
          imgUrl: res.data
        })
      },
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

  }
})