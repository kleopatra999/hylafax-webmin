#!/usr/bin/perl
# Display a fax in TIFF or PS format
# requires ImageMagick
# patched by Carl Pulley 

use CGI;
require './hylafax-lib.pl';

$q=new CGI;

$n=0;
if (!$q->param('n')) { 
  &webmin_log($text{'view_fax'}." ".$q->param('fax')); 
} else {
  $n=$q->param('n');  
}

print $q->header(-type=>'text/html', -expires=>'-1d',
	-Cache-Control=>'no-store, no-cache, must-revalidate',
	-Cache-Control=>'post-check=0, pre-check=0',
	-Pragma=>'no-cache');

@fname=split(/:/,$q->param('fax'));
$curpage=$n;
@curpath=();
@curpages=();
$maxpages=0;
foreach $fn (@fname) 
    {
    @path=split(/\//,"$HYLA_DIR/h$fn");
    @pages=();
    @lines=split(/\n/,`identify $HYLA_DIR/$arch$fn`);
    foreach $line (@lines) 
        {
        @prop=split(/\s/,$line);
        if (index($prop[0],$path[$#path])!=-1) 
            {
            push @pages, $prop[0];
            $type=$prop[1];
            $dim=$prop[2];
            }
        }
    if (!$curfname) 
        {
        if ($curpage <= $#pages) 
            {
            $curfname=$fn;
            $curtype=$type;
            $curdim=$dim;
            @curpages=@pages;
            @curpath=@path;
            } 
        else 
            {
            $curpage=$curpage-$#pages-1;
            }
        }
    $maxpages=$maxpages + $#pages + 1;
    }

print "<STYLE> body { margin: 0px; } </STYLE>\n";

print $q->start_html($curfname);
$hminus=0;
if (!$curdim) { print $text{'unable_to_identify'}; }  
else {
	if ($maxpages>0)
		{
		$hminus=22;
		$curfname.="[$curpage]";
		print "<TABLE><TR><TD>", $text{Page}, " ", $n+1, "/", $maxpages, "</TD><TD>",
	"<A HREF=javascript:ToPage(0)><IMG HSPACE=2 BORDER=0 SRC=images/first.gif TITLE=",$text{'first_page'},"></A>\n",
	"<A HREF=javascript:ToPage(", $n-1, ")><IMG HSPACE=2 BORDER=0 SRC=images/prev.gif TITLE=",$text{'prev_page'},"></A>\n",
	"<A HREF=javascript:ToPage(", $n+1, ")><IMG HSPACE=2 BORDER=0 SRC=images/next.gif TITLE=",$text{'next_page'},"></A>\n",
	"<A HREF=javascript:ToPage(", $maxpages-1, ")><IMG HSPACE=2 BORDER=0 SRC=images/last.gif TITLE=",$text{'last_page'},"></A>\n",
		"</TD></TR></TABLE>\n" if $maxpages>1;
		}
	@size=split(/x/,$curdim);
	$size[1]*=$config{'fax_size'} if $curtype eq "TIFF";
#	print "orig: $size[0]  x $size[1]; ";
#	print "screen: ", $q->param('w'), " x ", $q->param('h'), "; ";
	if ($config{'fit_screen'})
		{
		$h=$q->param('h')-$hminus;
		$w=int(($q->param('h')-$hminus)*$size[0]/$size[1]);
		}
	elsif ($q->param('w')<$size[0])
		{
		$w=$q->param('w');
		$h=int($size[1]/$size[0]*$w);
		}
	else { $w=$size[0]; $h=$size[1]; }
	$geo="-geometry $w"."x$h!";
#	print $geo;
	$image=$curfname.$curpage; $image =~ s/[\/\.0]//g;
	$image="images/$image.jpeg";
#cjp: perform conversion based on $config settings
	$res=`rm -f $module_root_directory/images/*.jpeg; convert $geo $HYLA_DIR/$curfname $module_root_directory/$image`;
	print "<IMG SRC=$image TITLE='fax: ", $curfname, "'>";
	}
print "</CENTER>", $q->end_html;
$h+=$hminus;
print "<SCRIPT>
self.focus();
w=$w+30; h=$h+50;
if (w>screen.availWidth*0.9) w=screen.availWidth*0.9;
if (h>screen.availHeight*0.98) h=screen.availHeight*0.98;
window.resizeTo(w,h);

function ToPage(n)
{
if (n==$n || n<0 || n>=$maxpages) return;
location.href='viewfax.cgi?w=", $q->param('w'), "&h=", $q->param('h'), 
	"&fax=", $q->param('fax'), "&n='+n;
}
</SCRIPT>";
