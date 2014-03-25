# general functions for hylafax module

do '../web-lib.pl';
&init_config();
require '../ui-lib.pl';

$HOST_NAME=get_system_hostname(); 
$HYLA_DIR=$config{'spool_path'};
$HYLA_CONF=$config{'conf_path'};
$hostfile=$HYLA_DIR."/etc/hosts.hfaxd";
$HOMESITE="www.tecchio.net";
$HOMEPAGE="webmin/hylafax";

sub hylacheck
{
return(-1) unless `ps -A | grep faxq`;
return(-1) unless `ps -A | grep hfaxd`;
return(1);
}

sub archcheck
{
my $ok=1, @dirs=('archive','log','info');
foreach (@dirs)
    { $ok=0 unless -d "$HYLA_DIR/$_"; }
return $ok;
}

sub start
# start the hylafax server
{
print $text{start_hylafax}, "... ";
&error_setup($text{'start_err'});
$temp = &tempname();
$rv = &system_logged("($config{'start_cmd'}) >$temp 2>&1");
$out = `cat $temp`; unlink($temp);
if ($rv) {
	&error("<pre>$out</pre>");
	}
sleep(3);
&webmin_log("start"); print "OK! ";
}

sub stop
# stop the hylafax server
{
print $text{stop_hylafax}, "... ";
if ($config{'stop_cmd'}) {
	$out = &backquote_logged("$config{'stop_cmd'} 2>&1");
	}
&error_setup($text{'stop_err'});
if ($?) {
	&error("<pre>$?\n$out</pre>");
	}
&webmin_log("stop"); print "OK! ";
}

sub restart
{ &stop; &start; }	

sub faxstat
# get the hylafax status
{ 
my @status=split /\n/, `faxstat`; 
print "<TABLE><TR VALIGN=TOP><TD><SMALL>", shift @status, "</SMALL></TD> <TD WIDTH=20></TD>\n",
    "<TD><SMALL>", (join "<BR>", @status), "</SMALL></TD> <TD WIDTH=20></TD>\n",
    "<TD VALIGN=MIDDLE><FORM><INPUT TYPE=BUTTON VALUE=\"", $text{'recheck'}, 
    "\" onClick='location.href=location.href'></FORM></TD>\n</TR></TABLE>";
}


sub faxqueue
# get a hylafax queue (send, done, received)
# args: param - s, d, or r
{
my $param=shift;
@lines=split(/\n/,`faxstat -l$param`);
while (shift @lines) {}; shift @lines;
# bugfixed by Carl Pulley
@return=();
$flag=1;
while (($value = shift @lines) && $flag == 1) 
    {
    if ($value =~ /^Trying [\-_a-zA-Z0-9\.]+ \([0-9\.]+\) at port [0-9]+\.\.\./) 
        { $flag = 0; } 
    else 
        { push(@return, $value); }
    }
return @return;
}

sub getModems
{
#count the modems from file config.* 
my $filelist=`ls $HYLA_DIR/etc/config.*`;
my @configs=split('\n',$filelist);
my @modems=();
foreach $conf (@configs)
	{ 
	@path=split('\.',$conf); 
	push @modems, $path[1] unless $path[1] eq "sav"; 
	}
return @modems;	
}

sub trim 
{
# a trim function 
my $string = shift;
for ($string) 
	{
	s/^\s+//;
	s/\s+$//;
	}
return $string;
}

sub quot
{
# trim spaces and quote a string if has blanks
my $item=shift; $item=trim($item);
$item='"'.$item.'"' if index($item," ")>0;
return $item;
}

sub outLang
{
# return a translation from a language, if exists; othervise return the string itself
my $item=shift; $chk=$item;
$chk =~ s/\s/_/gi;
if ($text{$chk}) { return $text{$chk}; }
elsif ($text{lc($chk)}) { return $text{lc($chk)}; }
else { return $item; }
}

sub getFmt
{
# get the format codes for queues output
# args: job (J or R), field to extract (code,key,title,size,descr)
my ($job,$field)=@_; 
my @FMT=();
my $fmtkey=($job eq 'J')? 'JobFmt' : 'RcvFmt';
my $fmt=`cat $HYLA_CONF/hyla.conf | grep -E ^$fmtkey`;
$fmt =~ /^$fmtkey:\s*"(.+)"/; 
foreach (split /\s+/,$1)
    {
    /%-?(\d*)\.?(\d*)(\w)/;
    $char=$3;
    if ($field eq 'size') { push @FMT, ($1)? $1 : $2; }
    else
        {
        foreach (@jobcodes)
            {
            ($code,$key,$title,$size,$descr)=split/;/;
            next unless $code =~ /$job/;
            push @FMT, $$field if $key eq $char;
            }
        }
    }
return @FMT;
}

sub queueItems
{
# retrieve the fields from a queue output
# args: $line - output line
# @sizes - array of field dimensions
my $line=shift;
@items=(); $n=0;
foreach $size (@_)
	{ 
	push @items, &trim(substr($line,$n,$size)); 
	$n+=($size+1);
	}
return @items;
}

sub getParams
{
foreach $myFile (@_)
	{
	open(MYFILE,$myFile);
	while(<MYFILE>)
		{
		next if /^#/;
		s/\"//g;
		if (/(\w+):\s*(.+)/)
			{ 
			@items=split('#', $2);
			$parms{$1} = trim($items[0]); 
			$comms{$1} = $items[1] if $items[1];
			}
		}
	close MYFILE;
	}
}


sub docInfo
{
# retrieve document informations from spool dir    
# patched by Carl Pulley (@fname)
my $item=shift; 
@fname=();
open INFO, "$HYLA_DIR/$item";
while (<INFO>)
    {
    chop; /^(.+):(.+)$/;
    $owner=$2 if $1 eq "owner";
    $number=$2 if $1 eq "number";
    push (@fname,$2) if index($1,"postscript")!=-1;
    }
close INFO;
return ($owner,$number,@fname);
}


sub saveConf
{
# save config files     
# arguments: $config_file, @config_parameters
my $file=shift;
my $aParam, $line;
my @lines=();
open CONF, $file;
while (<CONF>)
	{
	# correct existent parameters first
	foreach $aParam (@_)
		{
		$line=$_;
		if (/^#*\s*$aParam\s*:(.+)(#.+)*/)
			{
			if ($q->param($aParam) ne "" && !$q->param($aParam."_def")) 
				{ $line="$aParam:\t".quot($q->param($aParam))." $2\n"; }
			else				
				{ $line="#$aParam:\t$1$2\n"; }
			$q->delete($aParam); last;
			}
		}
	push @lines, $line;
	}
close CONF;	
# then add new parameters
foreach $aParam (@_)
	{
	if ($q->param($aParam) ne "" && !$q->param($aParam."_def"))
		{
		push @lines, "$aParam:\t".quot($q->param($aParam))."\n"; 
		}
	}
open CONF, ">$file";
print CONF foreach @lines;
close CONF;
}

sub slash
# return a 'backslashed' string, unless:
# a) the string is a complete IP address;
# b) the string is a name without special characters
{
my $str=shift;
return $str if $str =~ /^(\d{1,3}\.){3}\d{1,3}$/;
return $str if $str =~ /^\w+$/;
$str =~ s/\./\\\./gi;
$str =~ s/\\\\\./\\\./gi;
return $str;
}

sub unslash
# strip the backslashes from a string
{
my $str=shift;
$str =~ s/\\|\^//gi;
return $str;
}

sub delHostRow
{
# delete a row from hosts.hfaxd
my $row=shift;
$cmd=`cat $hostfile | grep -vF '$row'`;
open HOST, ">$hostfile";
print HOST $cmd;
close HOST;
&webmin_log($text{'conf_hosts'});
}	

1;
