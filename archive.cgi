#!/usr/bin/perl
# Display and manage the Archive

require './hylafax-lib.pl';
use CGI; $q=new CGI;
use POSIX qw(strftime);
&ui_print_header(undef,$text{archive}, undef);
print "<SCRIPT SRC=view".$config{'fit_screen'}.".js></SCRIPT>\n";
require './delfax.js';
@titles=("JID","DateTime","owner","client","Sender","Number", "Pages", "Dials");
@items=("jobid","tts","owner","client","sender","number","npages:totpages","ndials:totdials");

&faxstat;

if ($q->param('rm'))
	{
	$id=$q->param('rm');
	print `rm -fR $HYLA_DIR/archive/$id 2>&1`;
	&webmin_log($text{'delete_fax'}.": ".$text{archive}." ".$q->param('rm'));
	}

opendir(DIR, "$HYLA_DIR/archive") || die "$!<BR>".$text{is_not_installed};
@archives = grep {!/^\./ && -d "$HYLA_DIR/archive/$_" } readdir(DIR);
closedir DIR;

if ($#archives==-1)
	{
	print "<p>", $text{'no_fax_in_archive'}, "</p>";
	}
else
	{
	print "<FORM METHOD=POST><INPUT TYPE=HIDDEN NAME=rm>\n";
	print "<TABLE BORDER=1 CELLPADDING=2><CAPTION><B>", $text{archive}, "</B></CAPTION>\n<TR $cb>\n";
	foreach (@titles) { print "<TH>", &outLang($_), "</TH> "; }
	if ($q->param('ASC.x'))
        { 
        $img="ASC"; $imgname="DESC"; 
        @archives = sort {$a <=> $b}  @archives;
        }
    else
        { 
        $img="DESC"; $imgname="ASC"; 
        @archives = sort {$b <=> $a}  @archives;
        }
    print "\n<TH $tb> <INPUT TYPE=IMAGE SRC=images/$img.gif NAME=$imgname TITLE='",
                $text{'change_order'}, "'> </TH>\n</TR>\n";
        
    foreach $JID (@archives)
        {
        @fname=(); %elems=();
        open INFO, "$HYLA_DIR/archive/$JID/q$JID";
        while (<INFO>)
            {
            chop; /^(.+):(.+)$/;
            $elems{$1}=$2;
            if (index($1,"postscript")!=-1)
                {
                $val=$2; $val =~ s/docq/archive\/$JID/;
                push (@fname,$val);
                }
            }
        close INFO;            
		print "<TR>\n";
        foreach $item (@items)
		    { 
            if ($item =~ /:/)
                {        		    
                @kys=();
                foreach $k (split (/:/, $item)) { push @kys, $elems{$k}; }
                $val = join ":",@kys;
                }
            else 
                { 
                $val=$elems{$item}; 
                if ($item eq "tts") 
                    {
                    $val = strftime "%b %e %Y %H:%M ", gmtime($val);                        
#                    ($sec,$min,$ore,$giom,$mese,$anno,$gios,$gioa,$oraleg) =
#						localtime($val);
#                   $val="$giom $mese $anno $ore:$min";
                    }    						
                }
            print "<TD>$val&nbsp;</TD>"; 
            }
        @fname=("docq/doc$JID.ps") unless $#fname >= 0;
		print "\n<TD><A HREF=\"javascript:View('";
        for $fn (0 .. $#fname) 
            { 
            if ($fn == 0) { print $fname[0]; } 
            else { print ":",$fname[$fn]; } 
            } 
        print "')\" TITLE='",
            $text{'view_fax'}, "'><IMG HSPACE=2 SRC=images/lente.gif BORDER=0></A>",
            "<A HREF=javascript:delfax($JID) TITLE='",
			$text{'delete_job'}, "'><IMG HSPACE=2 SRC=images/cestino.gif BORDER=0></A>",
			"</TD></TR>\n";
		}
	print "</TABLE> </FORM>\n";
	}
&ui_print_footer("index.cgi", $text{'index_title'});

1;
