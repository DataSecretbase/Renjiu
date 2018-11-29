var plugin = requirePlugin("myPlugin")
var wxCharts = require('../../utils/wxcharts.js');
var app = getApp();
var lineChart = null;
var startPos = null;
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
  touchHandler: function (e) {
    lineChart.scrollStart(e);
  },
  moveHandler: function (e) {
    lineChart.scroll(e);
  },
  touchEndHandler: function (e) {
    lineChart.scrollEnd(e);
    lineChart.showToolTip(e, {
      format: function (item, category) {
        return category + ' ' + item.name + ':' + item.data
      }
    });
  },
  createSimulationData: function () {
    var categories = [];
    var data = [];
    for (var i = 0; i < 10; i++) {
      categories.push('201620162-' + (i + 1));
      data.push(Math.random() * (20 - 10) + 10);
    }
    return {
      categories: categories,
      data: data
    }
  },
  onLoad: function (e) {
    var windowWidth = 320;
    try {
      var res = wx.getSystemInfoSync();
      windowWidth = res.windowWidth;
    } catch (e) {
      console.error('getSystemInfoSync failed!');
    }

    var simulationData = this.createSimulationData();
    lineChart = new wxCharts({
      canvasId: 'lineCanvas',
      type: 'line',
      categories: simulationData.categories,
      animation: false,
      series: [{
        name: '成交量1',
        data: simulationData.data,
        format: function (val, name) {
          return val.toFixed(2) + '万';
        }
      }],
      xAxis: {
        disableGrid: false
      },
      yAxis: {
        title: '成交金额 (万元)',
        format: function (val) {
          return val.toFixed(2);
        },
        min: 0
      },
      width: windowWidth,
      height: 200,
      dataLabel: true,
      dataPointShape: true,
      enableScroll: true,
      extra: {
        lineStyle: 'curve'
      }
    });
  },
  set_fetch: function(e){
    var self = this
    wx.request({
      url: 'https://qgdxsw.com:8000/league/booksets/all',
      data: {
        token: wx.getStorageSync("token"),
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

        token: wx.getStorageSync("token"),
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
        token: wx.getStorageSync('token'),
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
        token:wx.getStorageSync('token'),
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