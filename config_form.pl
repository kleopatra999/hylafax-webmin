# parameter configuration form

print "<FORM METHOD=POST>\n";
print "<INPUT TYPE=HIDDEN NAME=modem VALUE=", $q->param('modem'), ">" if $q->param('modem');
print "<TABLE CELLPADDING=2 BORDER=1><CAPTION><B>$title</B></CAPTION>";
foreach $aParam (@aParams)
	{
	$help=0; 
	print "<TR $cb>\n<TD>";
	if ($comms{$aParam}) 
		{
		$help=1;
		print '<A HREF=javascript:alert("', $text{$comms{$aParam}}, '">';
		}
	print $text{$aParam};
	print "</A>" if $help;
	print "</TD>\n<TD>";
	$def=$defaults{$aParam};
	$type=$types{$aParam};
	$strdef="default: ".&outLang($def);
	$parms{$aParam}="" if $parms{$aParam} eq $def."";
	SWITCH: 
		{
		if ($type eq "F")
			{ 
			&$aParam($parms{$aParam},$def); 
			last SWITCH; 
			}
		if ($type eq "N")
			{
			print &ui_opt_textbox($aParam, $parms{$aParam}, "6 onBlur=IsInt(this)", $strdef, $text{'custom'});
			last SWITCH; 			
			}
		if ($type eq "T")
			{
			print &ui_textbox($aParam, $parms{$aParam}, 25);
			last SWITCH; 			
			}
		print &ui_opt_textbox($aParam, $parms{$aParam}, 25, $strdef, $text{'custom'});
		}
	print "</TD>\n</TR> ";
	}
print "</TABLE><INPUT TYPE=SUBMIT NAME=update VALUE=\"", $text{'update'}, "\">";
print "&nbsp;&nbsp;<INPUT TYPE=SUBMIT NAME=restart VALUE=\"", $text{'restart_hylafax'}, "\">" if $restart;
print "</FORM>";
		
&ui_print_footer("config.cgi", $text{'config'}, "index.cgi", $text{'index_title'});

$onlyInt=$text{'numbers_only'};
print <<JS;
<SCRIPT>
function IsNum(v)
{ if (v.value && isNaN(v.value))
        {
        alert("$onlyInt.");
        location.href=location.href;
        }
 else return true;
}

function IsInt(c)
{ if (IsNum(c)) { c.value=parseInt(c.value*1); return true; }}
</SCRIPT>
JS

1;
