/**
 * Created by yuan on 8/17/14.
 */

document.onkeydown = function (e) {
    var theEvent = window.event || e;
    var code = theEvent.keyCode || theEvent.which;
    if (code == 13 || code == 32) {
        $("#login").click();
    }
}

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

            if(data=='success'){
                alert('登录成功！')
                location.href='/admin'
            }
            else if(data=='error1'){
                alert('用户名/密码错误')
                location.reload()
            }
            else if(data=='error2'){
                alert('请输入密码')
                location.reload()
            }
            else if(data=='error4'){
                alert('系统错误')
                location.reload()
            }


        })
}




function changePassword(){
    var oldpassword=$('#oldpassword').val()
    var newpassword=$('#newpassword').val()
    var renewpassword=$('#renewpassword').val()

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
    $.post('/user/changepwd',
        {
            oldpassword:oldpassword,
            newpassword:newpassword,
            renewpassword:renewpassword
        },
        function (data,status) {
            if(data=='success'){
                alert('修改成功')
                location.href='/admin'
            }else{
                alert(data)
                location.reload()
            }

    })
}


function addUser(){
    var username=$('#username').val()
    var password=$('#password').val()
    var repassword=$('#repassword').val()
    if(username==''){
        alert('请输入用户名')
        return false
    }
    if(password==''){
        alert('请输入新密码')
        return false
    }
    if(repassword==''){
        alert('请确认密码')
        return false
    }
    if(password!=repassword){
        alert('两次密码不一致')
        return false
    }

    $.post('/user/add',
        {
            username:username,
            password:password,
            repassword:repassword
        },
        function(data,status){
            if(data=='success'){
                alert('添加成功！')
                location.reload()
            }
            else{
                alert(data)
                location.reload()
            }
        })

}

function deleteUser(obj){
    var userid=obj.getAttribute('data-userid')
    $.post('/user/delete',
        {
            userid:userid
        },
        function (data,status) {
            if(data=='success'){
                alert('删除成功')
                location.reload()
            }
            else if(data=='self'){
                alert('删除了自己')
                location.href='/logout'

            }
            else{
                alert('删除失败')
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


function addCategory1(){
    var categoryname=$('#categoryname1').val()
    var parentid='0'
    if(categoryname==''){
        alert('请输入模块名')
        return false
    }
    alert(categoryname)
    $.post('/category/add/',
        {
            categoryname:categoryname,
            parentid:parentid
        },
        function(data,status){
            if(data=='success'){
                alert('添加成功')
                location.reload()

            }
            else{
                alert(data)
                location.reload()
            }
        }
    )
}

function addCategory2(){
    var categoryname=$('#categoryname2').val()
    var parentid=$('#select').attr('data-parentid')
    if(!parentid){
        alert('请选择父模块')
        return false
    }
    if(categoryname==''){
        alert('请输入模块名')
        return false
    }
    $.post('/category/add/',
        {
            categoryname:categoryname,
            parentid:parentid
        },
        function(data,status){
            if(data=='success'){
                alert('添加成功')
                location.reload()

            }
            else{
                alert(data)
                location.reload()
            }
        }
    )
}

function selectCategory(obj){
    $('.category1_item').attr("id","unselect")
    $(obj).attr('id','select')
    $('.category1_item').css({'background':'#eee','color':'#666','border-color':'#ddd'})
    $(obj).css({'background-color':'#2F95CE','border-color':'#2F95CE','color':'#ffffff'})
}

function deleteCategory(obj){
    var categoryid=obj.getAttribute('data-categoryid')

    $.post('/category/delete',
        {
            categoryid:categoryid
        },
        function (data, status) {
            if(data=='success'){
                alert('删除成功！')
                location.reload()
            }else{
                alert('删除失败')
                location.reload()
            }
        })
}


function verifyArticle(state,obj){
//    alert('啊啊啊')
    var articleid=obj.getAttribute('data-articleid')
    var articlestate=obj.getAttribute('data-articlestate')
    var state=state
    if(articlestate=='3'){
        if(state=='2'||state=='1'){
            alert('三申的文章不可退回')
            location.reload()
        }

    }
//    alert('zzz')

//    alert('bbb')
    $.post('/article/verify/'+state,
        {
            articleid:articleid

        },
        function(data,status){

            if(data=='success'){
                alert('审核成功')
                location.reload()
            }else{
                alert('审核失败')
                location.reload()
            }

        })
}

function deleteArticle(obj){
    var articleid=obj.getAttribute('data-articleid')
    $.post('/article/delete',
        {
            articleid:articleid
        },
        function(data,status){
            if(data=='success'){
                alert('删除成功')
                location.reload()
            }else{
                alert('删除失败')
                location.reload()
            }
        })
}


function addArticle(){
    var title=$('#title').val();
    var content=UE.getEditor('editor').getContent();
    var categoryid=$('.active').attr('data-categoryid');
    var author=$('#author').val();
    var publisher=$('#publisher').val();
    $.post('/article/action/add',
        {
            title:title,
            content:content,
            categoryid:categoryid,
            author:author,
            publisher:publisher
        },
        function(data,status){
            if(data=='success'){
                alert('添加成功')
                location.reload()
            }else{
                alert(data)
                location.reload()
            }
        })
}


function updateArticle(obj){
    var articleid=obj.getAttribute('data-articleid')

    var title=$('#title').val();
    var content=UE.getEditor('editor').getContent();
    var categoryid=$('.active').attr('data-categoryid');
    var author=$('#author').val();
    var publisher=$('#publisher').val();

    $.post('/article/action/update/'+articleid,
        {

            title:title,
            content:content,
            categoryid:categoryid,
            author:author,
            publisher:publisher
        },
        function(data,status){
            if(data=='success'){
                alert('修改成功')
                location.reload()
            }else{
                alert(data)
                location.reload()
            }
        })
}


$(document).ready(function(){

    $("#selectLevel").click(function(){
        if($(this).val()=="1"){
            $("#erji").slideUp("slow")
            $("#yiji").slideDown("slow")
        }

        else if($(this).val()=="2"){
            $("#yiji").slideUp("slow")
            $("#erji").slideDown("slow")
        }

    })
})

$(document).ready(function(){

    $(".renameButton").click(function(){
        $("input").css("display","none")
        $("span").css("display","inline")
//        console.log("asgw")
        var categoryid=$(this).attr("data-categoryid")
//        console.log("bbbb"+categoryid+"aaa")
        var parentTd=$(this).parent()
        var tds=parentTd.siblings()

        var nameTd=tds.eq(1)
        var categoryname=nameTd.text()
        var inputEle=nameTd.find("input")
        var spanEle=nameTd.find("span")

//        var innerHtml="<input type="+"'text'"+" id='changedname'"+" value='"+categoryname+"'"+">"


//        nameTd.html(innerHtml)
        inputEle.css("display","inline")
        spanEle.css("display","none")
        $(this).text("确认修改")
        $(this).click(function(){
            $.post('/category/rename',
                {
                    categoryid:categoryid,
                    categoryname:inputEle.val()
                },
                function(data,status){
                    if(data=='success'){
                        alert('修改成功')

                    }
                    else{
                        alert(data)

                    }
                    location.reload()
                })
        })
    })
})



