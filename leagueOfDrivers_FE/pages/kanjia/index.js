//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');

Page({
  data: {
    autoplay: true,
    interval: 3000,
    duration: 1000,
    swiperCurrent: 0,
    goodsDetail: {}

  },

  //事件处理函数
  swiperchange: function (e) {
    //console.log(e.detail.current)
    this.setData({
      swiperCurrent: e.detail.current
    })
  },
  onLoad: function (e) {
    this.data.id = e.id;
    this.data.kjId = e.kjId;
    this.data.joiner = e.joiner;
    console.log(e.id, e.kjId,e.joiner)
    var that = this;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/goods/detail',
      data: {
        id: e.id
      },
      success: function (res) {
        console.log(res.data.data)
        that.data.goodsDetail = res.data.data;
        console.log("goodsDetail")
        console.log(res.data.data)
        that.setData({
          goodsDetail: res.data.data
        });
        WxParse.wxParse('article', 'html', res.data.data.content, that, 5);
      }
    })
    console.log("e.kjId, e.joiner")

    console.log(e.kjId, e.joiner)
    this.getKanjiaInfo(e.kjId, e.joiner);
    //this.getKanjiaInfoMyHelp(e.kjId, e.joiner);
  },
  onShareAppMessage: function () {
    var that = this;
    return {
      title: "帮我来砍价",
      path: "/pages/kanjia/index?kjId=" + that.data.kjId + "&joiner=" + that.data.joiner + "&id=" + that.data.id,
      success: function (res) {
        // 转发成功
      },
      fail: function (res) {
        // 转发失败
      }
    }
  },
  getVideoSrc: function (videoId) {
    var that = this;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/goods/detail',
      data: {
        videoId: videoId
      },
      success: function (res) {
        if (res.data.code == 0) {
          that.setData({
            videoMp4Src: res.data.data.fdMp4
          });
        }
      }
    })
  },
  getKanjiaInfo: function (kjid, joiner) {
    var that = this;
    console.log('joiner')

    console.log(joiner)
    wx.request({
      url: 'https://qgdxsw.com:8000/league/bargain/detail',
      data: {
        kjid: kjid,
        joiner: joiner,
      },
      success: function (res) {
        if (res.data.code != 0) {
          wx.showModal({
            title: '错误',
            content: res.data.msg,
            showCancel: false
          })
          return;
        }
        console.log("kanjiainfo")

        console.log(res.data.data)
        that.setData({
          kanjiaInfo: res.data.data
        });
      }
    })
  },
  getKanjiaInfoMyHelp: function (kjid, joiner) {
    var that = this;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/bargain/add',
      data: {
        kjid: kjid,
        joinerUser: joiner,
        token: wx.getStorageSync('token')
      },
      success: function (res) {
        if (res.data.code == 0) {
          that.setData({
            kanjiaInfoMyHelp: res.data.data,
            curuid: wx.getStorageSync(' ')
          });
        }
      }
    })
  },
  helpKanjia: function () {
    var that = this;
    wx.request({
      url: 'https://qgdxsw.com:8000/league/bargain/add/',
      data: {
        kjid: that.data.kjId,
        joinerUser: that.data.joiner,
        token: wx.getStorageSync('token')
      },
      success: function (res) {
        if (res.data.code != 0) {
          wx.showModal({
            title: '提示',
            content: res.data.msg,
            showCancel: false
          })
          return;
        }
        that.setData({
          mykanjiaInfo: res.data.data
        });
        wx.showModal({
          title: '成功',
          content: '成功帮好友砍掉 ' + res.data.data.cutPrice + ' 元',
          showCancel: false
        })
        that.getKanjiaInfo(that.data.kjId, that.data.joiner);
        that.getKanjiaInfoMyHelp(that.data.kjId, that.data.joiner);
      }
    })
  },
  tobuy: function () {
    wx.navigateTo({
      url: "/pages/goods-details/index?id=" + this.data.kanjiaInfo.kanjiaInfo.goodsId + "&kjId=" + this.data.kanjiaInfo.kanjiaInfo.kjId
    })
  }
})