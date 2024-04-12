# Building_CAD - QGIS Plugin [English version]

## Introduction
QGIS plugin developed by Kalundborg Municipality for digitization of buildings from two known reference points such as cadastral boundaries. 
Although the Building_cad plugin is developed with the purpose of digitizing buildings, the tool can still be used for digitizing other objects from known reference points.
The plugin has been tested on QGIS versions 3.16 to 3.36.1 and work with these versions of QGIS. The plugin is still undergoing development.

![BuildingCAD](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/de0bd78fab3844e59e79081090b15312/data "BuildingCAD QGIS plugin")

## How to install the plugin:

**1 -** Download the plugin as a .zip file by clicking on the "<> code" button and then "Download ZIP.

![BuildingCAD](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/34d8fe63c7bd4daa8a4ec5d59e7c2064/data "BuildingCAD QGIS plugin")


**2 -** Open QGIS. Go to the plugins menu by clicking on "plugins" -> "Manage and Install Plugins..." from the top menu.

![BuildingCAD](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/ab4c9e762e214326b8e5978bc0cdd344/data "BuildingCAD QGIS plugin")


**3 -** In the plugins menu choose **"Install from ZIP"** and locate the downloaded .zip file and install the plugin directly from the .zip file without unzipping.

![BuildingCAD icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1ec91e39f91c44c79de57d5a6899f2a4/data "BuildingCAD QGIS plugin icon")


**4 -** The plugin is now ready to use.


## How to use the plugin:
**1 -** Open the plugin by clicking on the icon ![BuildingCAD icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/58dac571dae0474092b1b91e807343b6/data "BuildingCAD QGIS plugin icon") or click on "Plugins" in the top menu and click on "BuildingCAD" in the dropdown.

**NOTE - If you don't see neither the icon** ![BuildingCAD icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/58dac571dae0474092b1b91e807343b6/data "BuildingCAD QGIS plugin icon") **or "BuildingCAD" in "Plugins" then open the plugins menu by clicking on "plugins" -> "Manage and Install Plugins..." from the top menu.**
**In the plugins menu click "Installed" and locate BuildingCAD in the pluginlist and make sure to checkmark the plugin to make it active**

![QGIS installed apps](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/0b5ef598ff7f4097899ce83f46d53061/data "QGIS installed apps")


**2 -** Once the plugin is opened the user can use select a start and end reference point by clicking the buttons "Select from map canvas". Clicking the button will minimize the plugin and allow the user to select a point in the map canvas with snapping turned on. Once both reference points is set you should see a red reference line marking the distance betweeen the points. With the reference points set the angle between them is calculated.
**Both reference needs to be set for the plugin to work as intended.**

![Set reference points](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/c34703d703804a7eb1a552dffc4817ba/data "Set reference points")


**3 -** Next step is to start placing some construction/building points using the two lineedits for **"Distance from start"** and **"Distance in direction"**.
Distance from start indicates the distance from the start reference point towards the end reference point in meters using the exact angle. It's possible to use decimal numbers and negative numbers aswell.
Distance in direction indicates the perpendicular distance from the red reference line in meters. Here it's also possible to use decimal numbers and negative numbers aswell. Positive numbers will place the point to the right side of the red reference line. Negitive numbers will place the point to the left side of the reference line.
Click the "Place a building point" button to place the point.
It's possible to use the same reference points to place multiple points or you can use the "Clear angel to set new reference points" button so set new reference points.

**Note - Use . and not , as a seperator for decimal numbers**

![Placing construction/builing point](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/d32c7cdc908a464390fe64d643086003/data "Placing construction/builing point")

**4 -** All the construction/building points will be in a temporary scratch layer called **"building_point_layer"** which is added to the QGIS project. There will also be created a temporary scratch layer called **"dot_layer"** with points placed along the red reference line and indicates the "distance from start".
Now the user can close down the plugin and use the regular polygon tool to draw and connect the building points in the right order to construct a polygon.

![temp layers created](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/88b03443f79344cab2670c448e75723d/data "temp layers created")
![Connecting points to polygon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/2b43db14b9af4a76923dccbe3a1e6afe/data "Connecting points to polygon")


# Bygnings_CAD - QGIS Plugin [Dansk version]

## Introduktion
QGIS plugin udviklet af Kalundborg Kommune til digitalisering af bygninger ud fra 2 kendte referencepunkter som f.eks. matrikelskel.
Selvom Building_cad pluginnet er udviklet med det formål at digitalisere bygninger, kan værktøjet stadig bruges til digitalisering af andre objekter fra kendte referencepunkter.
Pluginnet er blevet testet på QGIS versioner fra 3.16 til 3.36.1 og fungerer med disse versioner af QGIS. Pluginnet er stadig under udvikling.

![BuildingCAD](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/de0bd78fab3844e59e79081090b15312/data "BuildingCAD QGIS plugin")

## Sådan installeres pluginnet:

**1 -** Download pluginnet som en .zip fil ved at klikke på knappen "<> kode" og derefter "Download ZIP".

![BuildingCAD](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/34d8fe63c7bd4daa8a4ec5d59e7c2064/data "BuildingCAD QGIS plugin")

**2 -** Åbn QGIS. Gå til plugin-menuen ved at klikke på "plugins" -> "Administrer og installer plugins..." fra øverste menu.

![BuildingCAD](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/ab4c9e762e214326b8e5978bc0cdd344/data "BuildingCAD QGIS plugin")

**3 -** I plugin-menuen vælges **"Installér fra ZIP"** og lokaliser den downloadede .zip-fil og installer pluginnet direkte fra .zip-filen uden at udpakke.

![BuildingCAD icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/1ec91e39f91c44c79de57d5a6899f2a4/data "BuildingCAD QGIS plugin icon")

**4 -** Pluginnet er nu klar til brug.

## Sådan bruges pluginnet:
**1 -** Åbn plugin'et ved at klikke på ikonet ![BuildingCAD icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/58dac571dae0474092b1b91e807343b6/data "BuildingCAD QGIS plugin icon") eller klik på "Plugins" i topmenuen og klik på "BuildingCAD" i rullemenuen.

**BEMÆRK - Hvis du ikke ser hverken ikonet ![BuildingCAD icon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/58dac571dae0474092b1b91e807343b6/data "BuildingCAD QGIS plugin icon") eller "BuildingCAD" i "Plugins", så åbn plugin-menuen ved at klikke på "plugins" -> "Administrer og installer plugins..." fra øverste menu.**
**I plugin-menuen klikkes på "Installeret" og find BuildingCAD i pluginlisten og sørg for at sætte et flueben ved pluginnet for at gøre det aktivt**

![QGIS installed apps](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/0b5ef598ff7f4097899ce83f46d53061/data "QGIS installed apps")

**2 -** Når pluginnet er åbnet, kan brugeren vælge et start- og slutreferencepunkt ved at klikke på knapperne "Select from map canvas". At klikke på knappen vil minimere pluginnet og tillade brugeren at vælge et punkt på kortlærredet med snap-funktionen aktiveret. Når begge referencepunkter er sat, bør du se en rød referencelinje, der markerer afstanden mellem punkterne. Med referencepunkterne sat beregnes vinklen mellem dem.
**Begge referencepunkter skal være sat for at pluginnet fungerer som tiltænkt.**

![Set reference points](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/c34703d703804a7eb1a552dffc4817ba/data "Set reference points")

**3 -** Næste skridt er at begynde at placere nogle konstruktions-/bygningspunkter ved hjælp af de to tekstfelter for **"Distance from start"** og **"Distance in direction"**.
Afstand fra start angiver afstanden fra startreferencepunktet mod slutreferencepunktet i meter ved hjælp af den eksakte vinkel. Det er muligt at bruge decimaltal og negative tal.
Afstand i retning angiver den vinkelrette afstand fra den røde referencelinje i meter. Her er det også muligt at bruge decimaltal og negative tal. Positive tal vil placere punktet til højre side af den røde referencelinje. Negative tal vil placere punktet til venstre side af referencelinjen.
Klik på knappen "Place a building point" for at placere punktet.
Det er muligt at bruge de samme referencepunkter til at placere flere punkter, eller du kan bruge knappen "Clear angel to set new reference points" for at sætte nye referencepunkter.

**Bemærk - Brug . og ikke , som separator for decimaltal**

![Placing construction/builing point](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/d32c7cdc908a464390fe64d643086003/data "Placing construction/builing point")

**4 -** Alle konstruktions-/bygningspunkterne vil være i et midlertidigt skratch-lag kaldet **"building_point_layer"**, som tilføjes til QGIS-projektet. Der vil også blive oprettet et midlertidigt skratch-lag kaldet **"dot_layer"** med punkter placeret langs den røde referencelinje og angiver "afstand fra start".
Nu kan brugeren lukke plugin'et ned og bruge det almindelige polygonværktøj til at tegne og forbinde bygningspunkterne i den rigtige rækkefølge for at konstruere et polygon.

![temp layers created](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/88b03443f79344cab2670c448e75723d/data "temp layers created")
![Connecting points to polygon](https://kalundborg.maps.arcgis.com/sharing/rest/content/items/2b43db14b9af4a76923dccbe3a1e6afe/data "Connecting points to polygon")
