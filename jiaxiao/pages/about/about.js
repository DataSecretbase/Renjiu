// pages/about/about.js
const defaultPath='../../';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    logo:'https://mmbiz.qpic.cn/mmbiz_png/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44x8Ao0yjKVrC1PI5ZoFVObKMrpeicoC3UdRJkutkSHhsR873GpWjfM7Zw/0?wx_fmt=png',
    img:'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44x0R8RMuSbic0x4Eat5O7ecp5awWEbsOZpEmzFMs5s5TfTOHoeGvhObGQ/0?wx_fmt=jpeg'
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
  previewImage: function (event) {
    const app = getApp();
    const img = this.data.img;
    wx.previewImage({
      current: '', // 当前显示图片的http链接
      urls: [img] // 需要预览的图片http链接列表
    })
  }
})