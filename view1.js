function View(n)
{
h=parseInt(screen.availHeight*0.9);
w=parseInt(h*0.758)+2; 
if (window.fax) fax.close();
fax=window.open("viewfax.cgi?w="+w+"&h="+h+"&fax="+n,"fax","width="+w+",height="+h+",resizable=yes,menubar=yes,titlebar=yes");
}
