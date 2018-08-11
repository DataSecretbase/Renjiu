// pages/shop_cart/index.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {

  },

  /**
   * 组件的初始数据
   */
  data: {
    haveGoods: true,
    goods: [
      {
        name: '如果你无法简洁的表达你的想法，那只说明你还不够了解它。',
        price: 1000,
        img: '',
        active: false,
        number: 1
      },
      {
        name: '如果你无法简洁的表达你的想法，那只说明你还不够了解它。',
        price: 1000,
        img: '',
        active: false,
        number: 1
      },
      {
        name: '如果你无法简洁的表达你的想法，那只说明你还不够了解它。',
        price: 1000,
        img: '',
        active: false,
        number: 1
      }
    ],
    saveHidden: true,
    totalPrice: 0,
    allSelect: true,
    noSelect: false,
    delBtnWidth: 120
  },

  /**
   * 组件的方法列表
   */
  methods: {
    selectTap: function (e) {
      let that = this;
      let i = e.currentTarget.dataset.index;
      this.data.goods[i].active = !this.data.goods[i].active;
    },
    jianBtnTap: function (e) {
      var index = e.currentTarget.dataset.index;
      var list = this.data.goods;
      if (index !== "" && index != null) {
        if (list[parseInt(index)].number > 1) {
          list[parseInt(index)].number--;
        }
      }
    },
    jiaBtnTap: function (e) {
      var index = e.currentTarget.dataset.index;
      var list = this.data.goods;
      if (index !== "" && index != null) {
        if (list[parseInt(index)].number < 10) {
          list[parseInt(index)].number++;
        }
      }
    }
  }
})
