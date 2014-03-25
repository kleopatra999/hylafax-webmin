#!/usr/bin/perl
# hosts.cgi
# Display and manage the Hosts allowed to connect

require './hylafax-lib.pl';
&ReadParse();
&ui_print_header(undef,$text{'conf_hosts'}, "", "hosts");

if ($in{del}) 
    { delHostRow(slash($in{del})); }

&faxstat;

print "<FORM ID=hosts METHOD=POST ACTION=hosts.cgi>
    <INPUT TYPE=HIDDEN ID=del NAME=del>";
print "<TABLE BORDER=1 CELLPADDING=2><CAPTION><B>", $text{'conf_hosts_title'}, ":</B></CAPTION>",
	"<TR $cb><TH $tb></TH><TH>", $text{rule}, "</TH><TH>", $text{user}, "</TH><TH>", $text{from}, "</TH><TH>", $text{passwd}, 
	"</TH><TH>", $text{adminwd}, "</TH></TR>";
@lines=();	
open HOST, $hostfile or die $hostfile.$text{'not_found'}; 
while (<HOST>)
    { chop; next unless $_; push @lines, $_; }
close HOST;

foreach (sort @lines)
	{
	$op="";
	if (substr($_,0,1) eq "!")
		{
		$op="!";
		$_=substr($_,1);
		}
	($host,$x,$passwd,$adminwd)=split /:/;
	$host=unslash($host);
	if ($host =~ /\@/) { ($user,$host)=split /\@/,$host; }
	else { $user=''; }	

	print "<TR><TD $tb>
	    <INPUT TYPE=BUTTON VALUE='", $text{delete}, "' onClick='delRow(\"$op$_\")'>
	    <INPUT TYPE=BUTTON VALUE='", $text{modify}, "' onClick='edRow(\"$op$_\")'>
        </TD>\n<TD NOWRAP>",
        ($op eq '!')? $text{deny} : $text{allow},
        "</TD>\n<TD>",
        ($user)? $user : $text{all}, 
        "</TD>\n<TD>",
        ($host)? $host : $text{all}, 
        "</TD>\n<TD>",
        ($passwd)? $passwd : '&nbsp;',
        "</TD>\n<TD>",
        ($adminwd)? $adminwd : '&nbsp;',
		"</TD></TR>\n"; 
	}

print "</TABLE> <INPUT TYPE=BUTTON VALUE='", $text{new_rule}, "' onClick=edRow()> </FORM>";

&ui_print_footer("config.cgi", $text{'config'}, "index.cgi", $text{'index_title'});

print <<JS;
<SCRIPT>
function delRow(c)
{ 
document.getElementById('del').value=c;
document.getElementById('hosts').submit();
}

function edRow(c)
{ 
url="edit_hosts.cgi";
if (c) url+="?row="+c;
location.href=url;
}
</SCRIPT>
JS
