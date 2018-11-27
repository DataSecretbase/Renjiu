// pages/news/news.js
Page({
  data:{
    'news': [
      {
        'id': 10,
        'pic': 'http://toutiao.image.mucang.cn/toutiao-image/2016/06/14/18/8b231791cf694e4fa3520a1dfe6c574b.jpeg!jpg2',
        'title': '[盘点]2018驾考科二5个常考常识！',
        'content': '整个考场为一个“凸”字型，考生驾车进入考场后考试开始，此时“凸”字上方凸起的车库应在车辆前进方向右侧，考生应先将车辆驾驶至“凸”字左侧尽头边线前，然后向右后方倒车入库。'
      },
      {
        'id': 11,
        'pic': 'http://www.jsssha.com/wp-content/uploads/2016/10/1-300x250.png',
        'title': '科目二驾考太难？你可能忽视了这些……',
        'content': '驾考规定，驾考科目二“五门必考”必须一次通过，否则重考。考驾照证一直是现代人比较关注的话题，新规出台，又添加了不少的难度，小编在这方面稍有一点点经验，也对网络上不同的版本进行了整理，最后总结了一下经验形成了最新的驾校五项考试技巧供大家参考，一定会对您以后的考驾照之路有所帮助。'
      },
      {
        'id': 12,
        'pic': 'http://www.jsssha.com/wp-content/uploads/2016/10/DSC_4148-300x250.jpg',
        'title': '科目三灯光模拟并不难 这样练就对了',
        'content': '在这个“心理素质”主宰一切的驾驶考试中，科目三灯光模拟考试是最考验考生反应能力的，当然，学好这些，其实这与反应能力无关'
      },
      {
        'id': 13,
        'pic':'http://toutiao.image.mucang.cn/toutiao-image/2017/01/26/13/a679f1ff2ed84c6299d6430193b02b5e.png!jpg2',
        'title': '科二中途停车不合格改为“每次扣5分”后，该怎么做？',
        'content': '科目二考试中，中途停车是直接扣100分的。在考试项目区域内，汽车停顿2秒以上都算中途停车。'
      },
      {
        'id': 14,
        'pic':'http://toutiao.image.mucang.cn/toutiao-image/2016/09/20/17/10fff3d486a2405fa41a6f69699cd3d0.jpeg!jpg2',
        'title': '恶劣天气与复杂路段下，该怎么选？',
        'content': '下雨时路面湿，轮胎与路面之间的滑动摩擦因素小，相应的摩擦力也要变小。所以紧急制动时，汽车轮胎停止滚动，而向前滑动。或者说滑动摩擦力不能有效减慢汽车速度导致汽车还要向前滑出很大段距离。因此下雨路滑,宜减速行驶。'
      },
      {
        'id': 15,
        'pic':'http://www.jsssha.com/wp-content/uploads/2016/09/20130604083316_39766-300x250.jpg',
        'title': '3个秘诀搞定科三灯光模拟考？',
        'content': '科目三灯光模拟考试作为科目三考试内容，很多考生会觉得灯光操作很简单，所以不以为然，从而导致在科目三考试时，大意失荆州。'
      }
    ]
  },
  onLoad:function(options){
    // 页面初始化 options为页面跳转所带来的参数
  },
  onReady:function(){
    // 页面渲染完成
  },
  onShow:function(){
    // 页面显示
  },
  onHide:function(){
    // 页面隐藏
  },
  onUnload:function(){
    // 页面关闭
  },
  go: function(event) {
    wx.navigateTo({
      url: '/pages/tribune/news/news-details?id=' + event.currentTarget.dataset.type
    })
  }
})
