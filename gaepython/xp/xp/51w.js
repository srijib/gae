if (!document.layers){function hr()
	{document.write("<div><hr></div>")}}
function menu0(img,txt,click)
	{document.write("<div onMouseOver=this.className='over' onMouseOut=this.className='overout' onclick='"+click+"'><img border='0' src=xp/"+img+".gif align='absmiddle'  hspace='6' vspace='1'>"+txt+"</div>")}
function menu1(img,txt,show)
	{document.write("<div onMouseOver=this.className='over';show('"+show+"') onMouseOut=this.className='overout';hide('"+show+"') ><img border='0' src=xp/"+img+".gif align='absmiddle' width='24' height='24' hspace='6' vspace='1'>"+txt+"<span style='visibility: hidden'>-----</span><font face='Webdings'>4</font></div>")}
function title(txt,id){
	document.write("<table border='0' cellpadding='0' cellspacing='0' width='100%' height='19'><tr><td class='title' style='padding-left:6px' OnMouseDown=m('"+id+"') title="+txt+"><font face=Wingdings >1</font>"+txt+"</td><td width='16' noWrap ><img id=shut border='0' class=up1 OnMouseout=this.className='up1' OnMouseDown=this.className='down' onclick=hide('"+id+"')  src='xp/closexp.gif' title=关闭对话框 width='15' height='15'></td></tr></table>")}
function start(w,act,img,alt){
	document.write("<td align='center' width="+w+" noWrap height='27' style='padding:1px' ><img class=up  id='startmenu' OnMouseDown=this.className='down' onclick="+act+"  src=xp/"+img+".gif  width=44 height=20 align=absmiddle alt="+alt+"></td>")}
function qico(w,act,img,alt,c){
	document.write("<td align='center' width="+w+" noWrap height='25' style='padding:1px' ><img class='"+c+"'  OnMouseOver=this.className='up1' OnMouseup=this.className='up1' OnMouseout=this.className='out'  onclick=this.className='down1';GradientClose();updown();"+act+" src=xp/"+img+".gif  width=20 height=20 align=absmiddle alt="+alt+"></td>")}
function img(w,img,alt,act){
	document.write("<td align='center' width="+w+" noWrap height='25' style='padding:1px'><img alt='"+alt+"' src=xp/"+img+".gif   align=absmiddle ondblclick="+act+" onclick=updown();GradientClose()></td>")}
function item(w,img,txt,act){
	document.write("<td><table border='0' cellpadding='0' cellspacing='0' height='23' width="+w+" class=up1 title="+txt+"-www.518.Com OnMouseout=this.className='up1' OnMouseDown=this.className='down';updown();GradientClose();"+act+"><tr><td valign='middle'><img  src=xp/"+img+".gif  hspace='3' align=absmiddle>"+txt+"-518</td></tr></table></td>")}
function td(w){
	document.write("<td align='center' width="+w+" noWrap height='25' style='padding:1px'></td>")}
function ico(id,top,left,target,text,alt){
	document.write("<div id="+id+" style='position:absolute; top:"+top+"; left:"+left+"; width:56; height:56;display:block;z-index:1;cursor: default'  onDblClick='"+target+"' OnMouseOver=this.className='ico_over'  OnMouseOut=this.className='ico' class=ico><p align='center'><img border=0 onmousedown=m('"+id+"') vspace=5 src=xp/"+id+".gif alt="+alt+"  width='32' height='32'><br>"+text+"</div>")}
function cssbutton(css,txt,bg,c)
	{document.write("<input  type='Button' class=up onclick="+css+" value="+txt+"  style='font-family: 宋体; font-size: 9pt; border: 1 none "+bg+"'>")}
function link(act,txt)
	{document.write("<div class=link onMouseOver=this.className='overlink' onMouseOut=this.className='link' style='padding-left:16;padding-top:1;padding-bottom:1' onclick="+act+">"+txt+"</div>")}
function fav(win,txt)
	{document.write("<tr><td  onclick=pop('"+win+"');hide('fav') onMouseOver=this.className='over' onMouseOut=this.className='out' alt="+win+"><img border='0' src='xp/ie16.gif' hspace=4 vspace=2 align=absmiddle width=16 height=16>"+txt+"</td></tr>")}
function addfav()
	{window.external.addFavorite('http://www.y518.com','一笑家园')}
function viewcode()
	{window.location="view-source:"+window.location.href}
var Mouse_Obj="none";
var pX
var pY
document.onmousemove=D_NewMouseMove;
document.onmouseup=D_NewMouseUp;
function m(c_Obj)
{ Mouse_Obj=c_Obj;
pX=parseInt(document.all(Mouse_Obj).style.left)-event.x;
pY=parseInt(document.all(Mouse_Obj).style.top)-event.y; }
function D_NewMouseMove()
{if(Mouse_Obj!="none")
{document.all(Mouse_Obj).style.left=pX+event.x;
document.all(Mouse_Obj).style.top=pY+event.y;
event.returnValue=false;}}
function D_NewMouseUp()
{Mouse_Obj="none";}
var NSkey=(navigator.appName=="Netscape");function tick()
{var today;var timeString="";var hours,minutes,seconds,wday;var intHours,intMinutes,intSeconds;var wdaysE=new Array("SUN","MON","TUE","WED","THU","FRI","SAT");var wdaysC=new Array("","","","","","","");today=new Date();intHours=today.getHours();intMinutes=today.getMinutes();intSeconds=today.getSeconds();if(NSkey)
{wday=wdaysE[today.getDay()];}else
{wday=wdaysC[today.getDay()];}if(intHours<10)
{hours="0"+intHours;}else
{hours=intHours;}if(intMinutes<10)
{minutes=":0"+intMinutes;}else
{minutes=":"+intMinutes;}if(intSeconds<10)
{seconds=":0"+intSeconds;}else
{seconds=":"+intSeconds;}timeString+="<table width=100% cellspacing=0>";timeString+="<tr><td align=center><span class=time>"+hours+minutes+seconds+" "+wday+"</span></td></tr>";timeString+="</table>";if(NSkey)
{document.clock.document.open();document.clock.document.write(timeString);document.clock.document.close();}else
{clock.innerHTML=timeString;}document.refreshTimer=setTimeout("tick();",1000);}
var intDelay=20; 
var intInterval=50; 
function MenuClick()
	{if (LayerMenu.style.display=="")
	{GradientClose();}
else
	{LayerMenu.filters.alpha.opacity=0;
	LayerMenu.style.display="";
GradientShow();
	hide("first");}}
function GradientShow()
	{LayerMenu.filters.alpha.opacity+=intInterval;
	if (LayerMenu.filters.alpha.opacity<100) setTimeout("GradientShow()",intDelay);}
function GradientClose()
	{LayerMenu.filters.alpha.opacity-=intInterval;
	if (LayerMenu.filters.alpha.opacity>0)
	{setTimeout("GradientClose()",intDelay);
	}else{LayerMenu.style.display="none";}}
function updown()
	{if (startmenu.className == "down")
	startmenu.className = "up";
	else if (startmenu.className == "up")
	startmenu.className = "up";}
function ctrl()
	{if (startmenu.className == "up")
	startmenu.className = "down";
	else if (startmenu.className == "down")
	startmenu.className = "up";}
function pop(win)
	{window.open(win,'','')}
function pw(win)
	{window.open(win,'','top=10,left=10')}
function f5(){
	if (confirm("确实要注销吗？")){document.execCommand('refresh')}}
function shut(){
	if (confirm("确实要关机吗？")){window.close()}}
function keypress()
	{if(event.keyCode==82)show('Layerdisplay');
	if(event.keyCode==84)show('date');
	if(event.keyCode==91)MenuClick();
	if(event.keyCode==17)MenuClick();
	if(event.keyCode==91)ctrl();
	if(event.keyCode==17)ctrl();
	if(event.keyCode==72)show('help');
	if(event.keyCode==27)hide('help');
	if(event.keyCode==27)hide('layerdisplay');
	if(event.keyCode==27)hide('readme')}
	document.onkeydown = keypress
function show(c_Str)
	{document.all(c_Str).style.display='block';}
function hide(c_Str) 
	{if(document.all(c_Str).style.display=='none')
	{return;}
	document.all(c_Str).style.display='none';}
 var ll,xx,yy;
function x_y(ll,xx,yy)
	{document.all(ll).style.top=xx;
	document.all(ll).style.left=yy;}
function set_ico() { 
	if (document.body.clientHeight > 560){set_ico2();}
	else if (document.body.clientHeight <= 560){set_ico1(); }
	else return(false);  }
function set_ico1()
	{x_y('ico1','15','20');
	x_y('ico2','95','20');
	x_y('ico3','175','20');
	x_y('ico4','255','20');
	x_y('ico5','335','20');
	x_y('ico6','15','100');
	x_y('ico7','95','100');
	x_y('ico8','175','100');
	x_y('ico9','255','100');
	x_y('ico10','335','100');
	x_y('ico11','15','180');
	x_y('ico12','95','180');
	x_y('ico13','175','180');
	x_y('ico14','255','180');}
function set_ico2()
	{x_y('ico1','15','20');
	x_y('ico2','95','20');
	x_y('ico3','175','20');
	x_y('ico4','255','20');
	x_y('ico5','335','20');
	x_y('ico6','15','100');
	x_y('ico7','95','100');
	x_y('ico8','175','100');
	x_y('ico9','255','100');
	x_y('ico10','335','100');
	x_y('ico11','415','20');
	x_y('ico12','495','20');
	x_y('ico13','415','100');
	x_y('ico14','495','100');}
function test()
	{alert("\n系统信息检测结果如下：\n\n浏览器: "+navigator.appName+"\n版本号: "+navigator.appVersion+"\n代码名字: "+navigator.appCodeName+"\n分辨率:" +screen.width+"×"+screen.height+"\n显示色彩:"+window.screen.colorDepth+"位真彩色" );}
function cs(nh)
	{css.href=nh;}
function finish()
	{hide("load");show('first');window.status="..::Welcome to 518.com::.."}
function showmenuie5(){
	var rightedge=document.body.clientWidth-event.clientX-100
	var bottomedge=document.body.clientHeight-event.clientY-25
if (rightedge<ie5menu.offsetWidth)
	ie5menu.style.left=document.body.scrollLeft+event.clientX-ie5menu.offsetWidth;
else
	ie5menu.style.left=document.body.scrollLeft+event.clientX
if (bottomedge<ie5menu.offsetHeight)
	ie5menu.style.top=document.body.scrollTop+event.clientY-ie5menu.offsetHeight
else
	ie5menu.style.top=document.body.scrollTop+event.clientY
	ie5menu.style.visibility="visible"
return false}
function hidemenuie5(){
	ie5menu.style.visibility="hidden"}
function ico2k()
	{startmenu.src ="xp/start2k.gif";
	start_pro.src ="xp/s_pro2k.gif";
	start_doc.src ="xp/s_doc2k.gif";
	start_fav.src ="xp/s_fav2k.gif";
	start_set.src ="xp/s_set2k.gif";
	start_find.src ="xp/s_find2k.gif";
	start_help.src ="xp/s_help2k.gif";
	start_logoff.src ="xp/s_logoff2k.gif";
	update.src ="xp/s_update2k.gif";
	start_shut.src ="xp/s_shut2k.gif";
	shut.src ="xp/close.gif";}
function icoxp()
	{startmenu.src ="xp/startxp.gif";
	 start_pro.src="xp/start_pro.gif";
	start_doc.src ="xp/start_doc.gif";
	start_fav.src ="xp/start_fav.gif";
	start_set.src ="xp/start_set.gif";
	start_find.src ="xp/start_find.gif";
	start_help.src ="xp/start_help.gif";
	start_logoff.src ="xp/start_logoff.gif";
	start_shut.src ="xp/start_shut.gif";
	update.src ="xp/start_update.gif";
	shut.src ="xp/closexp.gif";}
function about(){
	showModelessDialog("xp/about.htm",window,"status:no;dialogWidth:341px;dialogHeight:195px");
}