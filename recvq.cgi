#!/usr/bin/perl
# Display and manage the Received queue

use CGI;
require './hylafax-lib.pl';
&ui_print_header(undef,$text{'recvq'}, undef);
require './delfax.js';
require './jobcodes.pl';
print "<SCRIPT SRC=view".$config{'fit_screen'}.".js></SCRIPT>\n";

&faxstat;

$q=new CGI;
if ($q->param('rm'))
	{
	$id=$q->param('rm');
	print `rm -f $HYLA_DIR/recvq/$id 2>&1`;
	&webmin_log($text{'delete_fax'}.": ".$text{'recvq'}." ".$q->param('rm'));
	}

@lines=faxqueue("r");
@titles=getFmt('R','title');
@sizes=getFmt('R','size');

if ($#lines==-1)
	{
	print "<p>", $text{'no_fax_in_queue'}, "</p>";
	}
else
	{
	%faxorder=();
	print "<FORM METHOD=POST><INPUT TYPE=HIDDEN NAME=rm>\n";
	print "<TABLE BORDER=1 CELLPADDING=2><CAPTION><B>", $text{'recvq'}, "</B></CAPTION>\n<TR $cb>\n";
	foreach (@titles) { print "<TH>", &outLang($_), "</TH> "; }
    if ($q->param('ASC.x'))
        {$img="ASC"; $imgname="DESC";}
    else
        {$img="DESC"; $imgname="ASC";}
    print "\n<TH $tb> <INPUT TYPE=IMAGE SRC=images/$img.gif VALUE=1 NAME=$imgname TITLE='",
        $text{'change_order'}, "'> </TH>\n</TR>\n";
    foreach $line (@lines)
		{        
        $line =~ /fax(\d+)\./;
	    $faxorder{$1}=$line;
	    }

# sorting faxes by num
    if ($q->param('ASC.x'))
        { @sortfax = sort {$a <=> $b} (keys %faxorder); }
    else
        { @sortfax = sort {$b <=> $a} (keys %faxorder); }
    foreach $faxnum (@sortfax)
        {
        @items = &queueItems($faxorder{$faxnum},@sizes);
        print "<TR>\n";
        foreach $item (@items)
		    { 
            print "<TD>";		        
            if ($item =~ /fax\d+/)
                {
                $fname=$item;  
                print "<A HREF=\"javascript:View('recvq/$fname')\" TITLE='", 
                    $text{'view_fax'}, "'>$fname</A>";
                }
            else {print $item;}
		    print "&nbsp;</TD> ";
		    }
		print "\n<TD> <A HREF=\"javascript:View('recvq/$fname')\" TITLE='", 
		    $text{'view_fax'}, "'><IMG HSPACE=2 SRC=images/lente.gif BORDER=0></A> ",
	        "<A HREF=\"javascript:delfax('$fname')\" TITLE='", $text{'delete_fax'},
	        "'><IMG HSPACE=2 SRC=images/cestino.gif BORDER=0></A> </TD> </TR>\n";
		}
	print "</TABLE> </FORM>\n";
    }
    
&ui_print_footer("index.cgi", $text{'index_title'});