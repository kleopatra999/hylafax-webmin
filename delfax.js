$confdel=$text{'confirm_delete'};
$confarch=$text{'confirm_archive'};
print <<JS;
<SCRIPT>
function delfax(n)
{ if (confirm("$confdel")) { document.forms[1].rm.value=n; document.forms[1].submit(); }}

function archfax(n)
{ if (confirm("$confarch")) location.href="faxarchive.cgi?ID="+n+"&q=$QTITLE"; }
</SCRIPT>
JS

1;