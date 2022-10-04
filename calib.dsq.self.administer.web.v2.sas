/*

DSQ Self-Administered Questionnaire: Web Version 2.1 (October, 2016)

  SAS program to analyze Dietary Screener Questionnaire (DSQ)
  data exported from the DSQ web site. This program expects the DSQ
  data to be in DietCalc format which is the default data export
  format.

  Please contact technical support at dhq@imsweb.com if you have
  questions or require assistance.

*/


/*
  The following file should be exported from the Dietary Screener
  Questionnaire (DSQ) web site.  The file must be in DietCalc format
  which is the default export format.
*/
filename yourdata '**insert file name for dsq data in DietCalc format**';


/*
  The following files are contained within the archive that
  contained this analysis program.  Once extracted from the archive,
  these files should be located in the same folder/directory as
  the analysis program.
*/
  libname ntile xlsx '..calib.DSQ.cereal.ntile.xlsx';
  libname psize xlsx '..calib.portion.size.xlsx';
  libname rcoeff xlsx '..calib.equation.coeff.xlsx';


proc format;
  value gender 1='male'
               2='female';


value $didfmt  /* Applies to all *_did variables */
'A'='Yes'
'B'='No'
'C'="Don't Know"
other="Missing"
;

value $unitsfmt /* Applies to all *_units variables */
'A'="PerDay"
'B'="perWeek"
'C'="PerMonth"
'E'="Don't know"
other="Missing"
;

value $milkchoicefmt  /* Applies to the milk_choice variable */
"A"="Whole or regular milk"
"B"="2% fat or reduced-fat milk"
"C"="1%, 1/2%, or low-fat milk"
"D"="Fat-free, skim or nonfat milk"
"E"="Soy milk"
"F"="Other"
other="Missing"
;

value $cerealchoicefmt  /* Applies to the cereal_1_choice and cereal_2_choice variables */
"A"="100% Bran"
"B"="100% Low Fat Natural Granola"
"C"="100% Natural Cereal"
"D"="100% Natural Cereal, with oats, honey and raisins"
"E"="100% Natural Granola, Oats & Honey"
"F"="100% Natural Wholegrain Cereal with raisins, lowfat"
"G"="All-Bran"
"H"="All-Bran Bran Buds"
"I"="All-Bran with Extra Fiber"
"J"="Alpen"
"K"="Alpha-Bits"
"L"="Alpha-Bits with marshmallows"
"M"="Amaranth Flakes"
"N"="Apple Jacks"
"O"="Apple Zaps"
"P"="Apple Zings, Malt-O-Meal"
"Q"="Banana Nut Crunch Cereal"
"R"="Barley"
"S"="Basic 4"
"T"="Berry Colossal Crunch, Malt-O-Meal"
"U"="Blueberry Morning"
"V"="Booberry"
"W"="Bran"
"X"="Bran Buds"
"Y"="Bran flakes"
"Z"="Bran, Nabisco"
"AA"="Branola"
"AB"="Brown Sugar Bliss"
"AC"="Buckwheat groats"
"AD"="Bulgur"
"AE"="Cap'n Crunch"
"AF"="Cap'n Crunch's Christmas Crunch"
"AG"="Cap'n Crunch's Crunch Berries"
"AH"="Cap'n Crunch's Oops! ChocoDonuts"
"AI"="Cap'n Crunch's Peanut Butter Crunch"
"AJ"="Cheerios"
"AK"="Cheerios, Apple Cinnamon"
"AL"="Cheerios, Berry Burst"
"AM"="Cheerios, Berry Burst Strawberry"
"AN"="Cheerios, Berry Burst Triple Berry"
"AO"="Cheerios, Berry Burst, Cherry Vanilla"
"AP"="Cheerios, Berry Burst, Strawberry Banana"
"AQ"="Cheerios, Frosted"
"AR"="Cheerios, Honey Nut"
"AS"="Cheerios, Multi Grain"
"AT"="Cheerios, Team"
"AU"="Cheerios, Yogurt Burst, Strawberry"
"AV"="Cheerios, Yogurt Burst, Vanilla"
"AW"="Cheese grits"
"AX"="Chex"
"AY"="Chex Morning Mix Banana Nut"
"AZ"="Chex Morning Mix Cinnamon"
"BA"="Chex Morning Mix Fruit & Nut"
"BB"="Chex Morning Mix Honey Nut"
"BC"="Chex, Bran"
"BD"="Chex, Corn"
"BE"="Chex, Honey Nut"
"BF"="Chex, Multi-Bran"
"BG"="Chex, Rice"
"BH"="Chex, Wheat"
"BI"="Chocolate frosted cereal"
"BJ"="Cinnamon Cluster Raisin Bran"
"BK"="Cinnamon Crunch Crispix"
"BL"="Cinnamon Grahams Cereal"
"BM"="Cinnamon Marshmallow Scooby Doo!"
"BN"="Cinnamon Toast Crunch"
"BO"="Cinnamon Toast Crunch, Reduced Sugar"
"BP"="Coco-Roos, Malt-O-Meal"
"BQ"="Cocoa Blasts"
"BR"="Cocoa Comets"
"BS"="Cocoa Dyno Bites, Malt-O-Meal"
"BT"="Cocoa Krispies"
"BU"="Cocoa Pebbles"
"BV"="Cocoa Puffs"
"BW"="Cocoa Puffs, Reduced Sugar"
"BX"="Cocoa Wheats"
"BY"="Complete Bran Flakes"
"BZ"="Complete Oat Bran Flakes"
"CA"="Complete Wheat Bran Flakes"
"CB"="Cookie-Crisp (all flavors)"
"CC"="Corn Bursts, Malt-O-Meal"
"CD"="Corn Flakes, Kellogg's"
"CE"="Corn Pops"
"CF"="Corn Puffs"
"CG"="Corn flakes"
"CH"="Corn flakes, low sodium"
"CI"="Cornmeal mush"
"CJ"="Count Chocula"
"CK"="Cracklin' Oat Bran"
"CL"="Cranberry Almond Crunch Cereal"
"CM"="Cream of Rice"
"CN"="Cream of Rye"
"CO"="Cream of Wheat"
"CP"="Crisp Crunch"
"CQ"="Crispix"
"CR"="Crispy Brown Rice Cereal"
"CS"="Crispy Rice"
"CT"="Crispy Rice, Malt-O-Meal"
"CU"="Crispy Wheats'N Raisins"
"CV"="Crunchy Corn Bran"
"CW"="Disney Cereal"
"CX"="Disney Hunny B's"
"CY"="Disney Mickey's Magix"
"CZ"="Disney Mud & Bugs"
"DA"="Ener-G Pure Rice Bran"
"DB"="Familia"
"DC"="Farina"
"DD"="Fiber 7 Flakes"
"DE"="Fiber One"
"DF"="Frankenberry"
"DG"="French Toast Crunch"
"DH"="Froot Loops"
"DI"="Frosted Flakes, Kellogg's"
"DJ"="Frosted Flakes, Malt-O-Meal"
"DK"="Frosted Fruit Rings"
"DL"="Frosted Mini Spooners, Malt-O-Meal"
"DM"="Frosted Mini Wheats"
"DN"="Frosted Shredded Wheat"
"DO"="Frosted Wheat Bites"
"DP"="Frosted cereal, with marshmallows"
"DQ"="Frosted corn flakes"
"DR"="Frosted flakes"
"DS"="Frosted rice"
"DT"="Frosty O's"
"DU"="Fruit & Fibre (fiber)"
"DV"="Fruit & Fibre (fiber) with Dates, Raisins and Walnuts"
"DW"="Fruit & Fibre (fiber) with Peaches, Raisins, Almonds, and Oat Clusters"
"DX"="Fruit Harvest"
"DY"="Fruit Harvest Apple Cinnamon"
"DZ"="Fruit Harvest Strawberry Blueberry"
"EA"="Fruit Loops"
"EB"="Fruit Rings"
"EC"="Fruit Whirls"
"ED"="Fruit and Cream Oatmeal"
"EE"="Fruity Dyno Bites, Malt-O-Meal"
"EF"="Fruity Pebbles"
"EG"="Golden Crisp"
"EH"="Golden Grahams"
"EI"="Golden Puffs, Malt-O-Meal"
"EJ"="Granola"
"EK"="Granola, homemade"
"EL"="Granola, lowfat"
"EM"="Granola, lowfat, Kellogg's"
"EN"="Granola, lowfat, with Raisins, Kellogg's"
"EO"="Grape Nut O's"
"EP"="Grape-Nuts"
"EQ"="Grape-Nuts Flakes"
"ER"="Great Grains Crunchy Pecan Whole Grain Cereal"
"ES"="Great Grains, Raisins, Dates, and Pecans Whole Grain Cereal"
"ET"="Grits"
"EU"="Harina de maize con leche"
"EV"="Harmony Vanilla Almond Oats"
"EW"="Healthy Choice"
"EX"="Honey Bunches of Oat Honey Roasted"
"EY"="Honey Bunches of Oat with Strawberry"
"EZ"="Honey Bunches of Oats"
"FA"="Honey Bunches of Oats with Almonds"
"FB"="Honey Buzzers, Malt-O-Meal"
"FC"="Honey Crisp Corn Flakes"
"FD"="Honey Crunch Corn Flakes"
"FE"="Honey Graham Squares, Malt-O-Meal"
"FF"="Honey Nut Clusters"
"FG"="Honey Nut Heaven"
"FH"="Honey Nut Shredded Wheat"
"FI"="Honey Smacks"
"FJ"="Honeycomb"
"FK"="Honeycomb, strawberry"
"FL"="Instant Grits, all flavors"
"FM"="Jenny O's"
"FN"="Just Right"
"FO"="Just Right with Fruit & Nut"
"FP"="Kaboom"
"FQ"="Kasha"
"FR"="Kashi"
"FS"="Kashi GOLEAN"
"FT"="Kashi Good Friends"
"FU"="Kashi Good Friends Cinna-Raisin Crunch"
"FV"="Kashi Heart to Heart Cereal"
"FW"="Kashi Honey Puffed"
"FX"="Kashi Medley"
"FY"="Kashi Organic Promise"
"FZ"="Kashi Pilaf"
"GA"="Kashi Pillows"
"GB"="Kashi Seven in the Morning"
"GC"="Kashi, Puffed"
"GD"="Kix"
"GE"="Kix, Berry Berry"
"GF"="Life (plain and cinnamon)"
"GG"="Lucky Charms"
"GH"="Lucky Charms, Berry"
"GI"="Lucky Charms, Chocolate"
"GJ"="Magic Stars"
"GK"="Malt-O-Meal"
"GL"="Malt-O-Meal, chocolate"
"GM"="Maltex"
"GN"="Marshmallow Mateys, Malt-O-Meal"
"GO"="Marshmallow Safari"
"GP"="Masa harina"
"GQ"="Maypo"
"GR"="Millet"
"GS"="Millet, puffed"
"GT"="Mini-Wheats"
"GU"="Mini-Wheats Frosted Bite Size"
"GV"="Mini-Wheats Frosted Original"
"GW"="Mini-Wheats Frosted Raisin"
"GX"="Mini-Wheats Frosted Strawberry"
"GY"="Mother's Natural Foods Cereal, Quaker"
"GZ"="Muesli"
"HA"="Muesli(x)"
"HB"="Multigrain Oatmeal"
"HC"="Multigrain cereal"
"HD"="Natural Bran Flakes"
"HE"="Nature Valley Granola"
"HF"="Nature Valley Granola, with fruit and nuts"
"HG"="Nesquik"
"HH"="Nestum"
"HI"="Nu System Cuisine Toasted Grain Circles"
"HJ"="Nutri-Grain"
"HK"="Nutri-Grain Golden Wheat and Raisin"
"HL"="Nutty Nuggets"
"HM"="OS"
"HN"="Oat Bran Cereal, Quaker"
"HO"="Oat Bran Flakes, Health Valley"
"HP"="Oat bran cereal"
"HQ"="Oat bran uncooked"
"HR"="Oat cereal"
"HS"="Oat flakes"
"HT"="Oatmeal"
"HU"="Oatmeal Crisp"
"HV"="Oatmeal Crisp with Almonds"
"HW"="Oatmeal Crisp, Apple Cinnamon"
"HX"="Oatmeal Crisp, Raisin"
"HY"="Oatmeal Squares"
"HZ"="Oatmeal Swirlers"
"IA"="Oats, raw"
"IB"="Oh's"
"IC"="Oh's, Apple Cinnamon"
"ID"="Oh's, Fruitangy"
"IE"="Oh's, Honey Graham"
"IF"="Old Wessex Irish Style Oatmeal"
"IG"="Optimum Slim, Nature's Path"
"IH"="Optimum, Nature's Path"
"II"="Oreo O's Cereal"
"IJ"="Peanut Butter Toast Crunch"
"IK"="Polenta"
"IL"="Product 19"
"IM"="Puffed Rice, Malt-O-Meal"
"IN"="Puffed Wheat, Malt-O-Meal"
"IO"="Quaker Dinosaur Eggs oatmeal"
"IP"="Quaker Fruit and Cream Oatmeal"
"IQ"="Quaker Instant Grits, all flavors"
"IR"="Quaker Multigrain Oatmeal"
"IS"="Quaker Oatmeal Express"
"IT"="Quaker Oatmeal Nutrition for Women"
"IU"="Quaker Oatmeal Squares"
"IV"="Quisp"
"IW"="Raisin Bran Crunch"
"IX"="Raisin Bran, Kellogg's"
"IY"="Raisin Bran, Post"
"IZ"="Raisin Nut Bran"
"JA"="Raisin bran"
"JB"="Reese's Peanut Butter Puffs"
"JC"="Rice Krispies"
"JD"="Rice Krispies, Frosted"
"JE"="Rice Krispies, Treats Cereal"
"JF"="Rice bran, uncooked"
"JG"="Rice cereal"
"JH"="Rice flakes"
"JI"="Rice polishings"
"JJ"="Rice, puffed"
"JK"="Roman Meal"
"JL"="Seven-grain Cereal"
"JM"="Seven-grain cereal"
"JN"="Shredded Wheat"
"JO"="Shredded Wheat 'N Bran"
"JP"="Shredded Wheat Spoon Size"
"JQ"="Shredded Wheat, 100%"
"JR"="Shredded Wheat, Original"
"JS"="Smacks"
"JT"="Smart Start"
"JU"="Smorz"
"JV"="Special K"
"JW"="Special K Fruit & Yogurt"
"JX"="Special K Low Carb Lifestyle Protein Plus"
"JY"="Special K Red Berries"
"JZ"="Special K Vanilla Almond"
"KA"="Strawberry Squares"
"KB"="Sun Country 100% Natural Granola, with Almonds"
"KC"="Sweet Crunch"
"KD"="Sweet Puffs"
"KE"="Tasteeos"
"KF"="Toasted Cinnamon Twists, Malt-O-Meal"
"KG"="Toasted Oatmeal Cereal"
"KH"="Toasted Oatmeal, Honey Nut"
"KI"="Toasted oat cereal"
"KJ"="Toasties"
"KK"="Toasty O's, Apple Cinnamon, Malt-O-Meal"
"KL"="Toasty O's, Honey and Nut, Malt-O-Meal"
"KM"="Toasty O's, Malt-O-Meal"
"KN"="Tony's Cinnamon Crunchers"
"KO"="Tootie Fruities, Malt-O-Meal"
"KP"="Total"
"KQ"="Total Brown Sugar & Oats"
"KR"="Total Corn Flakes"
"KS"="Total Instant Oatmeal"
"KT"="Total Raisin Bran"
"KU"="Trix"
"KV"="Trix, Reduced Sugar"
"KW"="Uncle Sam's Hi Fiber Cereal"
"KX"="Under Cover Bears"
"KY"="Waffle Crisp"
"KZ"="Weetabix Whole Wheat Cereal"
"LA"="Wheat Hearts"
"LB"="Wheat bran, unprocessed (miller's bran)"
"LC"="Wheat cereal"
"LD"="Wheat germ"
"LE"="Wheat germ, with sugar and honey"
"LF"="Wheat, puffed"
"LG"="Wheat, puffed, presweetened with sugar"
"LH"="Wheatena"
"LI"="Wheaties"
"LJ"="Wheaties Energy Crunch"
"LK"="Wheaties Raisin Bran"
"LL"="Whole wheat cereal"
"LM"="Whole wheat, cracked"
"LN"="Zoom"
"LO"="Other Hot Cereal"
"LP"="Other Cold Cereal"
"LQ"="Other"
other="Missing"
;

run;


data dsq;
infile yourdata missover lrecl=400;
length cereal_1_choice $ 3;
length cereal_2_choice $ 3;

input
@1      study_id 12.

@13     respondent_id $30.

@43     status_date YYMMDD8.

@51     Q1AGE 3.

@54     Q2SEX $1.
@55     cereal_did            $1. /* Cereal Frequency               Did you eat any hot or cold cereals? */
@56     cereal_1_freq         $4. /* Cereal Frequency               How often did you eat hot or cold cereals?  */
@60     cereal_1_units        $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */
@61     cereal_1_choice       $3.       /* Cereal Choice 1          What kind of cereal did you usually eat?&nbsp;&nbsp;Pick one. */
@64     cereal_1_other_hot         $char25.  /* Cereal Choice 1          You selected Other Hot Cereal. What other hot cereal was this?  */
@89     cereal_1_other_cold        $char25.  /* Cereal Choice 1          You selected Other Cold Cereal. What other cold cereal was this?  */
@114    cereal_1_other             $char25.  /* Cereal Choice 1          You selected Other for cereal. What other cereal was this?  */

@139    cereal_2_did          $1.       /* Cereal Choice 1          Was there another cereal that you usually ate?   */
@140    cereal_2_choice       $3.       /* Cereal Choice 2          What second kind of cereal did you usually eat?&nbsp;&nbsp;Pick one.   */
@143    cereal_2_other_hot         $char25.  /* Cereal Choice 2          You selected Other Hot Cereal. What other hot cereal was this?  */
@168    cereal_2_other_cold        $char25.  /* Cereal Choice 2          You selected Other Cold Cereal. What other cold cereal was this?  */
@193    cereal_2_other             $char25.  /* Cereal Choice 2          You selected Other for cereal. What other cereal was this?  */

@218    milk_did              $1.       /* Milk                     Did you have any milk (either to drink or on cereal)?  */
@219    milk_freq             $4.       /* Milk                     How often did you have any milk (either to drink or on cereal)?  */
@223    milk_units            $1.       /* Freq Units               A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */
@224    milk_choice           $1.       /* Milk                     What kind of milk did you usually drink? */
@225    milk_other            $char25.  /* Milk                     You selected Other for type of milk.  What kind of milk was this? */

@250    soda_did              $1. /* Regular Soda                   Did you drink any regular soda or pop that contains sugar?    */
@251    soda_freq             $4. /* Regular Soda                   How often did you drink regular soda or pop?   */
@255    soda_units            $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@256    juice_did             $1. /* 100% Pure Fruit Juices         Did you drink any 100% pure fruit juices such as orange, mango, apple, grape and pineapple juices?   */
@257    juice_freq            $4. /* 100% Pure Fruit Juices         How often did you drink 100% pure fruit juice? */
@261    juice_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@262    coffee_did            $1. /* Sweetened Coffee and Tea       Did you drink any coffee or tea that had sugar or honey added to it?  */
@263    coffee_freq           $4. /* Sweetened Coffee and Tea       How often did you drink coffee or tea containing sugar or honey?   */
@267    coffee_units          $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@268    sweet_drinks_did      $1. /* Other Sweetened Drinks         Did you drink any sweetened fruit drinks, sports or energy drinks, such as Kool-aid, lemonade, Hi-C, cranberry drink, Gatorade, Red Bull, or Vitamin Water?   */
@269    sweet_drinks_freq     $4. /* Other Sweetened Drinks         How often did you drink sweetened fruit, sports or energy drinks?   */
@273    sweet_drinks_units    $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@274    fruit_did             $1. /* Fruit                          Did you eat any fruit? Include fresh, frozen, or canned fruit. Do not include juices.  */
@275    fruit_freq            $4. /* Fruit                          How often did you eat fruit? */
@279    fruit_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@280    salad_did             $1. /* Green Salad                    Did you eat a green leafy or lettuce salad, with or without other vegetables?  */
@281    salad_freq            $4. /* Green Salad                    How often did you eat salad? */
@285    salad_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@286    potatoes_fried_did    $1. /* Fried Potatoes                 Did you eat any kind of fried potatoes including french fries, home fries, or hash brown potatoes?  */
@287    potatoes_fried_freq   $4. /* Fried Potatoes                 How often did you eat any kind of fried potatoes? */
@291    potatoes_fried_units  $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@292    potatoes_oth_did      $1. /* Other Potatoes                 Did you eat any other kind of potatoes, such as baked, boiled, mashed potatoes, sweet potatoes, or potato salad?   */
@293    potatoes_oth_freq     $4. /* Other Potatoes                 How often did you eat any other kind of potatoes? */
@297    potatoes_oth_units    $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@298    dry_beans_did         $1. /* Cooked Dried Beans             Did you eat any refried beans, baked beans, beans in soup, pork and beans or other cooked dried beans?  */
@299    dry_beans_freq        $4. /* Cooked Dried Beans             How often did you eat refried beans, baked beans, beans in soup, pork and beans or other cooked dried beans?  */
@303    dry_beans_units       $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@304    grains_did            $1. /* Whole Grains                   Did you eat any brown rice or other cooked whole grains, such as bulgur, cracked wheat, or millet? Do not include white rice. */
@305    grains_freq           $4. /* Whole Grains                   How often did you eat brown rice or other cooked whole grains?*/
@309    grains_units          $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@310    vegetables_did        $1. /* Other Vegetables               not including green salads, potatoes, and cooked dried beans, did you eat any other vegetables?  */
@311    vegetables_freq       $4. /* Other Vegetables               How often did you eat other vegetables?  */
@315    vegetables_units      $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@316    salsa_did             $1. /* Salsa                          Did you eat any Mexican-type salsa made with tomato?   */
@317    salsa_freq            $4. /* Salsa                          How often did you have Mexican-type salsa made with tomato?   */
@321    salsa_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@322    pizza_did             $1. /* Pizza                          Did you eat any pizza? Include frozen pizza, fast food pizza, and homemade pizza. */
@323    pizza_freq            $4. /* Pizza                          How often did you eat pizza? */
@327    pizza_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@328    sauce_did             $1. /* Tomato Sauce                   Did you have any tomato sauces such as with spaghetti or noodles or mixed into foods such as lasagna?   */
@329    sauce_freq            $4. /* Tomato Sauce                   How often did you have tomato sauces? */
@333    sauce_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@334    cheese_did            $1. /* Cheese                         Did you eat any kind of cheese?   */
@335    cheese_freq           $4. /* Cheese                         How often did you eat any kind of cheese?   */
@339    cheese_units          $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@340    red_meat_did          $1. /* Red Meat                       Did you eat any red meat, such as beef, pork, ham, or sausage? */
@341    red_meat_freq         $4. /* Red Meat                       How often did you eat red meat? */
@345    red_meat_units        $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@346    proc_meat_did         $1. /* Processed Meat                 Did you eat any processed meat, such as bacon, lunch meats, or hot dogs? */
@347    proc_meat_freq        $4. /* Processed Meat                 How often did you eat processed meat? */
@351    proc_meat_units       $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@352    bread_did             $1. /* Whole Grain Bread              Did you eat any whole grain bread including toast, rolls and in sandwhiches?  */
@353    bread_freq            $4. /* Whole Grain Bread              How often did you eat whole grain bread? */
@357    bread_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@358    candy_did             $1. /* Chocolate and Candy            Did you eat any chocolate or any other types of candy? Do not include sugar-free candy. */
@359    candy_freq            $4. /* Chocolate and Candy            How often did you eat chocolate or any other types of candy? */
@363    candy_units           $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@364    doughnuts_did         $1. /* Doughnuts                      Did you eat any doughnuts, sweet rolls, Danish, muffins, (pan dulce) or pop-tarts? Do not include sugar-free items.  */
@365    doughnuts_freq        $4. /* Doughnuts                      How often did you eat doughnuts, sweet rolls, Danish, muffins, (pan dulce) or pop-tarts? */
@369    doughnuts_units       $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@370    cookies_did           $1. /* Cookies, Cakes, Pie, Brownies  Did you eat any cookies, cake, pie, or brownies? Do not include sugar-free kinds.   */
@371    cookies_freq          $4. /* Cookies, Cakes, Pie, Brownies  How often did you eat cookies, cake, pie, or brownies?  */
@375    cookies_units         $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@376    desserts_did          $1. /* Frozen Desserts                Did you eat any ice cream or other frozen desserts? Do not include sugar-free kinds.   */
@377    desserts_freq         $4. /* Frozen Desserts                How often did you eat ice cream or other frozen desserts?  */
@381    desserts_units        $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

@382    popcorn_did           $1. /* Popcorn                        Did you eat any popcorn? */
@383    popcorn_freq          $4. /* Popcorn                        How often did you eat popcorn?  */
@387    popcorn_units         $1. /* Freq Units                     A=PerDay, B=PerWeek, C=PerMonth, E=Don't Know */

;

run;


data dsq;
  set dsq;


  *converting responses into times per day for food variables of interest;


  %macro xpd (did,unit,often,outv,maxv);
  if &did='B' then &outv=0;
    else if &did='A' then do;
     if &unit='A' then &outv=1*&often;
       else if &unit='B' then &outv=1*&often/7;
       else if &unit='C' then &outv=1*&often/30;
     end;
    *top code outliers;
    if &outv > &maxv then &outv=&maxv;
  %mend;

  %xpd(cereal_did,cereal_1_units,cereal_1_freq,hccerxpd,7);
  %xpd(milk_did,milk_units,milk_freq,milkxpd,10);
  %xpd(soda_did,soda_units,soda_freq,sodaxpd,8);
  %xpd(juice_did,juice_units,juice_freq,frtjcxpd,8);
  %xpd(coffee_did,coffee_units,coffee_freq,swtctxpd,10);
  %xpd(sweet_drinks_did,sweet_drinks_units,sweet_drinks_freq,energyxpd,7);
  %xpd(fruit_did,fruit_units,fruit_freq,fruitxpd,8);
  %xpd(salad_did,salad_units,salad_freq,saladxpd,5);
  %xpd(potatoes_fried_did,potatoes_fried_units,potatoes_fried_freq,frfryxpd,5);
  %xpd(potatoes_oth_did,potatoes_oth_units,potatoes_oth_freq,othpotxpd,3);
  %xpd(dry_beans_did,dry_beans_units,dry_beans_freq,beanxpd,4);
  %xpd(vegetables_did,vegetables_units,vegetables_freq,othvegxpd,5);
  %xpd(pizza_did,pizza_units,pizza_freq,pizzaxpd,2);
  %xpd(salsa_did,salsa_units,salsa_freq,salsaxpd,3);
  %xpd(sauce_did,sauce_units,sauce_freq,tomscxpd,2);
  %xpd(red_meat_did,red_meat_units,red_meat_freq,redmtxpd,6);
  %xpd(proc_meat_did,proc_meat_units,proc_meat_freq,procmtxpd,4);
  %xpd(cheese_did,cheese_units,cheese_freq,cheesexpd,6);
  %xpd(bread_did,bread_units,bread_freq,whgbrdxpd,6);
  %xpd(grains_did,grains_units,grains_freq,brricexpd,4);
  %xpd(candy_did,candy_units,candy_freq,candyxpd,8);
  %xpd(doughnuts_did,doughnuts_units,doughnuts_freq,donutxpd,5);
  %xpd(cookies_did,cookies_units,cookies_freq,cakexpd,7);
  %xpd(desserts_did,desserts_units,desserts_freq,icecrmxpd,5);
  %xpd(popcorn_did,popcorn_units,popcorn_freq,popcornxpd,3);

  label hccerxpd='number of times per day eat hot or cold cereal'
        milkxpd='number of times per day drink milk'
	sodaxpd='number of times per day drink soda'
	frtjcxpd='number of times per day drink fruit juice'
	swtctxpd='number of times per day drink sweet coffee/tea'
	energyxpd='number of times per day drink fruit/sports/energy drink'
	fruitxpd='number of times per day eat fruit'
	saladxpd='number of times per day eat salad'
	frfryxpd='number of times per day eat fried potatoes'
	othpotxpd='number of times per day eat other potatoes'
	beanxpd='number of times per day eat beans'
	othvegxpd='number of times per day eat other vegetables'
	pizzaxpd='number of times per day eat pizza'
	salsaxpd='number of times per day eat salsa'
	tomscxpd='number of times per day eat tomtato sauce'
	redmtxpd='number of times per day eat red meat'
	procmtxpd='number of times per day eat processed meat'
	cheesexpd='number of times per day eat cheese'
	whgbrdxpd='number of times per day eat whole grain bread'
	brricexpd='number of times per day eat cooked whole grain (brown rice)'
	candyxpd='number of times per day eat candy'
	donutxpd='number of times per day eat pastries'
	cakexpd='number of times per day eat cookies/cake'
	icecrmxpd='number of times per day eat ice cream'
	popcornxpd='number of times per day eat pop corn';

run;


data dtq;
  set dsq;

  *rename variables;
  ageinyr=q1age;
  if q2sex='A' then gender=1;
    else if q2sex='B' then gender=2;

  if (2 <= ageinyr <= 3) then bcage=1;
    else if (4 <= ageinyr <= 5) then bcage=2;
    else if (6 <= ageinyr <= 7) then bcage=3;
    else if (8 <= ageinyr <= 9) then bcage=4;
    else if (10 <= ageinyr <= 11) then bcage=5;
    else if (12 <= ageinyr <= 13) then bcage=6;
    else if (14 <= ageinyr <= 15) then bcage=7;
    else if (16 <= ageinyr <= 17) then bcage=8;
    else if (18 <= ageinyr <= 25) then bcage=9;
    else if (26 <= ageinyr <= 35) then bcage=10;
    else if (36 <= ageinyr <= 45) then bcage=11;
    else if (46 <= ageinyr <= 60) then bcage=12;
    else if (61 <= ageinyr <= 69) then bcage=13;
    else if (70 <= ageinyr <= 99) then bcage=14;

    *make age dummy variables ****;

    if (2 <= ageinyr <= 11) then kidgrp=1;
      else kidgrp=0;
    if (12 <= ageinyr <= 17) then teengrp=1;
      else teengrp=0;


  /* if all ages responded to all questions, then no modifications are needed                                                    */
  /* if kids < age 12 did NOT answer sugar in coffee/tea, then set response to zero.  This option should be commented out if not */
  /*   necessary                                                                                                                 */


  /*optional */
  if kidgrp=1 then swtctxpd=0;
  *end of option;


  length cereal1fc cereal2fc $12.;

  cereal1fc=compress(cereal_1_choice);
  cereal2fc=compress(cereal_2_choice);

  *create numcer to represent the number of cereals provided;

  if cereal1fc='...' and cereal2fc='...' then numcer=0;
    else if cereal1fc ne '...' and cereal2fc ne '...' then numcer=2;
    else if cereal1fc ne '...' then numcer=1;

run;

*this will input cereal ntile data;

data ntile;
  set ntile.'CALIB.DSQ.CEREAL.NTILE'n;
run;


proc sort data=ntile;
  by cchoice;
run;

data ntile (keep=cereal1fc cereal2fc whgnt sugnt calcnt fibnt);
  set ntile;
  by cchoice;
  if first.cchoice;
  cereal1fc=compress(cchoice);
  cereal2fc=compress(cchoice);
run;

proc sort data=dtq;
  by cereal1fc;
run;

proc sort data=ntile;
  by cereal1fc;
run;



data dtq (drop= whgnt sugnt calcnt fibnt);
  merge dtq (in=d) ntile (drop=cereal2fc);
  by cereal1fc;
  if d;

  c1whgnt=whgnt;
  c1sugnt=sugnt;
  c1calcnt=calcnt;
  c1fibnt=fibnt;
run;

proc sort data=dtq;
  by cereal2fc;
run;

proc sort data=ntile;
  by cereal2fc;
run;

data dtq (drop= whgnt sugnt calcnt fibnt);
  merge dtq (in=d) ntile (drop=cereal1fc);
  by cereal2fc;
  if d;


  c2whgnt=whgnt;
  c2sugnt=sugnt;
  c2calcnt=calcnt;
  c2fibnt=fibnt;
run;


data dtq;
  set dtq;

  if numcer in (0,1,2) and hccerxpd >= 0 then do;
   wg1f=0; wg2f=0; wg3f=0;
   as1f=0; as2f=0; as3f=0;
   cm1f=0; cm2f=0; cm3f=0;
   fb1f=0; fb2f=0; fb3f=0;
  if numcer=1 then do;
    if c1whgnt=1 then wg1f=wg1f+hccerxpd;
      else if c1whgnt=2 then wg2f=wg2f+hccerxpd;
      else if c1whgnt=3 then wg3f=wg3f+hccerxpd;
    if c1sugnt=1 then as1f=as1f+hccerxpd;
      else if c1sugnt=2 then as2f=as2f+hccerxpd;
      else if c1sugnt=3 then as3f=as3f+hccerxpd;
    if c1calcnt=1 then cm1f=cm1f+hccerxpd;
      else if c1calcnt=2 then cm2f=cm2f+hccerxpd;
      else if c1calcnt=3 then cm3f=cm3f+hccerxpd;
    if c1fibnt=1 then fb1f=fb1f+hccerxpd;
      else if c1fibnt=2 then fb2f=fb2f+hccerxpd;
      else if c1fibnt=3 then fb3f=fb3f+hccerxpd;
   end;
   else if numcer=2 then do;
    if c1whgnt=1 then wg1f=wg1f+(.75*hccerxpd);
      else if c1whgnt=2 then wg2f=wg2f+(.75*hccerxpd);
      else if c1whgnt=3 then wg3f=wg3f+(.75*hccerxpd);
    if c2whgnt=1 then wg1f=wg1f+(.25*hccerxpd);
      else if c2whgnt=2 then wg2f=wg2f+(.25*hccerxpd);
      else if c2whgnt=3 then wg3f=wg3f+(.25*hccerxpd);
    if c1sugnt=1 then as1f=as1f+(.75*hccerxpd);
      else if c1sugnt=2 then as2f=as2f+(.75*hccerxpd);
      else if c1sugnt=3 then as3f=as3f+(.75*hccerxpd);
    if c2sugnt=1 then as1f=as1f+(.25*hccerxpd);
      else if c2sugnt=2 then as2f=as2f+(.25*hccerxpd);
      else if c2sugnt=3 then as3f=as3f+(.25*hccerxpd);
    if c1calcnt=1 then cm1f=cm1f+(.75*hccerxpd);
      else if c1calcnt=2 then cm2f=cm2f+(.75*hccerxpd);
      else if c1calcnt=3 then cm3f=cm3f+(.75*hccerxpd);
    if c2calcnt=1 then cm1f=cm1f+(.25*hccerxpd);
      else if c2calcnt=2 then cm2f=cm2f+(.25*hccerxpd);
      else if c2calcnt=3 then cm3f=cm3f+(.25*hccerxpd);
    if c1fibnt=1 then fb1f=fb1f+(.75*hccerxpd);
      else if c1fibnt=2 then fb2f=fb2f+(.75*hccerxpd);
      else if c1fibnt=3 then fb3f=fb3f+(.75*hccerxpd);
    if c2fibnt=1 then fb1f=fb1f+(.25*hccerxpd);
      else if c2fibnt=2 then fb2f=fb2f+(.25*hccerxpd);
      else if c2fibnt=3 then fb3f=fb3f+(.25*hccerxpd);

    end;
   end;
run;

proc sort data=dtq;
  by gender bcage;
run;

*this pulls in the portion size adjustment information by gender and agegrp;
data adjps;
  set psize.'CALIB.PORTION.SIZE'n;
  bcage=agegrp;
run;

proc sort data=adjps;
  by gender bcage;
run;


*merge analysis data with portion size adjustment data;
data dtq;
  merge dtq (in=d) adjps;
  by gender bcage;
  if d;
run;

data dtq;
  set dtq;
  by gender;

  *make psize adj freq vars;
  gfb1f=fb1f*gadj25;
  gfb2f=fb2f*gadj26;
  gfb3f=fb3f*gadj27;
  gmilk=milkxpd*gadj3;
  gsoda=sodaxpd*gadj4;
  gfrtjc=frtjcxpd*gadj5;
  gswtct=swtctxpd*gadj6;
  genergy=energyxpd*gadj7;
  gfruit=fruitxpd*gadj8;
  gsalad=saladxpd*gadj9;
  gfrfry=frfryxpd*gadj10;
  gothpot=othpotxpd*gadj11;
  gbean=beanxpd*gadj12;
  gothveg=othvegxpd*gadj13;
  gpizza=pizzaxpd*gadj14;
  gsalsa=salsaxpd*gadj15;
  gtomsc=tomscxpd*gadj16;
  gcheese=cheesexpd*gadj17;
  gwhgbrd=whgbrdxpd*gadj18;
  gbrrice=brricexpd*gadj19;
  gcandy=candyxpd*gadj20;
  gdonut=donutxpd*gadj21;
  gcake=cakexpd*gadj22;
  gicecrm=icecrmxpd*gadj23;
  gpopcorn=popcornxpd*gadj24;

  *calcium;
  gcm1f=cm1f*gadj28;
  gcm2f=cm2f*gadj29;
  gcm3f=cm3f*gadj30;

  *for whole grain;
  gwg1f=wg1f*gadj34;
  gwg2f=wg2f*gadj35;
  gwg3f=wg3f*gadj36;

  *for dairy;
  dmilk=milkxpd*dadj3;
  dcheese=cheesexpd*dadj17;
  dpizza=pizzaxpd*dadj14;
  dicecrm=icecrmxpd*dadj23;


  *for sugar/ssb;
  sas1f=as1f*sadj31;
  sas2f=as2f*sadj32;
  sas3f=as3f*sadj33;
  sicecrm=icecrmxpd*sadj23;
  scake=cakexpd*sadj22;
  ssoda=sodaxpd*sadj4;
  sswtct=swtctxpd*sadj6;
  senergy=energyxpd*sadj7;
  scandy=candyxpd*sadj20;
  sdonut=donutxpd*sadj21;


  *for fruit;
  ffrtjc=frtjcxpd*fadj5;
  ffruit=fruitxpd*fadj8;


  *for veg;
  vsalad=saladxpd*vadj9;
  vfrfry=frfryxpd*vadj10;
  vothpot=othpotxpd*vadj11;
  vbean=beanxpd*vadj12;
  vothveg=othvegxpd*vadj13;
  vpizza=pizzaxpd*vadj14;
  vsalsa=salsaxpd*vadj15;
  vtomsc=tomscxpd*vadj16;

  *for tot frt/veg;
  pfrtjc=frtjcxpd*padj5;
  pfruit=fruitxpd*padj8;
  psalad=saladxpd*padj9;
  pfrfry=frfryxpd*padj10;
  pothpot=othpotxpd*padj11;
  pbean=beanxpd*padj12;
  pothveg=othvegxpd*padj13;
  ppizza=pizzaxpd*padj14;
  psalsa=salsaxpd*padj15;
  ptomsc=tomscxpd*padj16;

run;


*this pulls in the intercept and beta coefficient information by gender;

data betaint;
  set rcoeff.'CALIB.EQUATION.COEFF'n;
run;

proc sort data=betaint;
  by gender;
run;

*merge analysis data with intercept and beta coefficient data;
data mdtq;
  merge dtq (in=d) betaint;
  by gender;
  if d;
run;

data mdtq;
  set mdtq;
  by gender;

  DSQfib=mfintercept +  (kidgrp*mfkidb) + (teengrp*mfteenb)  + (gfb1f*mfcer1b) + (gfb2f*mfcer2b) + (gfb3f*mfcer3b) + (gwhgbrd*mfwgbb) + (gbrrice*mfbrricb) +
     (gcheese*mfcheesb) +  (gpizza*mfpizzab) +  (gmilk*mfmilkb) +  (gicecrm*mficecrb) +  (gpopcorn*mfpcornb) +
     (gsoda*mfsodab) +  (genergy*mfspdrb) +  (gcake*mfcakeb) +  (gdonut*mfdonutb) +  (gswtct*mfswctb) +  (gcandy*mfcandyb) +
     (gfrtjc*mffjcb) +  (gfruit*mffruitb)  +  (gsalad*mfsaladb) + (gothpot*mfothptb) +  (gbean*mfbeanb) +
     (gothveg*mfothvgb) +  (gfrfry*mffrfrb) +  (gtomsc*mftomscb) +  (gsalsa*mfsalsab) ;

  DSQcalc=mcintercept +  (kidgrp*mckidb) + (teengrp*mcteenb)  + (gcm1f*mccer1b) + (gcm2f*mccer2b) + (gcm3f*mccer3b) + (gwhgbrd*mcwgbb) + (gbrrice*mcbrricb) +
     (gcheese*mccheesb) +  (gpizza*mcpizzab) +  (gmilk*mcmilkb) +  (gicecrm*mcicecrb) +  (gpopcorn*mcpcornb) +
     (gsoda*mcsodab) +  (genergy*mcspdrb) +  (gcake*mccakeb) +  (gdonut*mcdonutb) +  (gswtct*mcswctb) +  (gcandy*mccandyb) +
     (gfrtjc*mcfjcb) +  (gfruit*mcfruitb)  +  (gsalad*mcsaladb) + (gothpot*mcothptb) +  (gbean*mcbeanb) +
     (gothveg*mcothvgb) +  (gfrfry*mcfrfrb) +  (gtomsc*mctomscb) +  (gsalsa*mcsalsab) ;

  DSQwhgr=mgintercept +  (kidgrp*mgkidb) + (teengrp*mgteenb)  + (gwg1f*mgcer1b) + (gwg2f*mgcer2b) + (gwg3f*mgcer3b) + (gwhgbrd*mgwgbb) + (gbrrice*mgbrricb) +
      (gpopcorn*mgpcornb)  ;

  DSQsug=msintercept +  (kidgrp*mskidb) + (teengrp*msteenb)  + (sas1f*mscer1b) + (sas2f*mscer2b) + (sas3f*mscer3b) +
     (sicecrm*msicecrb) +  (ssoda*mssodab) +  (senergy*msspdrb) +  (scake*mscakeb) +  (sdonut*msdonutb) +  (sswtct*msswctb) +  (scandy*mscandyb) ;

  DSQdairy=mdintercept +   (kidgrp*mdkidb) + (teengrp*mdteenb)  + (dcheese*mdcheesb) +  (dpizza*mdpizzab) +  (dmilk*mdmilkb) +  (dicecrm*mdicecrb)  ;

  DSQfvl=mpintercept +   (kidgrp*mpkidb) + (teengrp*mpteenb) +
     (pfrtjc*mpfjcb) +  (pfruit*mpfruitb)  +  (psalad*mpsaladb) + (pothpot*mpothptb) +  (pbean*mpbeanb) +
     (pothveg*mpothvgb) +  (pfrfry*mpfrfrb) +  (ptomsc*mptomscb) +  (psalsa*mpsalsab) +  (ppizza*mppizzab) ;

  DSQvlall=mvintercept +   (kidgrp*mvkidb) + (teengrp*mvteenb) +
     (vsalad*mvsaladb) + (vothpot*mvothptb) +  (vbean*mvbeanb) +  (vpizza*mvpizzab) +
     (vothveg*mvothvgb) +  (vfrfry*mvfrfrb) +  (vtomsc*mvtomscb) +  (vsalsa*mvsalsab) ;

  DSQfvlnf=mnintercept +   (kidgrp*mnkidb) + (teengrp*mnteenb) +
     (pfrtjc*mnfjcb) +  (pfruit*mnfruitb)  +  (psalad*mnsaladb) + (pothpot*mnothptb) +  (pbean*mnbeanb) +
     (pothveg*mnothvgb) +  (ptomsc*mntomscb) +  (psalsa*mnsalsab) + (ppizza*mnpizzab) ;

  DSQvlnf=muintercept +   (kidgrp*mukidb) + (teengrp*muteenb) +
     (vsalad*musaladb) + (vothpot*muothptb) +  (vbean*mubeanb) +  (vpizza*mupizzab) +
     (vothveg*muothvgb) +  (vtomsc*mutomscb) +  (vsalsa*musalsab) ;

  DSQfrt=mrintercept +   (kidgrp*mrkidb) + (teengrp*mrteenb)  + (ffrtjc*mrfjcb) +  (ffruit*mrfruitb)  ;

  DSQssb=mxintercept +  (kidgrp*mxkidb) + (teengrp*mxteenb) +  (ssoda*mxsodab) +  (senergy*mxspdrb) + (sswtct*mxswctb)  ;

label  DSQfvl = 'Predicted intake of fruits and vegetables including legumes and French fries (cup equivalents) per day'
 DSQfvlnf = 'Predicted intake of fruits and vegetables including legumes and excluding French fries (cup equivalents) per day'
 DSQfrt = 'Predicted intake of fruits (cup equivalents) per day'
 DSQvlall = 'Predicted intake of vegetables including legumes and French fries (cup equivalents) per day'
 DSQvlnf = 'Predicted intake of vegetables including legumes and excluding French fries (cup equivalents) per day'
 DSQdairy = 'Predicted intake of dairy (cup equivalents) per day'
 DSQsug = 'Predicted intake of total added sugars (tsp equivalents) per day'
 DSQssb = 'Predicted intake of added sugars from sugar-sweetened beverages (tsp equivalents) per day'
 DSQwhgr = 'Predicted intake of whole grains (ounce equivalents) per day'
 DSQfib = 'Predicted intake of fiber (gm) per day'
 DSQcalc = 'Predicted intake of calcium (mg) per day';

  *set neg to zero;
  array mpred DSQfib--DSQssb;
  do over mpred;
    if mpred ne . and mpred < 0 then mpred=0;
  end;

  DSQfib_low=lfintercept +  (kidgrp*lfkidb) + (teengrp*lfteenb)  + (gfb1f*lfcer1b) + (gfb2f*lfcer2b) + (gfb3f*lfcer3b) + (gwhgbrd*lfwgbb) + (gbrrice*lfbrricb) +
     (gcheese*lfcheesb) +  (gpizza*lfpizzab) +  (gmilk*lfmilkb) +  (gicecrm*lficecrb) +  (gpopcorn*lfpcornb) +
     (gsoda*lfsodab) +  (genergy*lfspdrb) +  (gcake*lfcakeb) +  (gdonut*lfdonutb) +  (gswtct*lfswctb) +  (gcandy*lfcandyb) +
     (gfrtjc*lffjcb) +  (gfruit*lffruitb)  +  (gsalad*lfsaladb) + (gothpot*lfothptb) +  (gbean*lfbeanb) +
     (gothveg*lfothvgb) +  (gfrfry*lffrfrb) +  (gtomsc*lftomscb) +  (gsalsa*lfsalsab) ;

  DSQcalc_low=lcintercept +  (kidgrp*lckidb) + (teengrp*lcteenb)  + (gcm1f*lccer1b) + (gcm2f*lccer2b) + (gcm3f*lccer3b) + (gwhgbrd*lcwgbb) + (gbrrice*lcbrricb) +
     (gcheese*lccheesb) +  (gpizza*lcpizzab) +  (gmilk*lcmilkb) +  (gicecrm*lcicecrb) +  (gpopcorn*lcpcornb) +
     (gsoda*lcsodab) +  (genergy*lcspdrb) +  (gcake*lccakeb) +  (gdonut*lcdonutb) +  (gswtct*lcswctb) +  (gcandy*lccandyb) +
     (gfrtjc*lcfjcb) +  (gfruit*lcfruitb)  +  (gsalad*lcsaladb) + (gothpot*lcothptb) +  (gbean*lcbeanb) +
     (gothveg*lcothvgb) +  (gfrfry*lcfrfrb) +  (gtomsc*lctomscb) +  (gsalsa*lcsalsab) ;

  DSQwhgr_low=lgintercept +  (kidgrp*lgkidb) + (teengrp*lgteenb)  + (gwg1f*lgcer1b) + (gwg2f*lgcer2b) + (gwg3f*lgcer3b) + (gwhgbrd*lgwgbb) + (gbrrice*lgbrricb) +
      (gpopcorn*lgpcornb)  ;

  DSQsug_low=lsintercept +  (kidgrp*lskidb) + (teengrp*lsteenb)  + (sas1f*lscer1b) + (sas2f*lscer2b) + (sas3f*lscer3b) +
     (sicecrm*lsicecrb) +  (ssoda*lssodab) +  (senergy*lsspdrb) +  (scake*lscakeb) +  (sdonut*lsdonutb) +  (sswtct*lsswctb) +  (scandy*lscandyb) ;

  DSQdairy_low=ldintercept +   (kidgrp*ldkidb) + (teengrp*ldteenb)  + (dcheese*ldcheesb) +  (dpizza*ldpizzab) +  (dmilk*ldmilkb) +  (dicecrm*ldicecrb)  ;

  DSQfvl_low=lpintercept +   (kidgrp*lpkidb) + (teengrp*lpteenb) +
     (pfrtjc*lpfjcb) +  (pfruit*lpfruitb)  +  (psalad*lpsaladb) + (pothpot*lpothptb) +  (pbean*lpbeanb) +
     (pothveg*lpothvgb) +  (pfrfry*lpfrfrb) +  (ptomsc*lptomscb) +  (psalsa*lpsalsab) +  (ppizza*lppizzab) ;

  DSQvlall_low=lvintercept +   (kidgrp*lvkidb) + (teengrp*lvteenb) +
     (vsalad*lvsaladb) + (vothpot*lvothptb) +  (vbean*lvbeanb) +  (vpizza*lvpizzab) +
     (vothveg*lvothvgb) +  (vfrfry*lvfrfrb) +  (vtomsc*lvtomscb) +  (vsalsa*lvsalsab) ;

  DSQfvlnf_low=lnintercept +   (kidgrp*lnkidb) + (teengrp*lnteenb) +
     (pfrtjc*lnfjcb) +  (pfruit*lnfruitb)  +  (psalad*lnsaladb) + (pothpot*lnothptb) +  (pbean*lnbeanb) +
     (pothveg*lnothvgb) +  (ptomsc*lntomscb) +  (psalsa*lnsalsab) + (ppizza*lnpizzab) ;

  DSQvlnf_low=luintercept +   (kidgrp*lukidb) + (teengrp*luteenb) +
     (vsalad*lusaladb) + (vothpot*luothptb) +  (vbean*lubeanb) +  (vpizza*lupizzab) +
     (vothveg*luothvgb) +  (vtomsc*lutomscb) +  (vsalsa*lusalsab) ;

  DSQfrt_low=lrintercept +   (kidgrp*lrkidb) + (teengrp*lrteenb)  + (ffrtjc*lrfjcb) +  (ffruit*lrfruitb)  ;

  DSQssb_low=lxintercept +  (kidgrp*lxkidb) + (teengrp*lxteenb) +  (ssoda*lxsodab) +  (senergy*lxspdrb) + (sswtct*lxswctb)  ;

  label
 DSQfvl_low ='Predicted probability of eating less than 1.7 cup equivalents of fruits and vegetables including legumes and French fries'
 DSQfvlnf_low ='Predicted probability of eating less than 1.7 cup equivalents fruits and vegetables including legumes and excluding French fries'
 DSQfrt_low ='Predicted probability of eating less than 0.5 cup equivalents of fruits'
 DSQvlall_low ='Predicted probability of eating less than 1.0 cup equivalents of vegetables including legumes and French fries'
 DSQvlnf_low ='Predicted probability of eating less than 1.0 cup equivalents vegetables including legumes and excluding French fries'
 DSQdairy_low ='Predicted probability of eating less than 1.2 cup equivalents of dairy'
 DSQsug_low ='Predicted probability of eating less than 11 tsp equivalents of total added sugars'
 DSQssb_low ='Predicted probability of eating less than 3 tsp equivalents added sugars from sugar-sweetened beverages'
 DSQwhgr_low ='Predicted probability of eating less than 0.3 ounce equivalents of whole grains'
 DSQfib_low ='Predicted probability of eating less than 12 grams of fiber'
 DSQcalc_low ='Predicted probability of eating less than 800 milligrams of calcium';

  array lpred DSQfib_low--DSQssb_low;
  do over lpred;
    if lpred ne . then do;

  if lpred < -100 then
    lpred = exp(-100)/(1+exp(-100));
   else if lpred > 100 then
    lpred = exp(100)/(1+exp(100));
   else  lpred = exp(lpred)/(1+exp(lpred));
   end;
  end;


  DSQfib_high=ufintercept +  (kidgrp*ufkidb) + (teengrp*ufteenb)  + (gfb1f*ufcer1b) + (gfb2f*ufcer2b) + (gfb3f*ufcer3b) + (gwhgbrd*ufwgbb) + (gbrrice*ufbrricb) +
     (gcheese*ufcheesb) +  (gpizza*ufpizzab) +  (gmilk*ufmilkb) +  (gicecrm*uficecrb) +  (gpopcorn*ufpcornb) +
     (gsoda*ufsodab) +  (genergy*ufspdrb) +  (gcake*ufcakeb) +  (gdonut*ufdonutb) +  (gswtct*ufswctb) +  (gcandy*ufcandyb) +
     (gfrtjc*uffjcb) +  (gfruit*uffruitb)  +  (gsalad*ufsaladb) + (gothpot*ufothptb) +  (gbean*ufbeanb) +
     (gothveg*ufothvgb) +  (gfrfry*uffrfrb) +  (gtomsc*uftomscb) +  (gsalsa*ufsalsab) ;

  DSQcalc_high=ucintercept +  (kidgrp*uckidb) + (teengrp*ucteenb)  + (gcm1f*uccer1b) + (gcm2f*uccer2b) + (gcm3f*uccer3b) + (gwhgbrd*ucwgbb) + (gbrrice*ucbrricb) +
     (gcheese*uccheesb) +  (gpizza*ucpizzab) +  (gmilk*ucmilkb) +  (gicecrm*ucicecrb) +  (gpopcorn*ucpcornb) +
     (gsoda*ucsodab) +  (genergy*ucspdrb) +  (gcake*uccakeb) +  (gdonut*ucdonutb) +  (gswtct*ucswctb) +  (gcandy*uccandyb) +
     (gfrtjc*ucfjcb) +  (gfruit*ucfruitb)  +  (gsalad*ucsaladb) + (gothpot*ucothptb) +  (gbean*ucbeanb) +
     (gothveg*ucothvgb) +  (gfrfry*ucfrfrb) +  (gtomsc*uctomscb) +  (gsalsa*ucsalsab) ;

  DSQwhgr_high=ugintercept +  (kidgrp*ugkidb) + (teengrp*ugteenb)  + (gwg1f*ugcer1b) + (gwg2f*ugcer2b) + (gwg3f*ugcer3b) + (gwhgbrd*ugwgbb) + (gbrrice*ugbrricb) +
      (gpopcorn*ugpcornb)  ;

  DSQsug_high=usintercept +  (kidgrp*uskidb) + (teengrp*usteenb)  + (sas1f*uscer1b) + (sas2f*uscer2b) + (sas3f*uscer3b) +
     (sicecrm*usicecrb) +  (ssoda*ussodab) +  (senergy*usspdrb) +  (scake*uscakeb) +  (sdonut*usdonutb) +  (sswtct*usswctb) +  (scandy*uscandyb) ;

  DSQdairy_high=udintercept +   (kidgrp*udkidb) + (teengrp*udteenb)  + (dcheese*udcheesb) +  (dpizza*udpizzab) +  (dmilk*udmilkb) +  (dicecrm*udicecrb)  ;

  DSQfvl_high=upintercept +   (kidgrp*upkidb) + (teengrp*upteenb) +
     (pfrtjc*upfjcb) +  (pfruit*upfruitb)  +  (psalad*upsaladb) + (pothpot*upothptb) +  (pbean*upbeanb) +
     (pothveg*upothvgb) +  (pfrfry*upfrfrb) +  (ptomsc*uptomscb) +  (psalsa*upsalsab) +  (ppizza*uppizzab) ;

  DSQvlall_high=uvintercept +   (kidgrp*uvkidb) + (teengrp*uvteenb) +
     (vsalad*uvsaladb) + (vothpot*uvothptb) +  (vbean*uvbeanb) +  (vpizza*uvpizzab) +
     (vothveg*uvothvgb) +  (vfrfry*uvfrfrb) +  (vtomsc*uvtomscb) +  (vsalsa*uvsalsab) ;

  DSQfvlnf_high=unintercept +   (kidgrp*unkidb) + (teengrp*unteenb) +
     (pfrtjc*unfjcb) +  (pfruit*unfruitb)  +  (psalad*unsaladb) + (pothpot*unothptb) +  (pbean*unbeanb) +
     (pothveg*unothvgb) +  (ptomsc*untomscb) +  (psalsa*unsalsab) + (ppizza*unpizzab) ;

  DSQvlnf_high=uuintercept +   (kidgrp*uukidb) + (teengrp*uuteenb) +
     (vsalad*uusaladb) + (vothpot*uuothptb) +  (vbean*uubeanb) +  (vpizza*uupizzab) +
     (vothveg*uuothvgb) +  (vtomsc*uutomscb) +  (vsalsa*uusalsab) ;

  DSQfrt_high=urintercept +   (kidgrp*urkidb) + (teengrp*urteenb)  + (ffrtjc*urfjcb) +  (ffruit*urfruitb)  ;

  DSQssb_high=uxintercept +  (kidgrp*uxkidb) + (teengrp*uxteenb) +  (ssoda*uxsodab) +  (senergy*uxspdrb) + (sswtct*uxswctb)  ;

  label
 DSQfvl_high ='Predicted probability of eating equal or more than 3.2 cup equivalents of fruits and vegetables including legumes and French fries'
 DSQfvlnf_high ='Predicted probability of eating equal or more than 3.2 cup equivalents fruits and vegetables including legumes and excluding French fries'
 DSQfrt_high ='Predicted probability of eating equal or more than 1.4 cup equivalents of fruits'
 DSQvlall_high ='Predicted probability of eating equal or more than 1.8 cup equivalents of vegetables including legumes and French fries'
 DSQvlnf_high ='Predicted probability of eating equal or more than 1.8 cup equivalents vegetables including legumes and excluding French fries'
 DSQdairy_high ='Predicted probability of eating equal or more than 2.4 cup equivalents of dairy'
 DSQsug_high ='Predicted probability of eating equal or more than 23 tsp equivalents of total added sugars'
 DSQssb_high ='Predicted probability of eating equal or more than 11 tsp equivalents added sugars from sugar-sweetened beverages'
 DSQwhgr_high ='Predicted probability of eating equal or more than 1.0 ounce equivalents of whole grains'
 DSQfib_high ='Predicted probability of eating equal or more than 19 grams of fiber'
 DSQcalc_high ='Predicted probability of eating equal or more than 1100 milligrams of calcium';

  array upred DSQfib_high--DSQssb_high;
  do over upred;
    if upred ne . then do;

  if upred < -100 then
    upred = exp(-100)/(1+exp(-100));
   else if upred > 100 then
    upred = exp(100)/(1+exp(100));
   else  upred = exp(upred)/(1+exp(upred));
   end;
  end;

run;



/*show results of scoring algorithm;
*/
proc means n nmiss min max mean;
  by gender;
  var DSQfib--DSQssb_high;
  title2 'predicated intake based on screener responses';
  format gender gender.;
run;
