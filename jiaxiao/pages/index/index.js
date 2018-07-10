//index.js
const defaultPath = '../../';
let count=0;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    name: '东南驾校桑园训练基地',
    logo: 'https://mmbiz.qpic.cn/mmbiz_png/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44x8Ao0yjKVrC1PI5ZoFVObKMrpeicoC3UdRJkutkSHhsR873GpWjfM7Zw/0?wx_fmt=png',
    address: '东莞市东城区桑园狮环路(科技园路对面入200米)',
    timeText: '8:00-21:00',
    phoneNum: '13580719991',
    imageList: [
'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xjp85fzWByxQMIINNGGGqttovib7ZTgYyUMq5X59MBc2M5SRRPQfMplw/0?wx_fmt=jpeg',
      
'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xpZsgPWjibP3s9U5T2bibBgGAmQdIm9n0siaO8ZmM2q5N3RAiaWZ41X2LXg/0?wx_fmt=jpeg',
      'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xXficVZDuGENq922DN05uLdD5lFu7HrQezs03vxLDwstdVGDxSia89bjQ/0?wx_fmt=jpeg'
    ]
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
  openMap: function () {
    wx.openLocation({
      latitude: 23.0680771882,
      longitude: 113.8142964982,
      scale:-30,
      address: '广东省东莞市东城区桑园狮环路'
    });
  },
  makePhoneCall: function () {
    const phoneNum = this.data.phoneNum;
    wx.makePhoneCall({
      phoneNumber: phoneNum,
      fail: function () {
        console.log('无法接通')
      }
    })
  },
  previewImage: function (event) {
    const app = getApp();
    const imgList = this.data.imageList;
    wx.previewImage({
      current: '', // 当前显示图片的http链接
      urls: imgList // 需要预览的图片http链接列表
    })
  },
  moreImg:function(){
    if(count==0){
      var list = this.data.imageList;
      list = list.concat([
      
        'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xxq6XRxGfGzU6kPbZkzwiamThCUEQNCDT6N3zHanWQ9auzptBrwia9mQQ/0?wx_fmt=jpeg',
              'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xncSfq98bs7cpkKnh7XU3W5kicwiarRVHc5BzGI1sIrCia5deEibWNLXf8g/0?wx_fmt=jpeg',
        'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xBiaHibUDXkdbmMveN8CtKuHwbYeXvgLvZVhbH2TKf8mbaNDMqIfiabOqA/0?wx_fmt=jpeg',
        'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xvbpLVlPIG9Bj5eoPDxtzKX4j4hYb4tbtZAvWaAJ6qBtXiaybKa6Yr7A/0?wx_fmt=jpeg',
        'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xjczcZOrHBHF4ZY29SNnvEoa9mQepMOoMPPWibib6sKHKhMCxhBdy3Zgw/0?wx_fmt=jpeg',
        'https://mmbiz.qpic.cn/mmbiz_jpg/Zo9MJ96lSvRubRa3iaAB0efTV5ictzv44xjC79fpFIa8fG3mbVGsZpTmkTsex7xIRmcibj2YQfXRjYicDT0XhbhHwg/0?wx_fmt=jpeg'
        
      ]);
      this.setData({
        imageList: list
      });
      count=1;
    }
  },
  followMath:function(){
    wx.showModal({
      title: '微信小贴士',
      content: '已关注的请从公众号列表进入，\n未关注的按如下步骤进行关注：\n1、打开微信点击右上角“+”\n2、选择添加朋友\n3、选择公众号\n4、输入“东南驾校桑园训练基地”\n5、添加并关注',
      showCancel:false
    })
  }
})
