import os
import csv

import astropy.units as units
from astropy.coordinates import SkyCoord

from dustmaps.config import config
#Dustmap for Schlafly & Finkbeiner (2011) i.e. What is on NED
import dustmaps.sfd


#Check if Dustmaps has already been downloaded
currentPath = os.path.dirname(os.path.abspath(__file__))
dustmapsExistFlag = os.path.exists("DustMaps/")

if not dustmapsExistFlag:
    config["data_dir"] = "{pathToScript}/DustMaps/".format(pathToScript = currentPath)
    #Downloading dustmap for galactic extinction from Schlafly & Finkbeiner (SFD; 2011)
    dustmaps.sfd.fetch()
else:
    config["data_dir"] = "{pathToScript}/DustMaps/".format(pathToScript = currentPath)
#Setting the extraction query for the SFD Dustmap
extinctionMap = dustmaps.sfd.SFDQuery()


#Read CSV file of ATLAS objects and sky positions (RA and Dec in degrees, frame icrs)
listAtlasObjects = csv.DictReader(open("AtlasObjects/atlas_object_positions.csv"))
listExtinctAtlasObjects = []

for atlasObject in listAtlasObjects:
    
    atlasName = atlasObject["ATLAS Name"]
    ra = float(atlasObject["RA (degrees)"])
    dec = float(atlasObject["Dec (degrees)"])

    #Retriving the dust extinction in the line-of-sight of Atlas object from dustmaps
    coords = SkyCoord(ra*units.deg, dec*units.deg, frame="icrs")
    ebv = extinctionMap(coords)

    #Converting to individual Pan-STARRS passband extinctions. Coefficients for conversion taken from Table 6: "F99 Reddening in Different Bandpasses" of Schlafly & Finkbeiner (2011) using RV = 3.1
    atlasObject["A_g"] = round(ebv * 3.172,3)
    atlasObject["A_r"] = round(ebv * 2.271,3)
    atlasObject["A_i"] = round(ebv * 1.682,3)

    listExtinctAtlasObjects.append(atlasObject)


#Writing extinctions to CSV file
extinctionFileColumns = ['ATLAS Name','RA (degrees)','Dec (degrees)','A_g','A_r','A_i']
extinctionFileName = "AtlasObjects/atlas_object_extinctions.csv"
try:
    with open(extinctionFileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=extinctionFileColumns)
        writer.writeheader()
        for modAtlasObject in listExtinctAtlasObjects:
            writer.writerow(modAtlasObject)
except IOError:
    print("I/O error")