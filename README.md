# RideGodi

Repository for the new app Ridegodi 

downloads: bicigodibili.vado.li

updates (future use): biciupdates.vado.li

Here is another place where we can publish code and links.

We have to be thankful to https://honey.noblogs.org/ (it should be public) that gave us some interesting starting points.

The app is nothing special:

The <b>TOT_BIKES.txt</b> contains the keys associated to the bikes, if you feel more confortable in writing your own bluetooth communicating app go ahead and just use these codes <code>(bikeID, macAddress,key)</code><br>. How we managed to obtain this stuff? Well, for now visit the blog above and start thinking, not so easy but you can have fun even with other protocols. 

The <b>main.py</b> is the driving program to comunicate via bluetooth with the bike, I didn't implement the scan option due to
errors in some devices.<br>

The compilation is not straightforward, the app is written with the kivy library that allows writing python apps for android.<br>
Buildozer is the tool used to compile, it allows automatization in all the stuff required for the building process.