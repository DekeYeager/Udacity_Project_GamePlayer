#!/bin/perl
print "Greetings, small planet!\n";

#open the file
open(INFILE, "<game_agent.py") or die "Cannot open game_agent.py\n";
@lines = <INFILE>;
close INFILE;
#
open (STDOUT, ">game_agent.py") or die "Can't reopen game_agent.py!\n";
#
##create some random weights
$value11 = 10.0 - rand(20);
$value12 = 10.0 - rand(20);
$value13 = 10.0 - rand(20);
$value21 = 10.0 - rand(20);
$value22 = 10.0 - rand(20);
$value23 = 10.0 - rand(20);
$value31 = 10.0 - rand(20);
$value32 = 10.0 - rand(20);
$value33 = 10.0 - rand(20);

#printf ("\n%.1f, %.1f, %.1f", $value1, $value2, $value3);
edit_weights();

##close the file
##Finish up
close STDOUT;

#randomly choose weights between -10.0 to 10.0
#inject game_agent.py with the new weights
#change timeout to much longer for weight development
LOOP:
##    run tournament.py
     system ("python tournament.py > score.out");
#
##    display and save the winner and his score
     open(INFILE, "score.out") or die "Cannot open score.out\n";
     @scorelines = <INFILE>;
     close INFILE;

     foreach $line ( @scorelines ) 
     {
         system("echo $line >> results.txt");
         ##Win Rate:      72.9%        74.3%        77.1%        67.1%
         #if ($line =~ /(Win Rate: .*)(\d+.\d+%)(\d+.\d+%)(\d+.\d+%)(\d+.\d+%)/)
         if ($line =~ /(Win Rate:\W*)([\d]+.[\d]+)(%\W*)([\d]+.[\d]+)(%\W*)([\d]+.[\d]+)(%\W*)([\d]+.[\d]+)(%\W*)/)
         {
             #print("\n2 ".$2);
             #print("\n3 ".$4);
             #print("\n4 ".$6);
             #print("\n5 ".$8);

             if( ($2 > $4) && ($2 > $6) && ($2 > $8) )
             {
                system("echo n1 is the winner with score $2! >> results.txt");
                $value11 = 10.0 - rand(20);
                $value12 = 10.0 - rand(20);
                $value13 = 10.0 - rand(20);
                $value21 = 10.0 - rand(20);
                $value22 = 10.0 - rand(20);
                $value23 = 10.0 - rand(20);
                $value31 = 10.0 - rand(20);
                $value32 = 10.0 - rand(20);
                $value33 = 10.0 - rand(20);
             }
             elsif( ($4 > $2) && ($4 > $6) && ($4 > $8) )
             {
                system("echo n2 is the winner with score $4! >> results.txt");
                $value21 = 10.0 - rand(20);
                $value22 = 10.0 - rand(20);
                $value23 = 10.0 - rand(20);
                $value31 = 10.0 - rand(20);
                $value32 = 10.0 - rand(20);
                $value33 = 10.0 - rand(20);
             }
             elsif( ($6 > $2) && ($6 > $4) && ($6 > $8) )
             {
                system("echo n3 is the winner with score $6! >> results.txt");
                $value11 = 10.0 - rand(20);
                $value12 = 10.0 - rand(20);
                $value13 = 10.0 - rand(20);
                $value31 = 10.0 - rand(20);
                $value32 = 10.0 - rand(20);
                $value33 = 10.0 - rand(20);
             }
             elsif( ($8 > $2) && ($8 > $4) && ($8 > $6) )
             {
                system("echo n4 is the winner with score $8! >> results.txt");
                $value11 = 10.0 - rand(20);
                $value12 = 10.0 - rand(20);
                $value13 = 10.0 - rand(20);
                $value21 = 10.0 - rand(20);
                $value22 = 10.0 - rand(20);
                $value23 = 10.0 - rand(20);
             }
         }
     }
     open(INFILE, "<game_agent.py") or die "Cannot open game_agent.py\n";
     @lines = <INFILE>;
     close INFILE;

     open (STDOUT, ">game_agent.py") or die "Can't reopen game_agent.py!\n";
     edit_weights();
     close STDOUT;
     
     goto LOOP;

#    re-weight the 2 loser players
#    inject game_agent.py with the new weights
#goto loop

sub edit_weights 
{

   for ( @lines ) {
       s/(WEIGHT1_A = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT1_A = $value11/;
       s/(WEIGHT1_B = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT1_B = $value12/;
       s/(WEIGHT1_C = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT1_C = $value13/;
       s/(WEIGHT2_A = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT2_A = $value21/;
       s/(WEIGHT2_B = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT2_B = $value22/;
       s/(WEIGHT2_C = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT2_C = $value23/;
       s/(WEIGHT3_A = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT3_A = $value31/;
       s/(WEIGHT3_B = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT3_B = $value32/;
       s/(WEIGHT3_C = [+-]?([0-9]*[.])?[0-9]+)/WEIGHT3_C = $value33/;
       print;
   }

}

