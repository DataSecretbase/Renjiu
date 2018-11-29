//index.js
//获取应用实例
const app = getApp()
const date = new Date()
const years = []
const months = []
const days = []
for (let i = 2017; i <= date.getFullYear(); i++) {
  years.push(i)
}

for (let i = 1; i <= 12; i++) {
  months.push(i)
}

for (let i = 1; i <= 31; i++) {
  days.push(i)
}


Page({
  data: {
    motto: 'Hello World',
    years: years,
    year: date.getFullYear(),
    months: months,
    month: 2,
    days: days,
    day: 2,
    value: [9999, 1, 1],
    userInfo: {},
    hasUserInfo: false,
    addShow: false,
    pickShow: false,
    addText: '',
    status: '1',
    focus: false,
    lists: [],
    curLists: [],
    temp_item: null,
    temp_temp: null,
    editIndex: 0,
    delBtnWidth: 120, // 删除按钮宽度单位（rpx）
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  changeTodo: function (e) {
    var _this = this
    var item = e.currentTarget.dataset.item
    var temp = _this.data.lists
    console.log(e.currentTarget.dataset)
    temp.forEach(el => {
      if (el['pk'] == item) {

        if (el['fields']['status'] == 0) {

          el['fields']['status'] = 1,
            el['fields']['book_time_start'] = new Date().getTime(),
            _this.showCur(temp)
          wx.setStorage({
            key: "lists",
            data: temp
          })
          wx.showToast({
            title: '已完成任务',
            icon: 'success',
            duration: 1000
          });
        } else {
          wx.showModal({
            title: '',
            content: '该预约已完成，确定撤销？',
            confirmText: "确定",
            cancelText: "不了",
            success: function (res) {
              if (res.confirm) {
                el['fields']['status'] = '0',
                  _this.showCur(temp)
                wx.setStorage({
                  key: "lists",
                  data: temp
                })
              } else {
                return console.log('不操作')
              }
            }
          })
        }
      }
    })
  },

  commitTodo: function (e) {
    var _this = this
    var item = e.currentTarget.dataset.item
    var temp = _this.data.lists
    wx.showModal({
      title: '',
      content: '这些任务已完成，确定提交信息？',
      confirmText: "确定",
      cancelText: "不了",
      success: function (res) {
        if (res.confirm) {
          temp.forEach(el => {
            if (el['fields']['status'] == 1) {
              _this.showCur(temp)
              var form = {};
              form['date'] = el;
              console.log(form)
              //发起日期更新request
              wx.getStorage({
                key: 'token',
                success: function (res) {
                  form['token'] = res;
                  wx.request({
                    url: 'https://qgdxsw.com:8000/league/dateupdate',
                    method: 'GET',
                    data: form,
                    header: {
                      'content-type': 'application/json' // 默认值
                    },
                    success: function (res) {
                      wx.showToast({
                        title: '已完成任务',
                        icon: 'success',
                        duration: 1000
                      });
                      console.log(res)
                    }
                  })
                }
              })
            }
          })
          wx.setStorage({
            key: "lists",
            data: temp
          })
          console.log(temp)


        } else {
          return console.log('不操作')
        }
      }
    })

    console.log(item)
  },
  addTodoShow: function () {
    this.setData({
      addShow: true,
      focus: true
    })
  },
  addTodoHide: function () {
    this.setData({
      addShow: false,
      focus: false,
      addText: ''
    })
  },

  setInput: function (e) {
    this.setData({
      addText: e.detail.value
    })
  },
  addTodo: function (addT) {
    if (!this.data.addText.trim()) {
      return
    }
    var temp = this.data.lists

    temp.push(addT)
    this.showCur(temp)
    this.addTodoHide()
    wx.setStorage({
      key: "lists",
      data: temp
    })
    wx.showToast({
      title: '添加成功!',
      icon: 'success',
      duration: 1000
    });
  },

  /*getPhoneNumber: function (e) {
    console.log(e.detail.errMsg)
    console.log(e.detail.iv)
    console.log(e.detail.encryptedData)
  },
  */

  showCur: function (data) {
    if (this.data.status == 1) {
      this.setData({
        lists: data,
        curLists: data
      })
    } else {
      this.setData({
        lists: data,
        curLists: data.filter(item => +item.status === (this.data.status - 2))
      })
    }
  },
  showStatus: function (e) {
    console.log(this.data)
    var st = e.currentTarget.dataset.status
    if (this.data.status === st) return
    if (st === '1') {
      this.setData({
        status: st,
        curLists: this.data.lists
      })
      return
    }
    this.setData({
      status: st,
      curLists: this.data.lists.filter(item => +item['fields']['status'] === (st - 2))
    })
  },
  touchS: function (e) {
    // console.log('开始：' + JSON.stringify(e))
    // 是否只有一个触摸点
    if (e.touches.length === 1) {
      this.setData({
        // 触摸起始的X坐标
        startX: e.touches[0].clientX
      })
    }
  },
  touchM: function (e) {
    // console.log('移动：' + JSON.stringify(e))
    var _this = this
    if (e.touches.length === 1) {
      // 触摸点的X坐标
      var moveX = e.touches[0].clientX
      // 计算手指起始点的X坐标与当前触摸点的X坐标的差值
      var disX = _this.data.startX - moveX
      // delBtnWidth 为右侧按钮区域的宽度
      var delBtnWidth = _this.data.delBtnWidth
      var txtStyle = ''
      if (disX == 0 || disX < 0) { // 如果移动距离小于等于0，文本层位置不变
        txtStyle = 'left:0'
      } else if (disX > 0) { // 移动距离大于0，文本层left值等于手指移动距离
        txtStyle = 'left:-' + disX + 'rpx'
        if (disX >= delBtnWidth) {
          // 控制手指移动距离最大值为删除按钮的宽度
          txtStyle = 'left:-' + delBtnWidth + 'rpx'
        }
      }
      // 获取手指触摸的是哪一个item
      var index = e.currentTarget.dataset.index;
      var list = _this.data.curLists
      // 将拼接好的样式设置到当前item中
      list[index].txtStyle = txtStyle
      // 更新列表的状态
      this.setData({
        curLists: list
      });
    }
  },
  touchE: function (e) {
    // console.log('停止：' + JSON.stringify(e))
    var _this = this
    if (e.changedTouches.length === 1) {
      // 手指移动结束后触摸点位置的X坐标
      var endX = e.changedTouches[0].clientX
      // 触摸开始与结束，手指移动的距离
      var disX = _this.data.startX - endX
      var delBtnWidth = _this.data.delBtnWidth
      // 如果距离小于删除按钮的1/2，不显示删除按钮
      var txtStyle = disX > delBtnWidth / 2 ? 'left:-' + delBtnWidth + 'rpx' : 'left:0'
      // 获取手指触摸的是哪一项
      var index = e.currentTarget.dataset.index
      var list = _this.data.curLists
      list[index].txtStyle = txtStyle
      // 更新列表的状态
      _this.setData({
        curLists: list
      });
    }
  },
  delTodo: function (e) {
    var _this = this
    var item = e.currentTarget.dataset.item
    console.log(item)
    var temp = _this.data.lists
    temp.forEach((el, index) => {
      if (el.id === item) {
        temp[index].txtStyle = 'left:0'
        wx.showModal({
          title: '',
          content: '您确定要删除吗？',
          confirmText: "确定",
          cancelText: "考虑一下",
          success: function (res) {
            if (res.confirm) {
              temp.splice(index, 1)
              _this.showCur(temp)
              wx.setStorage({
                key: "lists",
                data: temp
              })
            } else {
              _this.showCur(temp)
              return console.log('不操作')
            }
          }
        })
      }
    })

  },
  showDevices: function () {
    wx.getStorage({
      key: 'key',
      success: function (res) {
        var addT = {
          id: new Date().getTime(),
          title: res.data.devices.device_info[0][1],
          status: '0'
        }
        addTodo(res);
        console.log(res.data)
      }
    })
  },
  onLoad: function () {
    this.books()
  },
  //登录用户
  books: function (cb) {

    var that = this
    wx.request({
      url: "https://qgdxsw.com:8000/league/checkqr",
      data: {
        token: wx.getStorageSync('token'),
      },
      method: "GET",
      success: function (res) {
        if (res.data.code != 0) {
          // 登录错误 
          wx.hideLoading();
          wx.showModal({
            title: '失败',
            content: res.data.msg,
            showCancel: false
          })
          return;
        }
        var info = res['data']
        console.log(res['data'])
        that.setData({
          lists: info['data'],
          curLists: info['data']
        })
      }
    })

  },

  globalData: {
    domain: 'https://qgdxsw.com:8000/league/',
    token: ''
  },

})
var Util = require('../../../utils/util.js')