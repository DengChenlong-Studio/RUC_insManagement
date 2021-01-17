/*fn_load_banner();

    // 轮播图
    let $banner = $(".banner");
    let $picLi = $(".banner .pic li");
    let $prev = $(".banner .prev");
    let $next = $(".banner .next");
    let $tabLi = $(".banner .tab li");
    let index = 0;

    // 小圆点点击事件
    $tabLi.click(function () {
        index = $(this).index();
        $(this).addClass("active").siblings("li").removeClass("active");
        $picLi.eq(index).fadeIn(1500).siblings("li").fadeOut(1500);
    });
    // 点击切换上一张
    $prev.click(function () {
        index--;
        if(index < 0){
            index = $tabLi.length - 1;
        }
        $tabLi.eq(index).addClass("active").siblings("li").removeClass("active");
        $picLi.eq(index).fadeIn(1500).siblings("li").fadeOut(1500);

    }).mousedown(function () {
        return false;
    });

    // 点击切换下一张
    $next.click(auto).mousedown(function(){
        return false;
    })

    function auto(){
        index ++;
        index %= $tabLi.length;
        $tabLi.eq(index).addClass("active").siblings("li").removeClass("active");
        $picLi.eq(index).fadeIn(1500).siblings("li").fadeOut(1500);
    }

    // 定时器
    let timer = setInterval(auto, 2000);
    $banner.hover(function () {
        clearInterval(timer);
    }, function () {
        auto();
    });

    function fn_load_banner(){
        $.ajax({
            url: "/banner/",
            type: "GET",
            async: false
        })
            .done(function (res) {
                if(res.errno === "0"){
                    let content = ``;
                    let tab_content = ``;
                    $(".pic").html("");
                    $(".tab").html("");
                    res.data.banner.forEach(function(one_banner, index){
                        // console.log(one_banner);
                        if(index === 0){
                            console.log(one_banner);
                            content = `
                            <li style="display:block;"><a href="/static/images/${one_banner.news_id}/">
                 <img src="${one_banner.image_url}" alt="${one_banner.news_title}"></a></li>
                            `;
                            tab_content = `
                            <li class="active"></li>
                            `
                        }
                        else{
                            console.log(one_banner);
                            content = `
                            <li><a href="/static/images/${one_banner.news_id}/"><img src="${one_banner.image_url}" alt="${one_banner.news_title}"></a></li>
                            `
                            tab_content = `
                            <li></li>
                            `
                        }
                        $(".pic").append(content);
                        $(".tab").append(tab_content);
                    })
                }
                else{
                    message.showError(res.errmsg);
                }
            })
            .fail(function(){
                message.showError('服务器超时，请重试！');
            })
    }
*/
function moveElement(ele,x_final,y_final,interval){//ele为元素对象
  var x_pos=ele.offsetLeft;
  var y_pos=ele.offsetTop;
  var dist=0;
  if(ele.movement){//防止悬停
    clearTimeout(ele.movement);
  }
  if(x_pos==x_final&&y_pos==y_final){//先判断是否需要移动
    return;
  }
  dist=Math.ceil(Math.abs(x_final-x_pos)/10);//分10次移动完成
  x_pos = x_pos<x_final ? x_pos+dist : x_pos-dist;

  dist=Math.ceil(Math.abs(y_final-y_pos)/10);//分10次移动完成
  y_pos = y_pos<y_final ? y_pos+dist : y_pos-dist;

  ele.style.left=x_pos+'px';
  ele.style.top=y_pos+'px';

  ele.movement=setTimeout(function(){//分10次移动，自调用10次
    moveElement(ele,x_final,y_final,interval);
  },interval)
}





var img=document.getElementById('img');

var list=document.getElementById('index').getElementsByTagName('li');
var index=0;//这里定义index是变量，不是属性

var nextMove=function(){//一直向右移动，最后一个之后返回
  index+=1;
  if(index>=list.length){
    index=0;
  }
  moveIndex(list,index);
  moveElement(img,-720*index,0,20);
};
var play=function(){
  timer=setInterval(function(){
    nextMove();
  },2500);
};
for(var i=0;i<list.length;i++){//鼠标覆盖上哪个小圆圈，图片就移动到哪个小圆圈，并停止
  list[i].index=i;//这里是设置index属性，和index变量没有任何联系
  list[i].onmouseover= function () {
    var clickIndex=parseInt(this.index);
    moveElement(img,-720*clickIndex,0,20);
    index=clickIndex;
    moveIndex(list,index);
    clearInterval(timer);
  };
  list[i].onmouseout= function () {//移开后继续轮播
    play();
  };
}
