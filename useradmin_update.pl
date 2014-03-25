$faxadd=$config{faxbin_path}.'/faxadduser';
$faxdel=$config{faxbin_path}.'/faxdeluser';

sub useradmin_create_user
{
if ($config{'synchronize'})
    {
    my $pass; 
    $pass=$_[0]->{plainpass} if $_[0]->{passmode}==3;
    if ($pass) { system "$faxadd -a $pass ".$_[0]->{user}; }
    else { system "$faxadd ".$_[0]->{user}; }
    }
}

sub useradmin_modify_user
{
if ($config{'synchronize'})
    {
    my $pass; 
    $pass=$_[0]->{plainpass} if $_[0]->{passmode}==3;
    system "$faxdel ".$_[0]->{user};
    if ($pass) { system "$faxadd -a $pass ".$_[0]->{user}; }
    else { system "$faxadd ".$_[0]->{user}; }
    }
}	

sub useradmin_delete_user
{ 
system "$faxdel ".$_[0]->{user} if $config{'synchronize'};
}

1;