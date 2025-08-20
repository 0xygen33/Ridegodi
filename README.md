# RideGodi

Repository for Ridegodi 

THIS IS JUST THE GITHUB REPOST WITH THE COMPILED VERSION OF THE SOURCE CODE

downloads: check the releases

updates (future use): pretty sure they won't get released

We have to be thankful to https://honey.noblogs.org/ (it should be public) that gave us some interesting starting points.

The app is nothing special:

The <b>TOT_BIKES.txt</b> contains the keys associated to the bikes, if you feel more confortable in writing your own bluetooth communicating app go ahead and just use these codes <code>(bikeID, macAddress,key)</code><br>. How we managed to obtain this stuff? Well, for now visit the blog above and start thinking, not so easy but you can have fun even with other protocols. 

The <b>main.py</b> is the driving program to comunicate via bluetooth with the bike, I didn't implement the scan option due to
errors in some devices.<br>

The compilation is not straightforward, the app is written with the kivy library that allows writing python apps for android.<br>
Buildozer is the tool used to compile, it allows automatization in all the stuff required for the building process.
