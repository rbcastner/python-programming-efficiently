
import os, sys, re, io, base64
import requests, bs4
import PIL, PIL.Image, PIL.ImageOps, PIL.ImageEnhance

def getday(day):
    """Load the webpage collecting Curiosity Front Hazard Cam
    images for Sol day, and yield a sequence of URLs for (left,right) pairs.
    Before loading, see if the webpage is available in a local cache."""
    
    cached = os.path.join('..','03_05','images',str(day) + '.html')
    try:
        text = open(cached,'r').read()
    except FileNotFoundError:
        daypage = requests.get('http://mars.nasa.gov/msl/multimedia/raw',
                               params={'s': day,'camera': 'FHAZ'})
        text = daypage.text
    
    soup = bs4.BeautifulSoup(text,'lxml')
    srcs = [img['src'] for img in soup.find_all('img') if 'Image' in img['alt']]
    
    # drop the smaller thumbnail duplicates
    srcs = srcs[:int(len(srcs)/2)]

    # modify URLs to high-resolution images
    srcs = [re.sub('-thm','',src) for src in srcs]
    
    print("Found {} images for day {}...".format(len(srcs),day))

    # iterate over nonoverlapping pairs in the list:
    # 0,2,4,... and 1,3,5,...
    for one, two in zip(srcs[::2],srcs[1::2]):
        # we may get the left/right in the wrong order, so check the URLs
        left, right = (one, two) if 'FLB' in one else (two, one)
        
    yield left, right

def getimage(url):
    """Load a Curiosity image from url, resize it and dewarp it.
    However, first see if the image is available in a local cache."""
    
    # big = re.sub('-thm','',url)

    cached = os.path.join('..','03_05','images',os.path.basename(url))
    try:
        content = open(cached,'rb').read()
    except FileNotFoundError:
        content = requests.get(url).content
    
    img = PIL.Image.open(io.BytesIO(content))
    
    resized = img.resize((400,400))
    dewarped = img.transform((400,300),
                             PIL.Image.QUAD,data=(0,0,100,400,300,400,400,0),
                             resample=0,fill=1)
    
    return dewarped

def blend(left,right):
    """Colorize and blend left and right Curiosity images."""
    
    blend = PIL.Image.blend(PIL.ImageOps.colorize(left,(0,0,0),(255,0,0)),
                            PIL.ImageOps.colorize(right,(0,0,0),(0,255,255)),0.5)
    
    enhanced = PIL.ImageEnhance.Brightness(blend)
    
    return enhanced.enhance(1.75)