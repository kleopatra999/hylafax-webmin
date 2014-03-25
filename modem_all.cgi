#!/usr/bin/perl
# modem_all.cgi
# Manage the general configurations

use CGI;
require './hylafax-lib.pl';
require './config_array.pl';
require './jobcodes.pl';
require './escapes.pl';

&ui_print_header(undef,$text{'conf_general'},undef);

$q=new CGI;
if ($q->param("restart")) { &stop; &start; }

&faxstat;

sub PageSize
{
my $value=shift;
%options=();
open PAGES, "$HYLA_CONF/pagesizes";
while (<PAGES>)
	{
	next if /^#/;	
	my @elems=split ' ';
	$text=""; $key=undef;
	while (@elems)
		{
		$elem=pop @elems;
		next if $elem =~ /^\d+$/;
		if (!$key) { $key=$elem; }
		else { $text=$elem." ".$text; }
		}
	$text=&trim($text); $key=&trim($key);	
	next unless ($text && $key);
	if ($text ne "default") { $options{lc($key)}=$text; }
	else { $default=lc($key); }
	}
close PAGES;
$value=$default unless $value;
print "<select name=PageSize>\n";
foreach $k (sort(keys %options)) 
	{	
	print "<option value=$k";
	print " selected" if $k eq $value;
	print ">", $options{$k}, "</option>\n";
	}
print "</select>\n";	
}

sub VRes 
{
my $value=shift;
@high=(196, $text{'high'}); @low=(98,$text{'low'}); @options=(\@low, \@high);
print &ui_radio("VRes",$value, \@options);
}

sub displFmt
{
my ($job,$value)=@_;   
foreach (@jobcodes)
    {
    ($code,$key,$text,$size,$descr)=split/;/;
    if ($code =~ /$job/)
        {
        $descr =~ s/\s+/&nbsp;/g;
        print "<input type=checkbox name=", $job, "Fmt value=$key";
        print " checked" if index($value,$key)>0;
        print ">$descr\n";
        }
    }
}

sub JobFmt
{ displFmt 'J',shift; }

sub RcvFmt
{ displFmt 'R',shift; }

sub setJobFmt
{
my $job=shift, $strFmt="";
my $keymust=($job eq 'J')? 'j' : 'f';
my $keyname=($job eq 'J')? 'JobFmt' : 'RcvFmt';
foreach (@jobcodes)
    {
    ($code,$key,$text,$size,$descr)=split/;/;
    if ($code =~ /$job/)
        {
        if ($key eq $keymust) { $strFmt.="%$size$key "; }
        else
            { 
            foreach $item ($q->param($job."Fmt"))
                { $strFmt.="%$size$key " if $item eq $key; }    
            }
        }
    }
$q->param(-name=>$keyname,-value=>$strFmt);
}

sub DateFormat
{
my $value=shift;
print "<input size=35 name=DateFormat value=\"$value\"> \n<I>", 
	$text{add_an_item}, ":</I> ",
	"<select onChange=insert(this)>\n<option></option>\n";
foreach $item (@strftime)
	{
	$key=substr($item,0,1);
	if ($key eq "-") { print "<option>$item</option>\n"; }
	else 
		{ 
		$item =~ s/\s/_/gi;
		print "<option value='%$key'>"; 
		if ($text{substr($item,2)}) { print $text{substr($item,2)} }
		else {print substr($item,2)}
		print "</option>\n"; 
		}
	}
print "</select>";	
}

if ($q->param("update"))
	{
    setJobFmt('J') if $q->param("JFmt");
    setJobFmt('R') if $q->param("RFmt");
	$q->param(-name=>"DateFormat",-value=>'"'.$q->param("DateFormat").'"') if $q->param("DateFormat");
	&saveConf("$HYLA_CONF/hyla.conf", @hylaParams);
	&saveConf("$HYLA_DIR/etc/config", @commParams);
	$restart=1;
	}

%parms=(); %comms=(); 
getParams("$HYLA_CONF/hfaxd.conf", "$HYLA_CONF/hyla.conf", "$HYLA_DIR/etc/config");

@aParams=();
foreach $aParam (@hylaParams) { push @aParams, $aParam; } 
foreach $aParam (@commParams) { push @aParams, $aParam; } 

$title=$text{'conf_general'};
require './config_form.pl';

print <<JS;
<SCRIPT>
function insert(c)
{
f=c.form; v=c.options[c.selectedIndex].value;
if (v.length==2) f.DateFormat.value+=v; 
}
</SCRIPT>
JS

