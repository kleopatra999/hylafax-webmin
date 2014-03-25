#!/usr/bin/perl
# modems.cgi
# Display the icons for Modems configuration

require './hylafax-lib.pl';

&ui_print_header("",$text{'conf_modems'}, "");
&faxstat;

foreach $modem (&getModems)
	{
	push @icon_array, "images/modem.jpg";
	push @link_array, "modem_one.cgi?modem=$modem";
	push @title_array, $modem;
	}

&icons_table(\@link_array,\@title_array,\@icon_array);
&ui_print_footer("config.cgi", $text{'config'}, "index.cgi", $text{'index_title'});
