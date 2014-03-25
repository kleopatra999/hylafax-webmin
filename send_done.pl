#!/usr/bin/perl
# Display & manage the send queue

use CGI; $q=new CGI;
require './hylafax-lib.pl';
&ui_print_header(undef,$text{$QTITLE}, undef);
require './delfax.js';
require './jobcodes.pl';

print "<SCRIPT SRC=view".$config{'fit_screen'}.".js></SCRIPT>\n";

&faxstat;
if ($q->param('rm'))
	{
	$id=$q->param('rm');
    ($owner,$number,@fname)=docInfo("/$QTITLE/q$id");
	print "<BR>", `su -c "faxrm $id 2>&1" $owner`; 
	&webmin_log($text{'delete_job'}.": ".$text{$QTITLE}." ".$q->param('rm'));
	}

@lines=faxqueue($QPAR);
@titles=getFmt('J','title');
@sizes=getFmt('J','size');

if ($#lines==-1)
	{
	print "<p>", $text{'no_fax_in_queue'}, "</p>";
	}
else
	{
	%faxorder=();
	print "<FORM METHOD=POST><INPUT TYPE=HIDDEN NAME=rm>\n";
	print "<TABLE BORDER=1 CELLPADDING=2><CAPTION><B>", $text{$QTITLE}, "</B></CAPTION>\n<TR $cb>\n";
	foreach (@titles) { print "<TH>", &outLang($_), "</TH> "; }
	if ($q->param('ASC.x'))
        { $img="ASC"; $imgname="DESC"; }
    else
        { $img="DESC"; $imgname="ASC"; }
    print "\n<TH $tb> <INPUT TYPE=IMAGE SRC=images/$img.gif NAME=$imgname TITLE='",
                $text{'change_order'}, "'> </TH>\n</TR>\n";
	foreach $line (@lines)
		{
        $line =~ /^(\d+) /;
        $faxorder{$1}=$line;
		}
# sorting faxes by num
    if ($q->param('ASC.x'))
        { @sortfax = sort {$a <=> $b} (keys %faxorder); }
    else
        { @sortfax = sort {$b <=> $a} (keys %faxorder); }
        
    foreach $faxnum (@sortfax)
        {
		@items=&queueItems($faxorder{$faxnum},@sizes);
        print "<TR>\n";
# patched by Carl Pulley        
        ($owner,$number,@fname)=docInfo("/$QTITLE/q".$items[0]);
        foreach $item (@items)
		    { print "<TD>$item&nbsp;</TD> "; }
        @fname=("docq/doc".$items[0].".ps") unless $#fname >= 0;
		print "\n<TD><A HREF=\"javascript:View('";
        for $fn (0 .. $#fname) { if ($fn == 0) { print $fname[0]; } else { print ":",$fname[$fn]; } } 
        print "')\" TITLE='",
            $text{'view_fax'}, "'><IMG HSPACE=2 SRC=images/lente.gif BORDER=0></A>";
        print "<A HREF=javascript:archfax(", $items[0], ") TITLE='",
            $text{'archive_job'}, "'><IMG HSPACE=2 SRC=images/save.gif BORDER=0></A>"
                if &archcheck();
        print "<A HREF=javascript:delfax(", $items[0], ") TITLE='",
			$text{'delete_job'}, "'><IMG HSPACE=2 SRC=images/cestino.gif BORDER=0></A>",
			"</TD></TR>\n";
		}
	print "</TABLE> </FORM>\n";
	}
&ui_print_footer("index.cgi", $text{'index_title'});

1;
