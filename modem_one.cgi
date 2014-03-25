#!/usr/bin/perl
# modem_one.cgi
# Manage the configuration for one modem

use CGI;
require './hylafax-lib.pl';
require './config_array.pl';
$q=new CGI;

&ui_print_header(undef,$text{'modem'}." ".$q->param('modem'),undef);
&faxstat;

%parms=(); %comms=(); 
getParams("$HYLA_DIR/etc/config");
while (($k,$v)=each %parms) { $defaults{$k}=$v; }

if ($q->param("update"))
	{
	while (($k,$v)=each %parms)
		{
		if ($q->param($k) eq $v)
			{
			$q->param(-name=>$k,-value=>"");
			$q->param(-name=>$k."_def",-value=>1);
			}
		}
	if ($q->param("left") || $q->param("center") || $q->param("right"))
		{
		$tag=$q->param("left")."|".$q->param("center")."|".$q->param("right");
		$q->param(-name=>"TagLineFormat",-value=>$tag);
		}
	&saveConf("$HYLA_DIR/etc/config.".$q->param('modem'), @modemParams);
	}

sub SpeakerVolume
{ 
my $value=shift;
my $default=shift;
$value=$default unless $value;
my @options=("high", "medium", "low", "quiet", "off"); 
print "<SELECT NAME=SpeakerVolume>\n";
foreach $opt (@options) 
	{ 
	print "<OPTION VALUE=$opt";
	print " SELECTED" if $value eq $opt;
	print ">", $text{$opt}, "</OPTION>\n";
	}
print "</SELECT>\n";
}

sub TagLineFormat
{ 
my $value=shift;
my $default=shift;
my $item;
$value =~ /(.+)\|(.+)\|(.+)/;
$stropt="";
require './escapes.pl';
foreach $item (@hylaserv)
	{
	$key=substr($item,0,1);
	if ($key eq "-") { $stropt.="<option value=0>$item</option>\n"; }
	else { $stropt.="<option value='%%$key'>".&outLang(substr($item,2))."</option>\n"; }
	}
$stropt.="<option>- - - -</option>\n";	
foreach $item (@strftime)
	{
	$key=substr($item,0,1);
	if ($key eq "-") { $stropt.="<option value=0>$item</option>\n"; }
	else { $stropt.="<option value='%$key'>".&outLang(substr($item,2))."</option>\n"; }
	}		
print "<TABLE><TR><TD>", $text{'left'}, "</TD> <TD> ",
	"<INPUT NAME=left VALUE=\"", $1,  "\"></TD>\n<TD><i>", $text{"add an item"}, 
	"</i> <select onChange=\"insert(this,'left')\">\n<option></option>\n", $stropt, "</select>",
	"</TD>\n</TR> <TR>\n<TD>", $text{'center'}, "</TD>\n<TD>",  
	"<INPUT NAME=center VALUE=\"", $2, "\"></TD>\n<TD><i>", $text{"add an item"},
	"</i> <select onChange=\"insert(this,'center')\">\n<option></option>\n", $stropt, "</select>",
	"</TD>\n</TR> <TR>\n<TD>", $text{'right'}, "</TD>\n<TD>",
	"<INPUT NAME=right VALUE=\"", $3, "\"></TD>\n<TD><i>", $text{"add an item"},
	"</i> <select onChange=\"insert(this,'right')\">\n<option></option>\n", $stropt, "</select>",
	"</TD>\n</TR></TABLE>";
}

getParams("$HYLA_DIR/etc/config.".$q->param('modem'));
@aParams=();
foreach $aParam (@modemParams) { push @aParams, $aParam; } 
$title=$text{'config'}.": ".$text{'modem'}." ".$q->param('modem');
require './config_form.pl';

print <<JS;
<SCRIPT>
function insert(c,fld)
{
f=c.form; v=c.options[c.selectedIndex].value;
if (v.length>=2) f.elements[fld].value+=v; 
}
</SCRIPT>
JS
