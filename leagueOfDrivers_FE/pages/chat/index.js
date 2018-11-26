Page({
  data: {
    visible: false,
    title:"yangzhongjuu",
    content:"u♥me",
  },
  hide() {
    this.setData({
      visible: false,
    })
  },
  onChange(e) {
    console.log('onChange', e)
    this.setData({
      visible: e.detail.visible,
    })
  },
})