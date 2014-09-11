/**
 * Created by yuan on 8/17/14.
 */



function login(){
//    alert('???')
//    记得写val()
    var username=$('#username').val()
    var password=$('#password').val()
    if(username==""){
        alert('请填写用户名')
        return false
    }
    if(password==""){
        alert('请填写密码')
        return false
    }
    $.post('/login/',
        {
            username:username,
            password:password
        },
        function(data,status){
            if(data=='admin'){
                location.href='/admin/'
            }else if(data=='center'){
                location.href='/center/user/'+username
            }else if(data=='department'){
                location.href='/department/user/'+username
            }else if(data=='member'){
                location.href='/member/user/'+username

            }else if(data=='error0'){
                alert('role参数错误，不在0~3之间')
                location.reload()
            }else if(data=='error1'){
                alert('用户名/密码错误')
                location.reload()
            }else if(data=='error2'){
                alert('请输入密码')
                location.reload()
            }else if(data=='error3'){
                alert('请输入用户名')
                location.reload()
            }
        })
}




function changePassword(role,obj){
    var oldpassword=$('#oldpassword').val()
    var newpassword=$('#newpassword').val()
    var renewpassword=$('#renewpassword').val()
    var username=obj.getAttribute('data-username')
    if(oldpassword==''){
        alert('请输入旧密码')
        return false
    }
    if(newpassword==''){
        alert('请输入新密码')
        return false
    }
    if(renewpassword==''){
        alert('请确认密码')
        return false
    }
    $.post('/'+role+'/changepwd',
        {
            oldpassword:oldpassword,
            newpassword:newpassword,
            renewpassword:renewpassword
        },
        function (data,status) {
            if(data=='success'){
                alert('修改成功')
                location.href='/'+role+'/user/'+username
            }else{
                alert(data)
                location.reload()
            }

    })
}


function updateInfo(username){
//    var sno=$('#sno').val()
    var realname=$('#realname').val()
    var sex=$('#sex').val()
    var school=$('#school').val()
    var email=$('#email').val()
    var birthday=$('#birthday').val()
    var department=$('#department').val()
//    alert('aaaaa')
//    alert(department)

    var tag=$('#tag').val()
//    if(sno==''){
//        alert('学号不能为空')
//        return false
//    }
    if(realname==''){
        alert('真实姓名不能为空')
        return false
    }
    if(sex!='0'&&sex!='1'){
        alert('请注意你的性别')
        return false
    }
    if(school==''){
        alert('学院不能为空')
        return false
    }
    if(email==''){
        alert('email不能为空')
        return false
    }
    if(birthday==''){
        alert('生日不能为空')
        return false
    }
    if(department==''){
        alert('学院不能为空')
        return false
    }

    if(tag==''){
        alert('自我介绍不能为空')
        return false
    }

//    alert('nmb')
    $.post('/member/info/write',
        {
//            sno:sno,
            realname:realname,
            sex:sex,
            school:school,
            email:email,
            birthday:birthday,
            department:department,

            tag:tag
        },
        function(data,status){
            if(data=='success'){
                alert('提交成功！')
                location.href='/member/user/'+username
            }
            else{
                alert(data)
                location.reload()
            }
        })

}



function varifyMember(userid,mes,obj){
    var userid=userid
    var mes=mes
    var tester=obj.getAttribute('data-tester')
//    alert(userid)
//    alert(mes)
//    alert(tester)
    var url='/department/view/user/'+userid+'/varify'
    $.post('/department/view/user/'+userid+'/varify',
        {
            userid:userid,
            mes:mes,
            tester:tester
        },
        function(data,status){
            alert(data)
            location.href='/department/list/state/0/'
        })
//    alert(url)
//    alert(userid)
//    alert(mes)
//    alert(tester)

}