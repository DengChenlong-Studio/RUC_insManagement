// 表单提交
function Form_Submit() {
    let csrf = $("[name=csrfmiddlewaretoken]").val();
    let user = $('#inputUser').val().trim();
    let pwd = $('#inputPassword').val().trim();
    //let code = $('#code').val();

    //判断input不能为空
    if (user.length == 0) {
        swal({
            title: '用户名不能为空！',
            type: 'error',  //展示成功的图片
            timer: 1000,  //延时毫秒数
            showConfirmButton: false  //关闭确认框
        }, function () {
            //刷新当前页面
            window.location.reload();
        });
        return false
    }

    if (pwd.length == 0) {
        swal({
            title: '密码不能为空！',
            type: 'error',  //展示成功的图片
            timer: 1000,  //延时毫秒数
            showConfirmButton: false  //关闭确认框
        }, function () {
            //刷新当前页面
            window.location.reload();
        });
        return false
    }

    //发送ajax请求
    $.ajax({
        url: "/login/",
        type: "post",
        data: {
            username: user,
            password: pwd,
            csrfmiddlewaretoken: csrf,
        },
        success: function (data) {
            console.log(data);
            arg = JSON.parse(data);
            //console.log(arg.status);
            if (arg.code == "200") { //判断http 状态
                swal({
                    title: '登录成功！',
                    type: 'success',  //展示成功的图片
                    timer: 500,  //延时500毫秒
                    showConfirmButton: false  //关闭确认框
                }, function () {
                    window.location.href = "/index/";  //跳转后台首页
                });
            } else {
                swal({
                    title: '登录失败！',
                    type: 'error',  //展示成功的图片
                    timer: 1000,  //延时毫秒数
                    showConfirmButton: false  //关闭确认框
                }, function () {
                    //console.log("登录失败");
                    //刷新当前页面
                    window.location.reload();
                });
            }
        },
        error: function (data) {
            //console.log("失败data",data);
            swal({
                text: '网络请求不可达',
                title: '登录失败',
                type: 'error',
            });
            //刷新当前页面
            window.location.reload();
        }
    });
}

// 滑块验证码
$('#mpanel4').slideVerify({
    type: 2,   //类型
    vOffset: 5,  //误差量，根据需求自行调整
    vSpace: 5, //间隔
    imgName: ['1.jpg', '2.jpg'],
    imgSize: {
        // 设置100%宽度
        width: '100%',
        height: '200px',
    },
    blockSize: {
        width: '40px',
        height: '40px',
    },
    barSize: {
        width: '100%',
        height: '40px',
    },
    ready: function () {
    },
    success: function () {
        //alert('验证成功，添加你自己的代码！');
        //......后续操作
        Form_Submit()
    },
    error: function () {
        //              alert('验证失败！');
    }

});