#!/usr/bin/perl
# hosts.cgi
# Display and manage the Hosts allowed to connect

# ui_opt_textbox(name, value, size, option1, [option2])
# Returns HTML for a text field that is optional
sub my_ui_opt_textbox
{
return &theme_ui_opt_textbox(@_) if (defined(&theme_ui_opt_textbox));
local ($name, $value, $size, $opt1, $opt2) = @_;
local $dis1 = &js_disable_inputs([ $name, @$extra ], [ ]);
local $dis2 = &js_disable_inputs([ ], [ $name, @$extra ]);
local $rv;
$rv .= "<input type=radio name=\"".&quote_escape($name."_def")."\" ".
       "value=1 ".($value eq '' ? "checked" : "").
       " onClick='$dis1'> ".$opt1."\n";
if ($opt2)
    {
    $rv .= "<input type=radio name=\"".&quote_escape($name."_def")."\" ".
       "value=2 ".($value ne '' ? "checked" : "").
       " onClick='$dis1'> ".$opt2."\n";
    }           
$rv .= "<input type=radio name=\"".&quote_escape($name."_def")."\" ".
       "value=0 onClick='$dis2'>\n";
$rv .= "<input name=\"".&quote_escape($name)."\" ".
       "size=$size disabled=true>\n";
return $rv;
}

require './hylafax-lib.pl';
&ReadParse();
$title=($in{row})? $text{modify}.' '.$text{rule} : $text{new_rule};
&ui_print_header(undef,$title, "", "hosts");

# rewrite the hosts.hfaxd file with updated lines
if ($in{update})
	{
    delHostRow($in{row}) if $in{row};
    $row=$in{op};
    if ($in{user_def}==0)
        {
        $row.='^'.$in{user}.'@';
        $row.=$in{host} if $in{host_def}==0;
        $row=slash($row);
        }
    elsif ($in{host_def}==0)
        { $row.=slash($in{host}); }
    if ($in{passwd_def}!=1 || $in{adminwd_def}!=1)
        {
        $row.=':';
        if ($in{passwd_def}==1) { $row.=':'; }
        elsif ($in{passwd_def}==2) { $row.=':'.$in{oldpasswd}; }
        else 
            { 
            $row.=':'.crypt($in{passwd},
                join '', ('.', '/', 0..9, 'A'..'Z', 'a'..'z')[rand 64, rand 64]
                ); 
            }
        if ($in{adminwd_def}==1) { $row.=':'; }
        elsif ($in{adminwd_def}==2) { $row.=':'.$in{oldadminwd}; }
        else 
            { 
            $row.=':'.crypt($in{adminwd},
                join '', ('.', '/', 0..9, 'A'..'Z', 'a'..'z')[rand 64, rand 64]
                ); 
            }        
        }
    open HOST, ">>$hostfile";
    print HOST "$row\n";
    close HOST;
    print "<SCRIPT> location.href='hosts.cgi'; </SCRIPT>";
    exit;        
	}	

@allow=("", $text{'allow'}); @deny=("!",$text{'deny'}); @options=(\@allow, \@deny);
if ($in{row})
    {
    $op="";
	if (substr($in{row},0,1) eq "!")
		{
		$op="!";
		$in{row}=substr($in{row},1);
		}
	($host,$x,$passwd,$adminwd)=split /:/, $in{row};
	$host=unslash($host);	
	if ($host =~ /\@/) { ($user,$host)=split /\@/,$host; }
	else { $user=''; }	
	}

print "<FORM METHOD=POST>
    <TABLE $cb BORDER=1 CELLPADDING=0 CELLSPACING=0><TR><TD>
    <TABLE CELLPADDING=2>
    <TR><TD>", $text{rule}, "</TD><TD>",
        &ui_select("op$n", $op, \@options),
    "</TR>\n<TR><TD>", $text{user}, "</TD><TD>",
    	&ui_opt_textbox("user", $user, 20, $text{'all'}),     
    "</TR>\n<TR><TD>", $text{from}, "</TD><TD>", 
		&ui_opt_textbox("host", $host, 25, $text{'all'}),
    "</TR>\n<TR><TD>", $text{passwd}, "</TD><TD>
        <INPUT TYPE=HIDDEN NAME=oldpasswd VALUE=\"", $passwd, '"> ', 
        &my_ui_opt_textbox("passwd", $passwd, 20, $text{config_none}, $text{config_nochange}),
    "</TR>\n<TR><TD>", $text{adminwd}, "</TD><TD>
        <INPUT TYPE=HIDDEN NAME=oldadminwd VALUE=\"", $adminwd, '"> ',
        &my_ui_opt_textbox("adminwd", $adminwd, 20, $text{config_none}, $text{config_nochange}), 
    "</TR></TABLE></TD></TR></TABLE>
    <INPUT TYPE=SUBMIT NAME=update VALUE=\"", $text{update}, "\"> </FORM>";

&ui_print_footer("hosts.cgi", $text{conf_hosts}, "config.cgi", $text{config}, "index.cgi", $text{index_title});