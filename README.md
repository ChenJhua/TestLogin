# TestLogin
Django实现的手机短信验证码+极验验证的小demo

## 手机短信验证码

###Demo代码已放上GitHub，实现登录短信校验+极验验证
####[https://github.com/ChenJhua/TestLogin](https://github.com/ChenJhua/TestLogin)



 - 打开网站[互亿无线](http://user.ihuyi.com/login.html)注册一个账号，有50条免费短信
 - ![这里写图片描述](https://img-blog.csdn.net/20180427212411877?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
 - 登录进去后会有以下页面
 ![这里写图片描述](https://img-blog.csdn.net/20180427212453261?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
 
 - 使用图中的APIID和APIKEY开启你的免费手机短信旅程，可以使用接口下载、接口帮助实现Django手机短信验证
 - ![这里写图片描述](https://img-blog.csdn.net/20180427212652343?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
# 开始我的短信教程
 
1.注册页面加入两个文本框
```
               <li>
					<label for="">手机号码:</label>
                   <input type="text" placeholder="11位数的手机号码" id="mobile" name="mobile"/>
                   <span class="error_tip">提示信息</span>
			</li>
               <li>
                   <label for="">验证码:</label>
                   <input type="text" name="code" placeholder="请输入手机验证码" style="width: 140px;">
                   &nbsp;&nbsp;
                   <input type="button" value=" 获取验证码" id="zphone" style="width: 100px;margin-left: 10px">
               </li>
```
在models.py中定义手机号码字段：

```
    # 不要定义int型,否则存不进数据库,会报错,Out of range
    # 建议使用char类型
    uphone = models.CharField(max_length=11)
```

2.使用js+ajax请求短信发送和按钮计时触发

```
	$('#zphone').click(
		function(){
		//发送验证码
		$.get('/user/send_message', {mobile:$('#mobile').val()}, function(msg) {
			alert(jQuery.trim(msg.msg));
			if(msg.msg=='提交成功'){
				RemainTime();
			}
		});
	})

	//按钮倒计时
	var iTime = 60;
	sTime = ''
	function RemainTime(){
		if (iTime == 0) {
			document.getElementById('zphone').disabled = false;
			sTime="获取验证码";
			iTime = 60;
			document.getElementById('zphone').value = sTime;
			return;
		}else{
			document.getElementById('zphone').disabled = true;
			sTime="重新发送(" + iTime + ")";
			iTime--;
		}
		setTimeout(function() { RemainTime() },1000)
		document.getElementById('zphone').value = sTime;
	}

	// 检查用户输入的手机号是否合法
	function check_mobile() {

		var re = /^1[345678]\d{9}$/; //校验手机号

		if(re.test($('#mobile').val()))
		{
			$('#mobile').next().hide();
			error_mobile = false;
			document.getElementById('zphone').disabled = false;
		}
		else
		{
			$('#mobile').next().html('你输入的手机格式不正确')
			$('#mobile').next().show();
			error_mobile = true;
			document.getElementById('zphone').disabled = true;
		}
	}

```

3.配置url

```
    url(r'^send_message$', views.send_message, name='send_message'),
```

4.定义发送短信的视图函数

```
# 请求的路径
host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"
# 用户名是登录ihuyi.com账号名（例如：cf_demo123）
account = "C44****38"
# 密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
password = "ddd**************30 "

def send_message(request):
    """发送信息的视图函数"""
    # 获取ajax的get方法发送过来的手机号码
    mobile = request.GET.get('mobile')
    # 通过手机去查找用户是否已经注册
    user = User.objects.filter(uphone=mobile)
    if len(user) == 1:
        return JsonResponse({'msg': "该手机已经注册"})
    # 定义一个字符串,存储生成的6位数验证码
    message_code = ''
    for i in range(6):
        i = random.randint(0, 9)
        message_code += str(i)
    # 拼接成发出的短信
    text = "您的验证码是：" + message_code + "。请不要把验证码泄露给其他人。"
    # 把请求参数编码
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    # 请求头
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    # 通过全局的host去连接服务器
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    # 向连接后的服务器发送post请求,路径sms_send_uri是全局变量,参数,请求头
    conn.request("POST", sms_send_uri, params, headers)
    # 得到服务器的响应
    response = conn.getresponse()
    # 获取响应的数据
    response_str = response.read()
    # 关闭连接
    conn.close()
    # 把验证码放进session中
    request.session['message_code'] = message_code
    print(eval(response_str.decode()))
    # 使用eval把字符串转为json数据返回
    return JsonResponse(eval(response_str.decode()))
```

## 极验验证

###Demo代码已放上GitHub，实现登录短信校验+极验验证
####[https://github.com/ChenJhua/TestLogin](https://github.com/ChenJhua/TestLogin)


1.先到[极验验证网站](http://www.geetest.com/index)注册一个账号，登录上去
![这里写图片描述](https://img-blog.csdn.net/20180427213855635?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
2.创建应用
![这里写图片描述](https://img-blog.csdn.net/20180427214152296?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![这里写图片描述](https://img-blog.csdn.net/20180427214206936?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
3.出现如下的id和key
![这里写图片描述](https://img-blog.csdn.net/20180427214238316?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
4.可以根据安装指引自行学习，也可以按我步骤来
![这里写图片描述](https://img-blog.csdn.net/20180427214345842?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

# 极验验证码

在form表单添加代码
提交按钮id必须为：id="embed-submit"
后面使用ajax时使用

css代码块：

```
/* 极验验证的样式 */
#embed-captcha {
	width: 300px;
	margin: 0 auto;

}
.show {
	display: block;
}
.hide {
	display: none;
}
#notice {
	color: red;
}
```

```
{# 极验验证 #}
<div id="embed-captcha"></div>
<p id="wait" class="show">正在加载验证码......</p>
<p id="notice" class="hide">请先拖动验证码到相应位置</p>
<input type="submit" name="" value="登录" class="input_submit" id="embed-submit">
```

js代码块

```
<script>
    var handlerEmbed = function (captchaObj) {
        $("#embed-submit").click(function (e) {
            var validate = captchaObj.getValidate();
            if (!validate) {
                $("#notice")[0].className = "show";
                setTimeout(function () {
                    $("#notice")[0].className = "hide";
                }, 1000);
                e.preventDefault();
            }
        });
        // 将验证码加到id为captcha的元素里，同时会有三个input的值：geetest_challenge, geetest_validate, geetest_seccode
        captchaObj.appendTo("#embed-captcha");
        captchaObj.onReady(function () {
            $("#wait")[0].className = "hide";
        });
        // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
    };
    $.ajax({
        // 获取id，challenge，success（是否启用failback）
        url: "/user/pc-geetest/register?t=" + (new Date()).getTime(), // 加随机数防止缓存
        type: "get",
        dataType: "json",
        success: function (data) {
            // 使用initGeetest接口
            // 参数1：配置参数
            // 参数2：回调，回调的第一个参数验证码对象，之后可以使用它做appendTo之类的事件
            initGeetest({
                gt: data.gt,
                challenge: data.challenge,
                product: "embed", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
                offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
                // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
            }, handlerEmbed);
        }
    });
</script>
```

url配置：

```
    # 极验验证
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
```

视图views.py:

```
# 极验验证,请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "910*****************************01"  # id
pc_geetest_key = "73d****************************03"  # key

def pcgetcaptcha(request):
    """极验验证函数"""
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


```

成功后会出现极验验证码，显示正在加载时需要等待一下，请求别人的网络还没生成验证码，这个验证码已经自带校验是否输入验证码，验证码是否正确：
![这里写图片描述](https://img-blog.csdn.net/20180427215032586?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5odWExMTI1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
