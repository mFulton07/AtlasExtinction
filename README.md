# AtlasExtinction

Before Running AtlasExtinction make sure that:

* Dustmaps has been installed in your Python Library: pip install dustmaps
* You have cc'd into the AtlasExtinction directory


To get Pan-STARRS gri-passband dust extinction (Schlafly & Finkbeiner (2011)), populate altas_object_positions.csv with: 

* A list of ATLAS Names (optional)
* RA and Dec coordinates in degrees (mandatory) 

and run get_dust_extinction.py.

Extinction values, along with the objects/coordinates listed will be visible in atlas_object_extinction.csv once get_dust_extinction.py has successfully completed.
