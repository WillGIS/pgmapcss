#!/usr/bin/perl

$DB=$ENV{DB};
$DBUSER=$ENV{DBUSER};
$DBPASS=$ENV{DBPASS};
$DBHOST=$ENV{DBHOST};
$BASE=$ENV{BASE};
$STYLE_ID=$ENV{STYLE_ID};

%error_keys = ();

# possible_values: return list of all possible values for a key
sub possible_values {
  my $key = $_[0];
# TODO: escape characters
  my @ret = ();

  my $v;
  my $r;
# TODO: user/pass/host parameters for psql
  open $v, "psql -d \"dbname=$DB user=$DBUSER host=$DBHOST password=$DBPASS\" -t -A -c \"select (CASE WHEN value is null THEN 'NULL' ELSE value END) from (select key, unnest(cast(value as text[])) as value from each((${STYLE_ID}_stat()).properties_values)) t where key='$key';\"|";
  while($r = <$v>) {
    chop($r);
    push @ret, $r;
  }

  return @ret;
}

# now process test-template.mapnik and replace COLOR placeholders by colors
open $f, "<${BASE}-template.mapnik";
open $r, ">${STYLE_ID}.mapnik";
while (<$f>) {
  if (m/^# FOR (.*)$/) {
    @keys = split " ", $1;
    @t = ();
    while (<$f>) {
      if (m/^# END/) {
	last;
      }

      push @t, $_;
    }

    foreach $key (@keys) {
      @res = ();

      foreach $value (possible_values($key)) {
	if ($value eq 'NULL') {
	}
	elsif ($value eq '*') {
	  $error_keys{$key} = 1;
	}
	else {
	  foreach $row (@t) {
	    my $r1 = $row;
	    $r1 =~ s/\[$key\]/$value/;
	    push @res, $r1;
	  }
	}
      }

      @t = @res;
    }

    print $r join "", @t;
  }
  else {
    $_ =~ s/DBUSER/$DBUSER/ge;
    $_ =~ s/DBPASS/$DBPASS/ge;
    $_ =~ s/DBHOST/$DBHOST/ge;
    $_ =~ s/DB/${DB}/ge;
    $_ =~ s/STYLE_ID/$STYLE_ID/ge;

    print $r $_;
  }
}
close($r);
close($f);

@error_keys = keys %error_keys;
if (@error_keys != 0) {
  print "WARNING! Some values for the following keys are calculated by an eval-statement. As pgmapcss can't guess the result of those statements some symbols might not get rendered.\n* ";
  print join("\n* ", @error_keys);
  print "\n";
}