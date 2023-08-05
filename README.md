# MacroMap
PoC semi-automated python tool for translating and compiling wow minimap data
![kalimdor](https://cdn.discordapp.com/attachments/1063759326340186172/1137393000889208852/image.png)

# What is this?
This is a two part basic python tool for translating WoW's md5 labeled minimap tile data back into real file names.
The 2nd part of this tool will convert the blps into pngs and then compile those pngs into one large png for each zone.

# Limitations
- I don't know how to correctly extract patchs, and the expansion data over top of that. So you can have a 3.3.5 map. not just a 3.0.0 map.<br>
All testing was done on wow 3.3.5 though.<br>
(you can open and merge all MPQs with MPQeditor, but I end up with a lot of 0kb blp files and empty folders that don't have a corresponding entry in the md5 trs file. I'm getting a lot more consistent results just extracting the common MPQs)
- We are translating the md5 names for WMO's (buildings, raids, dungeons, etc) however as they are a layered map system I don't know the best way to compile them yet.
So Kalimdor has a Tanaris WMO room map folder inside it, this folder is not touched, but Kalimdor will still be converted and compiled.
And the whole WMO file is blacklisted from the macroMap script.

# Why?
Well compiling the maps in this way will give you a 1:1 scale satellite overview world map. So take the well known GM Island at the very top of Kalimdor, or the lesser known unused island at the bottom.<br>
These exported world maps are arranged and filled to scale, so you know exactly how many map tiles you have to fatigue swim to get to places. Or can more easily find other random things out in the ocean or other unused parts of the map where the game maps where "glued" together. So this makes things like flying to the other parts of Emerald Dream a little easier to navigate.<br>
So yes, if you see it on the macro map, you should be able to fly or telehack past world borders to see it in-game. As the macro map is layed out the same as it is rendered in-game.<br>
This also means we can get a complete world map of development zones as they where still in the game. So we only have one leak for the development map, but going off the minimap data, we only have around 6% of that map and the rest of the map model data is missing. Or Emerald Dream, where we can tell from the minimap that it's not meant to be this green, a lot of this neon green is because of missing textures. Textures that are shown on the minimap but not in-game anymore.<br>
On the subject of Emerald Dream, map tiles map24_27 to map24_30 and etc, the ones that are mostly black with a little bit of real map in the top corner.<br>
This is a left over very old part of development when minimap tiles where 64x64, and later in development the map tiles where expanded to 256x256 for better quality.<br>
And somewhere along the way, the minimap tool they where using incorrectly converted and scaled the old minimap data to fit the new scheme.<br>
You can sorta kinda fix this by scaling them in photoshop and re-running macroMap, but it's not the best. As it's so small I would suggest nearest neighbor scaling.<br>
Please note though for dev or unused zones in the game, the minimap data may not line up to what you are seeing in game. Either that zone never had minimap data made for it or, the zone changed over time 
and nobody updated the minimap as the zone was getting scrapped or forgotten about, like PVPZone2.<br>
Also, I just think it's neat.

# How to install and use.
I call this a semi-automated tool as you still need to extract the blps from your wow mpq files yourself.<br>
I think I could build a script to automatedly extract the data with MPQeditor however I need to correctly figure out how patch data are layered so you just point the tool at a wow folder and it figures out the rest.<br><br>

### Extracting the BLPs from the MPQs
- Download the [MPQeditor](https://github.com/MobCat/MacroMap/raw/main/mpqeditor_en_v3.6.0.868.zip) and extract it to somewhere that has more then 600MB of space left.
- Run the x64\MPQEditor.exe
- Click MPQs -> Open MPQ(s) at the top in the menu ribben
- Navigate to your wow game folder, and then the Data folder inside there.
- Hold down Ctrl and click on `common.MPQ` and then while still holding Ctrl click on `common-2.MPQ` then you can click on Open, to open both MPQs at the same time.
- This will open a window about opening multiple MPQ files at once, Check the checkbox for Merged mode and click OK
- Now use the folder tree on the left to navagate to the textuers\Minimap folder
- In this folder we can see *a lot* of "randomly" named blp files and a single `md5translate.trs` file at the end. We just want to right click on the Minimap folder in the folder tree and select Extract... This will take a few seconds, but it should compleat without any errors. We are now done with MPQ editor and we can Close the MPQ and the program it's self.
- Now in the x64 folder of MPQeditor, we should see a new `Work` folder. Inside this folder is where we want to navigate to next. Go to `Work\textures` you will see our extracted `Minimap` folder in there but we are going to be working in this `textuers` folder from now on. Windows has a mental breakdown trying to constantly index almost 13,000 files as we work on and change them<br><br>
### Renaming and sorting the BLPs<br>
- Now we want to download the [md5Fix.py](https://github.com/MobCat/MacroMap/raw/main/md5Fix.py) script from this github and place it in the texturs folder
- We can now simply run `python md5Fix.py` (Or `python3 md5Fix.py` if you are on linux for some reason) and in about 10 sec all the "random" files inside the Minimap folder will now be corecly renamed and sorted.
- If you just wanted sorted blq files for another project you can stop here. The rest of this "tutorial" is for converting and compiling these minimap files into big world map files.<br><br>

### Running macroMap to convert and compile the minimap data.
- Next we want to download the [macroMap.py](https://github.com/MobCat/MacroMap/raw/main/macroMap.py) script and [BLPConverter.exe](https://github.com/MobCat/MacroMap/raw/main/BLPConverter.exe) from this github and place them in the same textuers folder we ran the [md5Fix.py](https://github.com/MobCat/MacroMap/raw/main/md5Fix.py) script from.<br>
- If you have never ran this script before, you might need to run `pip install Pillow` to make sure you have the python image library needed to convert and compile the images.<br>
- Now we can just run `python macroMap.py` and for the next minute or so the script will work away to convert and compile the blps into map files.<br><br>
The print out will read as
```
(1/52 1%)Converting AhnQiraj
 [25/25]
(2/52 3%)Converting AhnQirajTemple
 [21/21]
(3/52 5%)Converting Azeroth
 [200/520]
```
3/52 is in refrence to the zone we are currently converting, there are 52 zones in total we are converting.<br>
[200/520] is what map tile we are currently converting from blp to png. In this case we are up to 200 out of a total of 520 for the 3rd zone in the game.<br>
Maps like development have 988 tiles and Kalimdor has 790 in patch 3.0, so a progress counter is needed as it would seem like it's spending a lot of time doing nothing.<br><br>

After the conversion is done, we will now drop into the building process.
```
(1/52 1%)Building AhnQiraj
(2/52 3%)Building AhnQirajTemple
(3/52 5%)Building Azeroth
(4/52 7%)Building Azjol_LowerCity
```
This is taking our converted png minimap tiles and compiling them into one large png file per each zone of the game. We don't need to track each tile of the zone here as this process is a little quicker<br>(well outside of the 980+ tile dev map that is).<br><br>
- Now that is all done, we can now navigate into the minimap folder. You will now see a heap of folders, one for each zone of the game.<br> In a zone folder you will see all of its converted `mapX_Y.png` files.<br>
And at the top of the folder you will see a large `!ZoneName-MacroMap.png` file.<br><br>
This naming scheme was chosen to make it both easy to find the macro maps in the soup of tile maps, or regex find, move and rename the macro maps into another folder.<br>
Please note though as some zones like NexusRaid and DalaranPrison are so small they only have one map tile. So you will end up with a macro map and a single map tile, that are the same thing..<br>
Also a reminder we are not converting and compiling the WMO folder. So those will just remain as sorted blp files.<br><br>

# TODO / improvements
Need to add a "you need to rename and sort tiles before converting them" check.<br>
Need to make checks for empty folders rather then just skipping them.<br>
Need to make a check for macroMap for if only one map tile, don't make macroMap.<br>
Should build a 3rd script to regex find, move and rename the macroMaps out of the tile folders into there own folders.<br>
Need to figure out how to compile patch data and add more robust checks for if files are being replaced, convert and compile both versions.<br>
    Part of this would be checking for and cleaning up the 0kb blps I'm getting when trying to extract patch data.
