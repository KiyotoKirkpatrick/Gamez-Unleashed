#!/usr/bin/env python
#
# -------------------------------------------------------------------------------------
#
# Copyright (c) 2013, Kiyoto Kirkpatrick
# All rights reserved.
#
# This program is released under the terms of the GNU General Public License.
# The license terms can be found at http://www.gnu.org/licenses/gpl.txt
#
# Redistribution and use in source and binary forms, with or without modification, 
# are permitted provided that the following conditions are met:
#
#    - Redistributions of source code must retain the above copyright notice, this 
#    list of conditions and the following disclaimer.
#    - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation and/or 
#    other materials provided with the distribution.
#    - Neither the name of the author nor the names of its contributors may be used 
#    to endorse or promote products derived from this software without specific prior 
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY 
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR 
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN 
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH 
# DAMAGE.
#
# -------------------------------------------------------------------------------------

from gimpfu import *
import math
import time
import re
import os

def open_to_layer(img, layer, file, x360, ps3, imageSize, font, inputText, export_type, save_to):
    ''' Open a PNG file, a JPEG file a BMP file, or a GIF file,
        resize it, reposition it, and apply text to the image.
        Then save the image to the desktop.
    
    Parameters:
    image : image The current image.
    layer : layer The layer of the image that is selected.
    file : string The file to open in a new layer.
    '''
    # Indicates that the process has started.
    gimp.progress_init("Opening '" + file + "'...")
    
    try:
        # Open file.
        fileImage = None
        if(file.lower().endswith(('.png'))):
            fileImage = pdb.file_png_load(file, file)
        if(file.lower().endswith(('.jpeg', '.jpg'))):
            fileImage = pdb.file_jpeg_load(file, file)
        if(file.lower().endswith(('.bmp'))):
            fileImage = pdb.file_bmp_load(file, file)
        if(file.lower().endswith(('.gif'))):
            fileImage = pdb.file_gif_load(file, file)
        
        if(fileImage is None):
            gimp.message("The image could not be opened since it is not an image file.")
        else :
            # Create new layer.
            newLayer = gimp.Layer(image, "new layer", layer.width, layer.height, layer.type, layer.opacity, layer.mode)
            image.add_layer(newLayer, -1)
        
            # Put image into the new layer and anchor it.
            fileLayer = fileImage.layers[0]
            pdb.gimp_edit_copy(fileLayer)
            floater = pdb.gimp_edit_paste(newLayer, True)
	    pdb.gimp_floating_sel_anchor(floater)
        
            # Update the new layer.
            #newLayer.flush()
            #newLayer.merge_shadow(True)
            #newLayer.update(0, 0, newLayer.width, newLayer.height)
	
	
	# Check title text isn't blank, or default, and send it to add_title_text function
	# to add the text to the image, rotate it, and position it.
	
	# make black text
	fontcolor = (0, 0, 0)
	x = 1620
	y = 962
	fontname = font
	if (inputText != '' and inputText != None):
		titleTextLayer = add_title_text(img, x, y, "titleTextLayer", inputText, fontcolor, fontname)
	# end if
	
	# Merge all the visible layers into a single layer, to be able to save.
	mergedLayers = pdb.gimp_image_merge_visible_layers(img, 1)
	
	#show_text(export_type)
	#show_text(save_to)
	if (save_to != '' and save_to is not None):
		filename = "untitled"
		if (export_type != 'None'):
			if (inputText != '' and inputText != None):
				filename = inputText
			# end if
		# end if

		# make a nicer filename (after the ^ is the list of acceptable characters)
		filename = re.sub("[^a-zA-Z0-9_-]", "", filename)
		save_to = re.sub("[\\/]$", "", save_to) # remove trailing [back]slash if there is one
		filename = save_to + os.sep + filename
      
		if (export_type == 'jpg'):
			# save as jpeg
			filename = filename + ".jpg"
			# I attempted to guess at the defaults... the lists might be wrong
			pdb.file_jpeg_save(img, mergedLayers, filename, filename, 1, 0, 1, 0, "Incomplete DVD Cover", 3, 1, 0, 1) 
			#Input:
			#IMAGE	image	Input image
			#DRAWABLE	drawable	Drawable to save
			#STRING	filename	The name of the file to save the image in
			#STRING	raw_filename	The name of the file to save the image in
			#SUCCESS	quality	Quality of saved image (0 <= quality <= 1)
			#SUCCESS	smoothing	Smoothing factor for saved image (0 <= smoothing <= 1)
			#INT32	optimize	Optimization of entropy encoding parameters (0/1)
			#INT32	progressive	Enable progressive jpeg image loading (0/1)
			#STRING	comment	Image comment
			#INT32	subsmp	The subsampling option number
			#INT32	baseline	Force creation of a baseline JPEG (non-baseline JPEGs can't be read by all decoders) (0/1)
			#INT32	restart	Frequency of restart markers (in rows, 0 = no restart markers)
			#INT32	dct	DCT algorithm to use (speed/quality tradeoff)
			pass
		elif (export_type == 'png'):
			# save as PNG
			filename = filename + ".png"
			pdb.file_png_save_defaults(img, mergedLayers, filename, filename)
			# file_png_save_defaults
			# IMAGE	image	Input image
			# DRAWABLE	drawable	Drawable to save
			# STRING	filename	The name of the file to save the image in
			# STRING	raw_filename	The name of the file to save the image in
			pass
		# end if
		if (export_type != 'None'):
			pdb.gimp_image_delete(img)
		else:
			disp = gimp.Display(img)
		# end if
	# end if

    except Exception as err:
        gimp.message("Unexpected error: " + str(err))
        
# End def open_to_layer

def add_title_text(image, x, y, layer_name, text, color, fontname):
   image.undo_group_start()
   foreground = gimp.get_foreground()
   gimp.set_foreground(color)
   
   textlayer = gimp.Layer(image, layer_name, image.width, image.height, GRAYA_IMAGE, 100, NORMAL_MODE)
   image.add_layer(textlayer, -1)
   pdb.gimp_drawable_fill(textlayer, 3) # transparent fill
   
   gimp.set_background(255, 255, 255)
   gimp.set_foreground(color)
   
   floattext = pdb.gimp_text_fontname(image, textlayer, x, y, text, 1, 1, 70, PIXELS, fontname)
   pdb.gimp_text_layer_resize(floattext, 1485, 98)
   pdb.gimp_layer_resize(textlayer, floattext.width, floattext.height, -x, -y)
   
   pdb.gimp_floating_sel_anchor(floattext)
   
   gimp.set_foreground(foreground)
   image.undo_group_end()
   return textlayer
# end def add_title_text

register(
    "python_fu_DVD_Cover",
    "Create Incomplete DVD Cover from image and text",
    "Create Incomplete DVD Cover: Navigate to or drag-and-drop cover image, select Regular(X360, XB1, Wii) or small(PS3, PS4) size, type title text and rating, press apply",
    "Kiyoto Kirkpatrick",
    "Open source (BSD 3-clause license)",
    "2013",
    "<Image>/Tools/Gamez Unleashed/Incomplete Cover",
    "*",
    [
        (PF_FILE, "file", "File to open", ""),
        (PF_BOOL, "x360", "Standard Size (X360, XB1, Wii)", False),
        (PF_BOOL, "ps3", "Small Size (PS3, PS4)", False),
		(PF_RADIO, "imageSize", "Cover Size", "Standard", (("STANDARD SIZE (X360, Wii, etc.)","X360"), ("PS3 SIZE","PS3"))),
		(PF_FONT, "font", "Font", "Sans"),
        (PF_TEXT, "inputText", "Game Title (for spine)", "Input Title"),
		(PF_RADIO, "export_type", "Export as", "png", (("NONE","None"), ("JPEG","jpg"), ("PNG","png"))),
		(PF_DIRNAME, "save_to", "Export files to", ""),
    ],
    [],
    open_to_layer)

main()
