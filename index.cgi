#!/usr/bin/perl
#
# Copyright (C) 2005-2006
# Roberto Tecchio <roberto@tecchio.net>
# Web Site: http://www.tecchio.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA 02111-1307, USA.
#
# index.cgi
# Display the HylaFax main menu

use CGI;
require './hylafax-lib.pl';
require './jobcodes.pl';
$rpm=`rpm -q hylafax`;
@vers=split("-",$rpm);
$rpmh="HylaFAX ".$vers[1] if $vers[1];
&ui_print_header(undef,$text{'index_title'}, undef, undef, 1, 1, 0, 
	"<a href=http://$HOMESITE/$HOMEPAGE target=_BLANK>$text{'homepage'}</a>",
	undef, undef, $rpmh);
# Check if it is installed and the config files exist
$err="";

@files=("hfaxd.conf", "pagesizes");
foreach $file (@files)
	{
	$file="$HYLA_CONF/$file";
	$err.=$file." ".$text{'not_found'}."<br />" if !-R $file; 
	}
	
$err.="faxstat ".$text{'not_found'}."<br />" if !`faxstat 2>&1`;

if ($err)
	{	
	print "<TABLE width=100% CELLPADDING=8><TR><TD>$err",$text{'is_not_installed'},".</TD>\n";
	}
else
	{
	$q=new CGI;
# execute actions
	@names=$q->param;
	foreach $name (@names) { &$name;  }
	
# check the output format strings	
    $jok=0; $rok=0;
    foreach (getFmt('J','key')) { $jok=1 if $_ eq 'j'; }
    if (!$jok)     
        {
	    $q->param(-name=>"JobFmt",-value=>'%-5j %1a %15o %-15.15e %5P %5D %5i %7z %.25s');
	    &saveConf("$HYLA_CONF/hyla.conf", ("JobFmt"));
	    $q->delete('JobFmt');	    
        }
    foreach (getFmt('R','key')) { $rok=1 if $_ eq 'f'; }
    if (!$rok)     
        {
	    $q->param(-name=>"RcvFmt",-value=>'%7o %-10t %-15s %-20f %5p %1z %-40e');
	    &saveConf("$HYLA_CONF/hyla.conf", ("RcvFmt"));
	    $q->delete('RcvFmt');
        }        
# check if is it running 
	if(&hylacheck() != 1)
		{
		print "<p>", $text{'is_not_running'}, " ", $HOST_NAME, "</p>";
		print "<TABLE width=100%><TR><TD><form method=post><input type=hidden name=start value=1><br />\n";
		print '<input type=submit value="', $text{'start_hylafax'}, '"></td>';
		print "</form></TD>\n";
		$err=1;
		}
    elsif ($rok+$jok < 2) { &restart; }
	}

# show the icons
if (!$err)
	{	
	&faxstat;
	@icon_array=("images/config.gif","images/sendq.gif","images/doneq.gif","images/recvq.gif");
	@link_array=("config.cgi","sendq.cgi","doneq.cgi","recvq.cgi");
	@title_array=($text{config}, $text{sendq}, $text{doneq}, $text{recvq});
	$cols=4;
	
	if (&archcheck())
	    {
	    $cols=5;
	    push @icon_array, "images/archivio.jpg";
	    push @link_array, "archive.cgi";
	    push @title_array, $text{archive};
	    }

	&icons_table(\@link_array,\@title_array,\@icon_array,$cols);

	print "<TABLE width=100%><TR><TD><form method=post><input type=hidden name=stop value=1>\n";
	print "<input type=submit ","value=\"$text{'stop_hylafax'}\"></td>\n";
	print "</form></TD>\n";
	}

print "<TD ALIGN=RIGHT><I>mod. ",$module_name, " ", $module_info{version}; 
if ($config{chkupdate})
	{
	&http_download($HOMESITE, 80, "/$HOMEPAGE/lastrelease.php", "/tmp/lastversion", \$errhttp);
	unless($errhttp)
		{
		$last=`cat /tmp/lastversion`;
		print " - <a href=http://$HOMESITE/$HOMEPAGE target=_BLANK>$text{'new_release'} $last</a>" if $last > $module_info{version};
		unlink "/tmp/lastversion";
		}
	}
print "</I></TD></TR></TABLE>\n";

&ui_print_footer("/", $text{'index'});