// components/bargain/bargain.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    pList: {
      type: Array,
      value: [],
      observer: function (newVal, oldVal) {
        this.setData({
          pList: newVal
        })
      }
    },
    sHeight: {
      type: Number,
      value: 0
    },

  },

  /**
   * 组件的初始数据
   */
  data: {
    show: "none"

  },

  /**
   * 组件的方法列表
   */
  methods: {
    onSelectTime:function(e) {
        const { startTimeText, endTimeText } = e.detail;
        this.setData({
          startTimeText,
          endTimeText,
        })
    },
    redictDetail:function(e){
      console.log(e)
      console.log(this.properties.pList[e.currentTarget.dataset.index])
      console.log(e.currentTarget.dataset.item)
      this.setData({
        'pList':this.properties.pList
        }
      )
      if(e.currentTarget.dataset.item == 'none')
      {
        this.properties.pList[e.currentTarget.dataset.index].fields.show = "block";
        this.setData({
          'pList': this.properties.pList})
      }
      else if (e.currentTarget.dataset.item == 'block'){this.properties.pList[e.currentTarget.dataset.index].fields.show = "none"
        this.setData({
          'pList': this.properties.pList
        })
}
    },
    commit:function(e){
      console.log(this.data.startTimeText, this.data.endTimeText)
      this.properties.pList[e.currentTarget.dataset.index].fields.show = "none"
      this.setData({
        'pList': this.properties.pList
      })
      wx.request({
        url: "https://qgdxsw.com:8000/league/book/add",
        data: {
          cookie: wx.getStorageSync('cookie'),
          startTimeText:this.data.startTimeText,
          endTimeText: this.data.endTimeText,
          coach_id: this.properties.pList[e.currentTarget.dataset.index].fields.coach.id,
          train_ground: this.properties.pList[e.currentTarget.dataset.index].fields.train_ground,
        },
        method: "GET",
        success: function (res) {
          if (res.data.code != 0) {
            // 预约错误 
            wx.hideLoading();
            wx.showModal({
              title: '失败',
              content: res.data.msg,
              showCancel: false
            })
            return;
          }
          console.log(res)
        }
      })
    }
  }
})
