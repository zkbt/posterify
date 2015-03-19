'''Generate a batch of posters from a list of strings and a list of background images.

The easiest way to use this is probably to drop a copy of this file into a directory where you'd like to generate some posters, and modify the text() statements to suit your needs. To pick a font, you can use, for example "posterify.findFont('Comic Sans')" to find the font file on your computer, and then code that font path into the script.

Then, you can run "makePosters(strings=[a list of strings you'd like to see on posters], images=[a list of valid image paths for the backgrounds])" to loop through all the strings, randomly choosing from images as backgrounds for each.

Good luck! Happy postering!

[originally written by Zach Berta-Thompson, 2015]'''

# load desired font for the poster
import matplotlib.font_manager as fm
def findFont(name='Arial'):
    possiblefonts = fm.findSystemFonts()
    return [f for f in possiblefonts if name in f]
prop = fm.FontProperties(fname='/Library/Fonts/Arial.ttf')

# set the font to that font
import matplotlib
matplotlib.rcParams['font.family'] = prop.get_name()

# import various tools
import glob, os
import matplotlib.pyplot as plt, scipy.misc, numpy as np


def makePosters(strings = open('phrases.txt').readlines(),
                images = glob.glob('/Users/zkbt/Cosmos/Artwork/AstroImages/*')):
    '''Make a bunch of posters from a list of strings, choosing a random image for each.'''
    for s in strings:
        poster(s, filename=np.random.choice(images))


def poster(string='Alien  Worlds', filename='source/1.png',
            size=(8.5, 11), margin=0.5, dpi=100, channel='green'):
    '''Make a poster, given a string and an image.

    string = what to say
    filename = image to show
    size = (width, height) of poster
    margin = white space from edge of poster (same all around)
    dpi = resolution (probbaly best to keep around 100)
    channel = which of RGB colors to use, in case the input image is in color'''

    plt.ion()
    print
    print "Making a poster that says:"

    # convert double spaces into newlines
    string = string.replace('  ', '\n')
    print "--------------------------"
    print string
    print "--------------------------"

    # define some scales
    xsize = float(size[0])
    ysize = float(size[1])
    aspect = ysize/xsize

    # load the image
    image = scipy.misc.imread(filename)
    print "Using {0}, a {1} image, as a backdrop.".format(filename, image.shape)

    # create the plot
    plt.figure('poster', figsize=size, dpi=dpi)
    a = plt.subplot()
    a.cla()
    plt.setp(a.get_xticklabels(), visible=False)
    plt.setp(a.get_xticklines(), visible=False)
    plt.setp(a.get_yticklabels(), visible=False)
    plt.setp(a.get_yticklines(), visible=False)
    plt.subplots_adjust(left=margin/xsize, right=1.0 - margin/xsize, top=1.0 - margin/ysize, bottom=margin/ysize)

    # show the image, in grayscale, cropping to center
    if len(image.shape) == 2:
        print "The image appears to be black and white. How easy!"
    elif len(image.shape) == 3:
        rgb = dict(red=0, green=1, blue=2)
        print "The image appears to be a color image. Using channel={0} as black-and-white.".format(channel)
        image = image[:,:,rgb[channel.lower()]]
    else:
        print "The image has a confusing shape [{0}]. Skipping it!".format(image.shape)
        return

    # crop the image to the right aspect ratio
    imageaspect = float(image.shape[0])/float(image.shape[1])
    if imageaspect > aspect:
        # (image is taller than the poster)
        trim = (image.shape[0] - aspect*image.shape[1])/2
        image = image[trim:-trim, :]
    elif imageaspect < aspect:
        # (image is wider than the poster)
        trim = (image.shape[1] - image.shape[0]/aspect)/2
        image = image[:,trim:-trim]
    print imageaspect

    # draw the background image, using vmax=500 to keep all colors dark gray
    a.imshow(image, cmap='gray', interpolation='nearest', extent=[0, xsize, 0, ysize], vmax=500)

    # draw the text
    a.text(4.25, 0.75, 'January 2015 at MIT', fontsize=30, ha='center', weight='normal', color='white')
    a.text(4.25, 1.25, 'bit.ly/astroIAP', fontsize=60, ha='center', weight='bold', color='white')
    a.text(4.25, 9, string.upper(), fontsize=100, color='white', ha='center', weight='bold', va='top')

    # save the output posters to their own directory
    try:
        os.mkdir('outputs')
    except:
        pass
    filename = 'outputs/'+ string.replace(' ', '').replace('\n','') + '_' + filename.split('/')[-1].split('.')[0] + '.pdf'
    print "Saving poster to ", filename
    plt.savefig(filename)
    plt.draw()
