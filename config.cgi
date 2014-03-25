#!/usr/bin/perl
# config.cgi
# Display the configuration options menu

require './hylafax-lib.pl';
&ui_print_header(undef,$text{'config'},"");
&faxstat;

@modems=&getModems;
if ($#modems==0)
	{
	$img="images/modem.jpg";
	$url="modem_one.cgi?modem=".$modems[0];
	$desc=$text{'modem'};
	}
else	
	{
	$img="images/modems.jpg";
	$url="modems.cgi";
	$desc=$text{'conf_modems'};
	}

my @icon_array=("images/settings.png",$img,"images/hosts.gif");
my @link_array=("modem_all.cgi",$url,"hosts.cgi");
my @title_array=($text{'conf_general'}, $desc, $text{'conf_hosts'});

&icons_table(\@link_array,\@title_array,\@icon_array);

&ui_print_footer("index.cgi", $text{'index_title'});
$todo=$text{'todo'};

print <<JS;
<SCRIPT>
function ToDo() {alert("$todo");}
</SCRIPT>
JS
