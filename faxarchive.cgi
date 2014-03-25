#!/usr/bin/perl
# Archive a job from doneq

require './hylafax-lib.pl';
&ReadParse();
&ui_print_header(undef,$text{archive}, undef);

if ($in{ID})
    {
    print &text('archiving_job',$in{ID});
    $ARCH="$HYLA_DIR/archive/$in{ID}"; 
    system "mkdir $ARCH; chmod 0700 $ARCH; chown uucp:uucp $ARCH";
    ($owner,$number,@fname)=docInfo("/$in{q}/q$in{ID}");
    system "cp $HYLA_DIR/$in{q}/q$in{ID} $ARCH/q$in{ID}";
    foreach (@fname) 
        { 
        $fdest = $_; $fdest =~ s /docq//;
        system "cp $HYLA_DIR/$_ $ARCH$dest";
        }
    $info=(split /\n/, `ls -t $HYLA_DIR/info/$number`)[0];
    system "cp $info $ARCH/$number" if $info;
    foreach (split /\s+/,`ls $HYLA_DIR/log`) 
        { 
        if (`cat $HYLA_DIR/log/$_ | grep 'JOB $in{ID}'`)
            { system "cp $HYLA_DIR/log/$_ $ARCH/$_"; }
        }
    
    &webmin_log(&text('archiving_job',$in{ID}));
    print "<BR>", `su -c "faxrm $in{ID} 2>&1" $owner`;
    print "<BR>", `su -c "faxrm $in{ID} 2>&1" $owner` if $in{q} eq "sendq";  
    &webmin_log($text{'delete_job'}.": ".$text{$in{q}}." ".$in{ID});
    &ui_print_footer("$in{q}.cgi", $text{$in{q}}, "archive.cgi", $text{archive});
    }
else
    { print "<SCRIPT> location.href='index.cgi'; </SCRIPT>"; }
