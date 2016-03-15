$(function(){
    $(".input").on('focus', '#userName', function(){
        $('#userName').css("background", "url('../../static/image/login/input_name_hover.png') no-repeat scroll left top");
        if ($('#userName').val() == "用户名"){
            $('#userName').val("");
        }
    })
    $(".input").on("blur", '#userName', function(){
        $('#userName').css("background", "url('../../static/image/login/input_name.png') no-repeat scroll left top");
        if ($('#userName').val() == ''){
            $('#userName').val("用户名");
        }
    });

    $('#password').attr("type", "text");
    $('#password').val("密码");
    $(".input").on("focus", '#password', function(){
        if ($('#password').val()=="密码"){
            $('#password').attr("type", "password");
            $('#password').val("");
        }
        $('#password').css("background", "url('../../static/image/login/input_password_hover.png') no-repeat scroll left top");

    });
    $(".input").on("blur", '#password', function(){
        if ($('#password').val() == ""){
            $('#password').attr("type", "text");
            $('#password').val("密码");
        }
        $('#password').css("background", "url('../../static/image/login/input_password.png') no-repeat scroll left top");

    });
    $("#verificationCode").click(function(){
        $("#verificationCode").attr("src", "getVerificationCode?rand=" + Math.random());
        return false;
    });

    $("#registerUser").validate({
        rules: {
            reg_username: {
                required: true,
                remote: {
                    url: "checkUser",
                    type: "get",
                    dataType: "json",
                    data: {
                        reg_username: function(){
                            return $("#reg_username").val();
                        }
                    }
                }
            },

            reg_usermail: {
                required: true,
                email:true
            },
            reg_password: {
                required: true,
                minlength: 5
            },
            conformpassword: {
                required: true,
                minlength: 5,
                equalTo: "#reg_password"
            },
            verificationData: {
                required: true,
                remote: {
                    url: "VerificationCode",
                    type: "get",
                    dataType: "json",
                    data: {
                        verificationData: function(){
                            return $("#VerificationData").val();
                        }
                    }
                }
            }
        },
        messages: {
            reg_username: {
                required: "请输入用户名",
                remote: "该用户已存在"
            },
            reg_usermail: {
                required: "请输入Email地址",
                email: "请输入正确的email地址"
            },
            reg_password: {
                required: "请输入密码",
                minlength: "密码不能小于{0}个字 符"
            },
            conformpassword: {
                required: "请输入确认密码",
                minlength: "确认密码不能小于5个字符",
                equalTo: "两次输入密码不一致不一致"
            },
            verificationData: {
                required: "请输入验证码",
                remote: "验证码输入错误，请重新输入",
            }
        },
        showErrors: function(errorMap, errorList){
            $.each(errorMap, function(index, value){
                //alert(value);
                if (value == '验证码输入错误，请重新输入'){
                    $("#verificationCode").attr("src", "getVerificationCode?rand=" + Math.random());
                }
            });
            this.defaultShowErrors();
        },
        errorPlacement: function(error, element){
            element.parent().append(error);
        },

        debug: false,
        submitHandler: function(form){
            form.submit();
            $("#reg_submit").attr("disabled", "true");


        },
        wrapper: "p",
        errorElement: "label",
        onkeyup: false,

    });
    if ($("#ok").html() == 1){
        $(".registerNofity").html("恭喜你，注册成功！正在跳转登陆界面....");
        $("#modelLayer").show();
        $("#registerSuccess").show();
        //var user = $("#user").html();
        setTimeout(function(){this.location.href="Login.html"},3000);
        //setTimeout(function(){this.location.href="/login/"},3000);
    };
    $("#loginSubmit").submit(function(){
        $("#error").hide();
        if ($("#userName").val() == "用户名" || $("#password").val() == "密码"){
           //alert("error");
           $("#error").show();
           return false;
        }
        window.location.reload();
    });
    if($("#loginInfonation").text() == "success"){
            var dialog = frameElement.dialog;
            dialog.close();
        }else{
        $("#loginInfonation").css('display', "block");
    }

});