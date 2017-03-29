
import bs4, io

import matplotlib.pyplot as pp
from mpl_toolkits.basemap import Basemap
import PIL, PIL.Image

# initialize the database of Curiosity locations.
xml = bs4.BeautifulSoup(open('locations.xml','r'),'lxml-xml')
locations = xml.find_all('location')

def findcuriosity(sol):
    """Look for a site record in locations.xml that includes the requested sol.
    Return longitude and latitude."""
    
    for location in locations:
        if int(location.startSol.string) <= int(sol) <= int(location.endSol.string):
            return float(location.lon.string), float(location.lat.string)

# load the map of Gale crater and initialize basemap
crater = PIL.Image.open('gale_themis_vis_fix_v4_reduced.png')
world = Basemap(lon_0=180)

def plotcuriosity(lon,lat):
    """Return a BytesIO buffer containing a PNG with Gale + curiosity."""
    
    pp.figure(figsize=(12,6))

    pp.imshow(crater,origin='upper',interpolation='none',
              cmap=pp.get_cmap('gray'),
              extent=[135.6,139.9,-7.5,-3.2])

    world.plot(lon,lat,'r.',latlon=True)

    pp.axis(xmin=135.6,xmax=139.9,ymin=-7.5,ymax=-3.2)
    
    buffer = io.BytesIO()
    pp.savefig(buffer,format='PNG')
    pp.close()
    
    return buffer