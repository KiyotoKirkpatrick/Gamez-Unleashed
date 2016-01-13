# -------------------------------------------------------------------------------------
#
# Copyright (c) 2014, Kiyoto Kirkpatrick
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# -------------------------------------------------------------------------------------
import sys, glob
import math

def plugin_main (timg, tdrawable, inputTitle):
    twidth = tdrawable.width
    theight = tdrawable.height
    timg.disable_undo()


    # Grab the pasted image and create a new layer for it.
    floatingCover = pdb.gimp_image_get_floating_sel(timg)

    # Get the length of the input text to make sure it isn't too long.
    inputTitleLength = len(inputTitle)
    acceptableInputTitleLength = (inputTitleLength <= 85)

    if (floatingCover is not None and acceptableInputTitleLength):
        pdb.gimp_floating_sel_to_layer(floatingCover)

        # Grab the newly created layer
        imageArray = timg.layers
        coverArtLayer = imageArray[0]

        # Remove any extra layers.
        imageArrayLength = len(imageArray)
        if imageArrayLength > 2:
            i = 1
            while i < imageArrayLength - 1:
                timg.remove_layer(imageArray[i])
                i += 1


        # Get cover art dimensions and ratio to determine which style cover
        currentWidth = coverArtLayer.width
        currentHeight = coverArtLayer.height
        currentRatio = (float(currentWidth) / float(currentHeight))

        targetWidth = float(1.0)
        targetHeight = float(1.0)

        targetCoverX = 1
        targetCoverY = 1

        # Standard size cover art
        if 0.7 < currentRatio < 0.8:
            targetWidth = float(1000)
            targetHeight = float(1400)

            targetCoverX = 2020
            targetCoverY = 685

        # PS3 size cover art
        elif 0.8 < currentRatio < 0.9:
            targetWidth = float(1160)
            targetHeight = float(1340)

            targetCoverX = 1940
            targetCoverY = 700

        # Weird Amazon square covers with white space
        elif 0.9 < currentRatio < 1.1:
            targetWidth = float(1400)
            targetHeight = float(1400)

            targetCoverX = 1800
            targetCoverY = 690

        else:
            pdb.gimp_message("Error:\n    Unknown image size.\n    Please try again.")



        # pdb.gimp_message("Ratio is %s, Targets are: %s, %s" % (currentRatio, targetWidth, targetHeight))


        # Scale the layer if it's not the correct size
        if (currentWidth != targetWidth or currentHeight != targetHeight):
            pdb.gimp_layer_scale(coverArtLayer, targetWidth, targetHeight, True)


        # Move the cover art layer to the correct place.
        cover_x_off, cover_y_off = coverArtLayer.offsets
        if (targetCoverX != cover_x_off or targetCoverY != cover_y_off):
            pdb.gimp_layer_translate(coverArtLayer, targetCoverX - cover_x_off, targetCoverY - cover_y_off)




        # Create the title text for the spine
        layer_title = pdb.gimp_layer_new(timg, 1488, 225, 1, "Title Text", float(100), 0)
        timg.add_layer(layer_title, -1)
        title = pdb.gimp_text_fontname(timg, layer_title, 0, 0, inputTitle, 0, True, float(75), 0, "Sans")

        # Resize the text box to fit inside the text layer
        pdb.gimp_text_layer_resize(title, 1488, 225)

        # Anchor the floating text layer
        floatingText = pdb.gimp_image_get_floating_sel(timg)
        pdb.gimp_floating_sel_anchor(floatingText)

        # Rotate the text 90 degrees
        pdb.gimp_item_transform_rotate_simple(layer_title, 0, True, 0, 0)

        # We created the title at the top left corner of the image, so
        # move the title layer to the correct place.
        targetTitleY = 640

        # Change X the location of text depending on how long the text is.
        if (inputTitleLength <= 45):
            targetTitleX = 1440
        else:
            targetTitleX = 1483
        title_x_off, title_y_off = layer_title.offsets
        pdb.gimp_layer_translate(layer_title, targetTitleX - title_x_off, targetTitleY - title_y_off)





    elif (not acceptableInputTitleLength):
        pdb.gimp_message("Error:\n    Title text too long.\n    Please try again.")


    else:
        pdb.gimp_message("Error:\n    Cannot find pasted image.\n    Please try again.")




    # Re-enable Undoing.
    timg.enable_undo()

    # ---------------------------- END PLUGIN_MAIN() ----------------------------


try:
    # succeeds if path includes gimpfu (ie invoked from Gimp app as a plugin)
    from gimpfu import *

    register(
        "python_fu_Standard_Cover",
        "Create Incomplete Standard Size Cover from image and text",
        "Create Incomplete Standard Size Cover: Paste Cover Art into GIMP, run this program, enter Title, and hit OK.",
        "Kiyoto Kirkpatrick",
        "Copyright 2014 Kiyoto Kirkpatrick",
        "2014",
        "<Image>/Gamez Unleashed/Incomplete Standard Cover",
        "RGB*, GRAY*",
        [
            (PF_STRING, "inputTitle", "Game Title:", "Temp - Temporary Title"),
        ],
        [],
        plugin_main)

    main()

except:
    '''
    invoked standalone.  For testing, you might call plug-in main with testing parameters,
    but you would first need to import the proper PyGimp modules,
    so its unless your plugin doesn't do much with Gimp,
    its easier to test invoked from Gimp.
    '''
    pass
