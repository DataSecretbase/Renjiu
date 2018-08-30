//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    addressList:[]
  },

  selectTap: function (e) {
    var id = e.currentTarget.dataset.id;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/address/update',
      method: "POST",
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      data: {
        cookie: wx.getStorageSync('cookie'),
        id:id,
        isDefault:'true'
      },
      success: (res) =>{
        wx.navigateBack({})
      }
    })
  },

  addAddess : function () {
    wx.navigateTo({
      url:"/pages/address-add/index"
    })
  },
  
  editAddess: function (e) {
    wx.navigateTo({
      url: "/pages/address-add/index?id=" + e.currentTarget.dataset.id
    })
  },
  
  onLoad: function () {
    console.log('onLoad')

   
  },
  onShow : function () {
    this.initShippingAddress();
  },
  initShippingAddress: function () {
    var that = this;
    wx.request({
      url: "https://qgdxsw.com:8000/league/address/list",
      data: {
        cookie: wx.getStorageSync('cookie')
      },
      method:"POST",
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      success: (res) =>{
        if (res.data.code == 0) {
          console.log(res)
          that.setData({
            addressList:res.data.data
          });
        } else if (res.data.code == 700){
          that.setData({
            addressList: null
          });
        }
      }
    })
  }

})
