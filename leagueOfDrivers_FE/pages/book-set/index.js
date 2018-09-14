var plugin = requirePlugin("myPlugin")
import {$wuxSelect} from '../../dist/wux_dist/index'
Page({
  data: {
    isShow: false,
    dateStr: '',
   
      value1: '',
      title1: '',
      value2: '',
      title2: '',
      value3: '',
      title3: '',

  },
  onLoad: function () {
    this.set_fetch()
  },
  set_fetch: function(e){
    var self = this
    wx.request({
      url: 'https://qgdxsw.com:8000/league/booksets/all',
      data: {
        cookie: wx.getStorageSync("cookie"),
        set_type:"default"
      },
      success(res) {
        if (res.data.code == 0) {
          console.log(res)
          self.setData({
            option:res.data.data.option
          })
        }
      }
    })
  },
  _yybindchange: function (e) {
    console.log(e)
    this.setData({
      dateStr: e.detail.date
    })
  },
  onChange(event) {
    wx.showToast({
      icon: 'none',
      title: `该时间段预约人数：${event.detail/10}`
    });
  },
  cellClick: function () {
    var isShow = true
    this.setData({
      isShow: isShow
    })
  },
    changeTime: function () {
    console.log('111')
  }
  , onClick1(e) {
    console.log(e)
    wx.request({
      url: 'https://qgdxsw.com:8000/league/booksets/update',
      data: {

        cookie: wx.getStorageSync("cookie"),
      },
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      method: "POST",
      success(res) {
        if (res.data.code == 0) {
          console.log(res)
        }
      }
    })
    $wuxSelect('#wux-select1').open({
      
      value: this.data.value1,
      options: this.data.option,
      onConfirm: (value, index, options) => {
        console.log(value, index, options)
        this.setData({
          value1: value,
          title1: options[index],
        })
      },
    })
  },
  onClick2() {
    $wuxSelect('#wux-select2').open({
      value: this.data.value2,
      options: [{
        title: 'iPhone 3GS',
        value: '001',
      },
      {
        title: 'iPhone 5',
        value: '002',
      },
      {
        title: 'iPhone 5S',
        value: '003',
      },
      {
        title: 'iPhone 6',
        value: '004',
      },
      {
        title: 'iPhone 6S',
        value: '005',
      },
      {
        title: 'iPhone 6P',
        value: '006',
      },
      {
        title: 'iPhone 6SP',
        value: '007',
      },
      {
        title: 'iPhone SE',
        value: '008',
      },
      {
        title: 'iPhone 7',
        value: '009',
      },
      ],
      onConfirm: (value, index, options) => {
        console.log(value, index, options)
        this.setData({
          value2: value,
          title2: options[index].title,
        })
      },
    })
  },
  BookSetsAll(){
    wx.request({
      url: 'https://qgdxsw.com:8000/league/booksets/all',
      data: {
        cookie: wx.getStorageSync('cookie'),
      },
      success(res) {
        if (res.data.code == 0) {
          console.log(res)
          self.setData({
            options: res.data.data.option,
            booksetes_id: res.data.data.book_set_id,
          })
        } else if (res.data.code != 0) {
          wx.showModal({
            title: '添加预约时间错误',
            content: res.data.msg,
            showCancel: false,
          })
        }
      }
    })
  },
  addBookTimeSet(){
    var self = this
    console.log('11')
    wx.request({
      url: 'https://qgdxsw.com:8000/league/booksets/add',
      data: {
        cookie:wx.getStorageSync('cookie'),
        type:"default",
      },
      success(res) {
        if (res.data.code == 0) {
          console.log(res)
          self.setData({
            options: res.data.data.option,
            booksetes_id: res.data.data.book_set_id,
          })
        }else if(res.data.code !=0){
          wx.showModal({
            title: '添加预约时间错误',
            content: res.data.msg,
            showCancel: false,
          })
        }
      }
    })
  }
})