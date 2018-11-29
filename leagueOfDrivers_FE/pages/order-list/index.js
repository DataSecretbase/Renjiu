var wxpay = require('../../utils/pay.js')
var app = getApp();
Page({
  data:{
    statusType:[
      {name:"待付款",page:0},
      {name:"待发货",page:0},
      {name:"待收货",page:0},
      {name:"待评价",page:0},
      {name:"已完成",page:0}],
    currentType:0,
    list:[[],[],[],[],[]],
    goodsMap:[{},{},{},{},{}],
    logisticsMap:[{},{},{},{},{}],
    windowHeight:''
  },
  onLoad(options){
    this.getList();
    var systemInfo = wx.getSystemInfoSync()
    this.setData({
      windowHeight: systemInfo.windowHeight,
      currentType:options.id ? options.id:0
    })
  },
  // 点击tab切换 
  swichNav: function (res) {
    if (this.data.currentType == res.detail.currentNum) return;
    this.setData({
      currentType: res.detail.currentNum
    })
  } , 
  bindChange:function(e){
    this.setData({
      currentType: e.detail.current
    })
    console.log(e.detail.current)
    if (!this.data.list[e.detail.current].length)
      this.getList();
  } ,
  getList(){
    wx.showLoading();
    var that = this;
    var postData = {
      token: wx.getStorageSync('token'),
      status: that.data.currentType
    };
    var _page = that.data.statusType[that.data.currentType].page+1 ;;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/order/list',
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      method: "POST",
      data: postData,
      success: (res) => {
        console.log(res)
        wx.hideLoading();
        var param = {}, str1 = "list[" + that.data.currentType + "]", str2 = 'statusType[' + that.data.currentType + '].page', str3 = "logisticsMap[" + that.data.currentType + "]", str4 = "goodsMap[" + that.data.currentType + "]" ;
        if (res.data.code == 0) {
          param[str1] = res.data.data.orderList ;
          param[str2] = _page ;
          //param[str3] = res.data.data.logisticsMap ;
          param[str3] = "";

          param[str4] = res.data.data.goodsMap ;

          for (var orders in res.data.data.orderList)
          {
            param[str1][orders]["fields"].goodsmap = []
            for (var goods in param[str4])
            {
              console.log(param[str1][orders].pk, param[str4][goods].fields.order_id)
              if (param[str1][orders].pk == param[str4][goods].fields.order_id)
              {
                param[str1][orders]["fields"].goodsmap.push(param[str4][goods].fields);
              }
            }
          }
          console.log("param[str1]")

          console.log(param[str1])
          that.setData(param);
        } else {
          param[str1] = [];
          param[str3]= {};
          param[str4] = {};
          this.setData(param);
        }
      }
    })
  },
  orderDetail: function (e) {
    var orderId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: "/pages/order-details/index?id=" + orderId
    })
  },
  cancelOrderTap: function (e) {
    var that = this;
    var orderId = e.currentTarget.dataset.id;
    wx.showModal({
      title: '确定要取消该订单吗？',
      content: '',
      success: function (res) {
        if (res.confirm) {
          wx.showLoading();
          wx.request({
            url: 'https://qgdxsw.com:8000/league/order/close',
            header: { "Content-Type": "application/x-www-form-urlencoded" },
            method: "POST",
            data: {
              token: wx.getStorageSync('token'),
              orderId: orderId
            },
            success: (res) => {
              wx.hideLoading();
              if (res.data.code == 0) {
                var param = {}, str = 'statusType[' + that.data.currentType + '].page';
                param[str]=0;
                that.getList();
              }
            }
          })
        }
      }
    })
  },
  toPayTap: function (e) {
    var that = this;
    var orderId = e.currentTarget.dataset.id;
    console.log(e)
    var money = e.currentTarget.dataset.money;
          wx.request({
            url: 'https://qgdxsw.com:8000/league/order/pay',
              method:'POST',
              header: {
                'content-type': 'application/x-www-form-urlencoded'
              },
              data: {
                token: wx.getStorageSync('token'),
                orderId: orderId
              },
              success: function (res2) {
                wx.reLaunch({
                  url: "/pages/order-list/index"
                });
              }
            })
    wx.login({
      success: function (res) {
        if (res.code) {
          wx.request({
            url: 'https://qgdxsw.com:8000/league/order/pay',
            method: 'POST',
            header: {
              'content-type': 'application/x-www-form-urlencoded'
            },
            data: {
              token: wx.getStorageSync('token'),
              orderId: orderId
            },
            success: function (res) {
              console.log(res.data)
              wx.requestPayment({
                timeStamp: res.data.timeStamp,
                nonceStr: res.data.nonceStr,
                package: res.data.package,
                signType: 'MD5',
                paySign: res.data.paySign,
                success: function (res) {
                  // success
                  console.log(res);
                },
                fail: function (res) {
                  // fail
                  console.log(res);
                },
                complete: function (res) {
                  // complete
                  console.log(res);
                }
              })
            }
          })
        } else {
          console.log('获取用户登录态失败！' + res.errMsg)
        }
      }
    });
    wxpay.wxpay(app, money, orderId, "/pages/order-list/index");
  },
  onHide:function(){
    // 生命周期函数--监听页面隐藏
 
  },
  onUnload:function(){
    // 生命周期函数--监听页面卸载
 
  },
  onPullDownRefresh: function() {
    // 页面相关事件处理函数--监听用户下拉动作
   
  },
  onReachBottom: function() {
    // 页面上拉触底事件的处理函数
  
  }
})