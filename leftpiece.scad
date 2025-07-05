
inch = 25.4;
EZLOKHOLE = 9;
m6hole = 6.6;

module dog_holes(dogoffset)
{
    starty = 2 * inch;
    increment = 4 * inch;
    thend = 47.5 * inch;
    for(y = [starty : increment : thend]){
       translate([dogoffset,y,-.1])cylinder(r=(.75 * inch)/2,h=1 * inch);
       }
}

module ezlock_holes(dogoffset)
{
    starty = 3 * inch;
    increment = 4 * inch;
    thend = 47.5 * inch;
    for(y = [starty : increment : thend]){
       translate([dogoffset - (2 * inch),y,-.1])cylinder(r=EZLOKHOLE/2,h=14);
       translate([dogoffset + (2 * inch),y,-.1])cylinder(r=EZLOKHOLE/2,h=14);
       translate([dogoffset - (2 * inch),y,13])cylinder(r=m6hole/2,h=10);
       translate([dogoffset + (2 * inch),y,13])cylinder(r=m6hole/2,h=10);
       }
}

module ezlock_holes_top(dogoffset)
{
    starty = 3 * inch;
    increment = 4 * inch;
    thend = 47.5 * inch;
    for(y = [starty : increment : thend]){
       translate([dogoffset - (2 * inch),y,-0.1])cylinder(r=m6hole/2,h=20);
       translate([dogoffset + (2 * inch),y,-0.1])cylinder(r=m6hole/2,h=20);
       }
}

module ezlock_holes_bottom(dogoffset)
{
    starty = 3 * inch;
    increment = 4 * inch;
    thend = 47.5 * inch;
    for(y = [starty : increment : thend]){
       translate([dogoffset - (2 * inch),y,-.1])cylinder(r=EZLOKHOLE/2,h=25);
       translate([dogoffset + (2 * inch),y,-.1])cylinder(r=EZLOKHOLE/2,h=25);
       }
}

module mount_holes(mountoffset)
{
   
    hole1 = (4 * inch);
    translate([mountoffset, hole1,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole1,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole2 = hole1 + (7.75 * inch);
    translate([mountoffset, hole2,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole2,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole3 = hole2 + (7.75 * inch);
    translate([mountoffset, hole3,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole3,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole4 = hole3 + (5.585 * inch);
    translate([mountoffset, hole4,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole4,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole5 = hole4 + (7.75 * inch);
    translate([mountoffset, hole5,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole5,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole6 = hole5 + (5.585 * inch);
    translate([mountoffset, hole6,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole6,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole7 = hole6 + (7.75 * inch);
    translate([mountoffset, hole7,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    translate([mountoffset, hole7,.5 * inch]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    
}

module mount_holes_top(mountoffset)
{
   
    hole1 = (4 * inch);
    translate([mountoffset, hole1,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    hole2 = hole1 + (7.75 * inch);
    translate([mountoffset, hole2,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    hole3 = hole2 + (7.75 * inch);
    translate([mountoffset, hole3,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    hole4 = hole3 + (5.585 * inch);
    translate([mountoffset, hole4,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    hole5 = hole4 + (7.75 * inch);
    translate([mountoffset, hole5,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    hole6 = hole5 + (5.585 * inch);
    translate([mountoffset, hole6,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
    hole7 = hole6 + (7.75 * inch);
    translate([mountoffset, hole7,-.1]) cylinder(r=6.35/2,h=.80 * inch,$fn=128);
}

module mount_holes_top2(mountoffset)
{
   
    hole1 = (4 * inch);
    translate([mountoffset, hole1,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole2 = hole1 + (7.75 * inch);
    translate([mountoffset, hole2,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole3 = hole2 + (7.75 * inch);
    translate([mountoffset, hole3,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole4 = hole3 + (5.585 * inch);
    translate([mountoffset, hole4,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole5 = hole4 + (7.75 * inch);
    translate([mountoffset, hole5,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole6 = hole5 + (5.585 * inch);
    translate([mountoffset, hole6,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    hole7 = hole6 + (7.75 * inch);
    translate([mountoffset, hole7,-.1]) cylinder(r=9.53/2,h=.80 * inch,$fn=128);
    
}

module left_slat()
{
    
    difference(){
       cube([9.875 * inch,48 * inch,.75 * inch]);
       mountoffset1 = (9.875 * inch) - (.824 * inch);
       mount_holes(mountoffset1);
       mountoffset2 = mountoffset1 - (7.102 * inch);
       mount_holes(mountoffset2);
       dog_holes((9.875 * inch) / 2);
       ezlock_holes((9.875 * inch) / 2);
       }
}

module left_slat_top1()
{
    
    difference(){
       cube([9.875 * inch,48 * inch,.75 * inch]);
       mountoffset1 = (9.875 * inch) - (.824 * inch);
       mount_holes_top(mountoffset1);
       mountoffset2 = mountoffset1 - (7.102 * inch);
       mount_holes_top(mountoffset2);
       dog_holes((9.875 * inch) / 2);
       ezlock_holes_top((9.875 * inch) / 2);
       }
}

module left_slat_top2()
{
    
    difference(){
       cube([9.875 * inch,48 * inch,.75 * inch]);
       mountoffset1 = (9.875 * inch) - (.824 * inch);
       mount_holes_top2(mountoffset1);
       mountoffset2 = mountoffset1 - (7.102 * inch);
       mount_holes_top2(mountoffset2);
       }
}

module left_slat_bot1()
{
    
    difference(){
       cube([9.875 * inch,48 * inch,.75 * inch]);
       ezlock_holes_bottom((9.875 * inch) / 2);
       }
}

//left_slat();
//projection(cut = true) left_slat_top1(); // top1
//projection() translate([0,0,12]) left_slat_top2(); // top2
projection() translate([9.875 * inch,0,0]) rotate([0,180,0]) left_slat_bot1(); // bot1