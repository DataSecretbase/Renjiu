//app.js
App({
  onShow: function (options) {
    console.log(options);
  },
  onHide() {
    console.log('hide');
  },
  getUserInfo: function (cb) {
  },
  globalData: {
    userInfo: null,
    baseUrl: 'https://api.it120.cc/jy02149522',
    version: "1.7",
    cookie: 'tianqianwen',
    shareProfile: '百款精品商品，总有一款适合您', // 首页转发的时候话术
    navigate_type: 1,
    tlist: []
  },
  dateToObj(dateObj) {
    return JSON.parse(JSON.stringify(dateObj))
  },
  onLaunch: function () {
    var that = this;
    //  获取商城名称
    wx.request({
      url: that.globalData.baseUrl + '/config/get-value',
      data: {
        key: 'mallName'
      },
      success: function (res) {
        if (res.data.code == 0) {
          wx.setStorageSync('mallName', res.data.data.value);
        }
      }
    })
    this.getTlist();
    this.btnclick()
  },
  btnclick: function () {
    wx.getLocation({
      type: 'wgs84',// 默认wgs84
      success: function (res) {
        console.log(res)
      },
      fail: function (res) { },
      complete: function () { },
    });
  },
  sendTempleMsg: function (orderId, trigger, template_id, form_id, page, postJsonString) {
    var that = this;
    wx.request({
      url: that.globalData.baseUrl + '/template-msg/put',
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      data: {
        cookie: that.globalData.cookie,
        type: 0,
        module: 'order',
        business_id: orderId,
        trigger: trigger,
        template_id: template_id,
        form_id: form_id,
        url: page,
        postJsonString: postJsonString
      },
      success: (res) => {
        //console.log('*********************');
        //console.log(res.data);
        //console.log('*********************');
      }
    })
  },
  //获取类别列表
  getTlist() {
    var self = this;
    wx.request({
      url: "https://qgdxsw.com:8000/league/goods/list",
      data: {
        all: "true",
      },
      method: 'POST',
      header: {
        'content-type': 'application/x-www-form-urlencoded'
      },
      success: function (res) {
        //划分分类
        console.log(res.data.data)
        var _data = res.data.data, _tlist = [];
        //选出一级分类，放入firstType
        for (var x in _data) {
          if (_data[x].fields.level == 1) {
            _tlist.push({
              firstType: _data[x],
              second: []
            })
          }
          //判断是否存在二级分类
          if (self.globalData.navigate_type == 1 && _data[x].fields.level == 2) {
            console.log("type2")
            console.log(_data[x].fields.level)

            self.globalData.navigate_type = 2;
          }
        }
        //如果存在二级分类
        if (self.globalData.navigate_type == 2) {
          //选出二级分类，放入对应的secondList
          for (var x in _data) {
            for (var y in _tlist) {
              console.log("type2")
              console.log(_data[x].fields.pid, _tlist[y].firstType.pk)
              if (_data[x].fields.pid == _tlist[y].firstType.pk) {
                _tlist[y].second.push(_data[x]);
              }
            }
          }
          console.log(_tlist)

          //整理二级分类
          for (var x in _tlist) {
            //两行显示
            if (_tlist[x].second.length >= 10) {
              var _slist = _tlist[x].second;
              _tlist[x].secondList = [];
              _tlist[x].thirdList = [];
              for (var y in _slist) {
                if (y % 2) {
                  _tlist[x].thirdList.push(_slist[y]);
                } else {
                  _tlist[x].secondList.push(_slist[y]);
                }
              }
            }
          }
        } else {
          _tlist[0].secondList = [];
          _tlist[0].thirdList = [];
          for (var x in _tlist) {
            //两行显示
            if (_tlist.length >= 10) {
              if (x % 2) {
                _tlist[0].thirdList.push(_tlist[x].firstType);
              } else {
                _tlist[0].secondList.push(_tlist[x].firstType);
              }
            } else {
              _tlist[0].secondList.push(_tlist[x].firstType);
            }
          }
        }
        self.globalData.tlist = _tlist;
        console.log("_tlist!!!!!!!!!!!!!!!")
        console.log(_tlist)

      }
    })
  }
})