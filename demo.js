function startTime()
{
    var today=new Date();
    var h=today.getHours();
    var m=today.getMinutes();
    var s=today.getSeconds();
    m=checkTime(m);
    s=checkTime(s);
    document.getElementById('time').innerHTML="当前时间为："+h+":"+m+":"+s;
    setTimeout(function(){startTime()},500);
}
 
function checkTime(i)
{
    if (i<10)
    {
        i="0" + i;
    }
    return i;
}
