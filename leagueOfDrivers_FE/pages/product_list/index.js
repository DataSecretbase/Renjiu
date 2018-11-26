var app = getApp();
// pages/product_list/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    page:1,
    hidden:true
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    this.setData({
      id:options.id
    })
    this.getList();
  },
  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    this.getList();
  },

  formatDateTime(inputTime) {
    var date = new Date(inputTime);
    var y = date.getFullYear();
    var m = date.getMonth() + 1;
    m = m < 10 ? ('0' + m) : m;
    var d = date.getDate();
    d = d < 10 ? ('0' + d) : d;
    var h = date.getHours();
    h = h < 10 ? ('0' + h) : h;
    var minute = date.getMinutes();
    var second = date.getSeconds();
    minute = minute < 10 ? ('0' + minute) : minute;
    second = second < 10 ? ('0' + second) : second;
    return y + '-' + m + '-' + d + ' ' + h + ':' + minute + ':' + second;
  },
  getList(){

    var self = this;
    var _page = self.data.page;
    self.setData({
      hidden: false
    })
    console.log(self.data.id)
    //获取分类商品
    wx.request({
      url: 'https://qgdxsw.com:8000/league/goods/list',
      header: { "Content-Type": "application/x-www-form-urlencoded" },
      method: "POST",
      data: {
        page: _page,
        pageSize: 6,
        categoryId: self.data.id,
      },
      success: function (res) {
        console.log(res)
        if (!res.data.data) {
          wx.showToast({
            title: res.data.msg
          })
          self.setData({
            hidden: true
          })
          return false
        }
        var second = app.globalData.tlist[0].second
        var en_name = "";
        for (var x in second)
        {

           if(second[x].pk == res.data.data[0].fields.category_id)
           {
             en_name = second[x].fields.eng_name;
             
           }
           
        }
        if (en_name == "parter") {
          wx.navigateTo({
            url: "/pages/joinus/index"
          })
          return
        }
        if (en_name == "tuisong") {
          wx.navigateTo({
            url: "/pages/tribune/index/index"
          })
          return
        }
        if (en_name == "share") {
          wx.navigateTo({
            url: "/pages/tribune/news/news-details?id=0"
          })
          return
        }
        if (en_name == "jiakaoliucheng") {
          wx.navigateTo({
            url: "/pages/tribune/news/news-details?id=1"
          })
          return
        }
        if (en_name == "jiakaobaodian") {
          wx.navigateTo({
            url: "/pages/tribune/news/news-details?id=2"
          })
          return
        }
        if (en_name == "zixun") {
          wx.navigateTo({
            url: "/pages/tribune/news/news-details?id=3"
          })
          return
        }
        if (en_name == "coupons") {
            wx.navigateTo({
              url: "/pages/my-coupon/index"
            })
            return
        }
        self.setData({
          en_name:en_name,
          page : _page+1,
          list: _page == 1 ? res.data.data : self.data.list.concat(res.data.data)
        });//当前页页数+1
        if(en_name == 'appointment'){

          wx.request({
            url: 'https://qgdxsw.com:8000/league/isenrol',
            method: "GET",
            data: {
              cookie: wx.getStorageSync('cookie')
            },
            success: function (res) {
              console.log(res.data.code)
              if (res.data.code != 0) {
                wx.showModal({
                  title: '提示',
                  content: res.data.msg,
                  showCancel: false
                })
                for (var x in self.data.list) {
                  console.log('en_name ' + x)

                  wx.request({
                    url: 'https://qgdxsw.com:8000/league/school/detail',
                    header: { "Content-Type": "application/x-www-form-urlencoded" },
                    method: "POST",
                    data: {
                      bookid: self.data.list[x]['fields']['shop_id']
                    },
                    success: function (res) {
                      console.log('en_name serc  ' + x)
                      for (var y in self.data.list) {
                        if (self.data.list[y]['fields']['shop_id'] == res.data.data[0]['pk']) {
                          self.data.list[y]['fields']['shop_id'] = res.data.data[0]
                        }
                      }
                      console.log(res.data.data)

                      console.log(self.data.list)
                    }
                  })
                }
                return;
              }
            }
          })
        en_name = "book";
          self.setData({
            en_name: en_name,
          })

          wx.request({
            url: 'https://qgdxsw.com:8000/league/coach/list',
            method: "GET",
            data: {
              cookie: wx.getStorageSync('cookie')
            },
            success: function (res) {
              console.log(res.data.code)
              if (res.data.code != 0) {
                wx.showModal({
                  title: '提示',
                  content: res.data.msg,
                  showCancel: false
                })
                return
              }
              for(var coach in res.data.data){
                res.data.data[coach].fields.show = "none"
                for(var book in res.data.data[coach].book_list){
                  res.data.data[coach].book_list[book].fields.book_time_start_datetime = self.formatDateTime(res.data.data[coach].book_list[book].fields.book_time_start)
                  res.data.data[coach].book_list[book].fields.book_time_end_datetime = self.formatDateTime(res.data.data[coach].book_list[book].fields.book_time_start)
                }
              }
              console.log(res.data.data)

              self.setData({
                coach_list:res.data.data
              })
            }
          })

        }
        if (en_name == 'driverSchool') {


                for (var x in self.data.list) {
                  console.log('en_name ' + x)

                  wx.request({
                    url: 'https://qgdxsw.com:8000/league/school/detail',
                    header: { "Content-Type": "application/x-www-form-urlencoded" },
                    method: "POST",
                    data: {
                      bookid: self.data.list[x]['fields']['shop_id']
                    },
                    success: function (res) {
                      console.log('en_name serc  ' + x)
                      for (var y in self.data.list) {
                        if (self.data.list[y]['fields']['shop_id'] == res.data.data[0]['pk']) {
                          self.data.list[y]['fields']['shop_id'] = res.data.data[0]
                        }
                      }
                      console.log(res.data.data)

                      console.log(self.data.list)
                    }
                  })
                }

        }

        wx.hideNavigationBarLoading() //完成停止加载
        wx.stopPullDownRefresh() //停止下拉刷新
        self.setData({
          hidden: true
        })
      }
    })
  }
})
