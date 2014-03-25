function View(n)
{
w=parseInt(screen.availWidth*0.8);
if (w>640) w=640;
h=parseInt(screen.availHeight*0.9);
if (window.fax) fax.close();
fax=window.open("viewfax.cgi?w="+w+"&h="+h+"&fax="+n,"fax","width="+w+",height="+h+",scrollbars=yes,resizable=yes,menubar=yes,titlebar=yes");
}
