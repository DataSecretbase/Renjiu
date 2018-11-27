Page({
  data: {
    title: '江苏盛世华安智能科技有限公司',
    swipers: [
      { 'pic': 'http://www.jsssha.com/wp-content/uploads/2017/01/video.jpeg', 'link': '/pages/video/video' },
      { 'pic': 'http://img02.tooopen.com/images/20150928/tooopen_sy_143912755726.jpg', 'link': '' }
    ],
    indicatorDots: false,
    autoplay: false,
    interval: 5000,
    duration: 1000,

    news: [
      {
        'id': 0,
        'pic': 'http://toutiao.image.mucang.cn/toutiao-image/2016/09/27/17/6bbf63dc5c2040e8b3c2e948743f05b9.png!jpg2',
        'title': '驾照领取时间地点',
        'content': '为更加方便群众高效快捷办理机动车驾驶证业务，2013年新规推出了6项便民服务措施，其中一项是：将核发和补换领驾驶证的时限由3日缩短为1日。',
      },
      {
        'id': 1,
        'pic': 'http://toutiao.image.mucang.cn/toutiao-image/2016/09/27/17/a39ef4c3fe0c417ca2728b358714609f.png!jpg2',
        'title': '驾照年审',
        'content': '《机动车驾驶证申领和使用规定》实施后，驾驶证已经取消了年审，取而代之是有效期6年，10年和长期。但是A1，A2，A3，B1，B2证(以前的A证,B证)每年在驾驶证的初次领证日期后15日内要向车管所提交一份体检表',
      },
      {
        'id': 2,
        'pic': 'http://toutiao.image.mucang.cn/toutiao-image/2018/02/28/16/577f85c843df4f3498b42d0f2c5d3ba4.png!jpg2',
        'title': '2018交警手势图解 科目一巧记方法',
        'content': '交通警察手势——停止信号▼停止信号其表示不准前方车辆通行，手势为手举过头顶，手掌向前。交通警察手势——直行信号▼',
      }
    ]
  },
  onShareAppMessage: function () {
    // return custom share data when user share.
    console.log('onShareAppMessage')
    return {
      title: '盛世华安',
      desc: '小程序',
      path: '/pages/index/index'
    }
  },
});
