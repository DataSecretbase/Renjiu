Component({
  properties: {
    pList: {
      type: Array,
      value: [
        { name: 'cpname', placeholder: '您的商户名称' },
        { name: 'project', placeholder: '请输入您的主营项目' },
        { name: 'nickname', placeholder: '您的姓名' },
        { name: 'phone', placeholder: '您的手机号码' },
      ],

      observer: function (newVal, oldVal) {
        this.setData({
          pList: newVal
        })
      }
    },
    en_name: {
      type: String,
      value: "goods"
    },
    sHeight: {
      type: Number,
      value: 0
    }
  },
  methods: {
    product_detail: function (e) {
      var _id = e.currentTarget.dataset.id;
      wx.navigateTo({
        url: "/pages/goods-details/index?id=" + e.currentTarget.dataset.id
      })
    }
  }
})