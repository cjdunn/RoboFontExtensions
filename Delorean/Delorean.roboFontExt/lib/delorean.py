# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Delorean: Interpolation Preview by CJ Dunn.
# Thanks to Frederik Berlaen and David Jonathan Ross.

from __future__ import print_function

import vanilla
from mojo.glyphPreview import GlyphPreview
from lib.UI.stepper import SliderEditIntStepper
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver, postEvent
import sys
import os

from mojo.roboFont import version








class Dialog(BaseWindowController):

    def activateModule(self):
        # init for glyphChangeObserver
        addObserver(self, "glyphChangeObserver", "currentGlyphChanged")
        addObserver(self, "glyphOutlineChangeObserver", "draw")
        addObserver(self, "checkReport", "updateReport")
        addObserver(self, "generate", "generateCallback")

    def deactivateModule(self):
        removeObserver(self, "currentGlyphChanged")
        removeObserver(self, "draw")
        removeObserver(self, "updateReport")
        removeObserver(self, "checkReport")
        removeObserver(self, "generateCallback")
        removeObserver(self, "interpSetGlyph")




    def __init__(self, value, font1, font2, available_fonts):
        self.activateModule()

        # sets initial value
        # self.redBlink = False
        global redIsOn
        redIsOn = False

        x = 10
        y = 10
        lineHeight = 23

        self.value = value
        self.font1 = font1
        self.font2 = font2
        self.available_fonts = available_fonts

        # gname1
        if CurrentGlyph() != None:
            g = CurrentGlyph()
        else:
            g = gInit

        self.gname = g

        # use minSize to make window re-sizable
        self.w = vanilla.Window(
            (400, 400),
            'Delorean: Interpolation Preview',
            minSize=(200, 200))

        # Figuring out what to display in the dropdown list
        styleNames_set = False
        familyNames_set = False
        familyNames_differ = False

        if all([f.info.styleName for f in self.available_fonts]):
            styleNames_set = True
        if all([f.info.familyName for f in self.available_fonts]):
            familyNames_set = True
            if len(set([f.info.familyName for f in self.available_fonts])) > 1:
                familyNames_differ = True

        if styleNames_set:
            # If style names are all set and family name is all the same
            # (or not set), display only the style name.
            # If family names are different, display family name & style name.
            if familyNames_set:
                if familyNames_differ:
                    fontList = ['%s %s' % (f.info.familyName, f.info.styleName) for f in self.available_fonts]
                else:
                    fontList = [f.info.styleName for f in self.available_fonts]
            else:
                fontList = [f.info.styleName for f in self.available_fonts]

        elif familyNames_set and familyNames_differ:
            # If for some reason only the family name is set, check if it is
            # different across UFOs. If it is, use it.
            fontList = [f.info.familyName for f in self.available_fonts]

        else:
            # Last resort (neither family nor style name are set), or the
            # family name is the same across UFOs (and no style name set):
            # Only display the UFO path.
            fontList = [os.path.basename(f.path) for f in self.available_fonts]

        # Dropdown menus
        w_width = self.w.getPosSize()[2]
        menu_width = w_width/2 - 15
        # It would be nice to make the dropdown respond to a width change,
        # of the window, but that is for next time.

        self.w.leftList = vanilla.PopUpButton(
            (x, y, menu_width, lineHeight), fontList,
            callback=self.font1ChangeCallback)
        self.w.leftList.set(self.available_fonts.index(font1))

        self.w.rightList = vanilla.PopUpButton(
            (-menu_width-x, y, menu_width, lineHeight), fontList,
            callback=self.font2ChangeCallback)
        self.w.rightList.set(self.available_fonts.index(font2))

        # Line Return
        y += lineHeight

        # vanilla.TextBox (not interactive field)
        self.w.gnameTextBox = vanilla.TextBox(
            (x, y, 200, lineHeight), 'Glyph name')
        self.w.valueTextBox = vanilla.TextBox(
            (x+105, y, 200, lineHeight), 'Interpolation %')

        # Line Return
        y += lineHeight

        # "Glyph name"
        self.w.gnameTextInput = vanilla.EditText(
            (x, y, 80, lineHeight),
            self.gname.name,
            callback=self.setterButtonCallback)

        # "Percentage" Slider
        # Value
        self.w.valueTextInput = SliderEditIntStepper(
            (x+105, y, -10, 22),
            minValue=-200, maxValue=400, value=50, increment=10,
            callback=self.setterButtonCallback)

        y += lineHeight
        y += 15

        # -5 from bottom
        self.w.preview = GlyphPreview((0, y, -0, -5))

        # Report
        self.w.reportText = vanilla.TextBox(
            (x, -27, 400, lineHeight), '')

        # generate instance
        self.w.generate = vanilla.Button(
            (-35, -27, 27, lineHeight),
            u"⬇", callback=self.generateCallback)

        if CurrentGlyph() != None:
            g = CurrentGlyph()
        else:
            g = gInit

        gname = g.name
        self.interpSetGlyph(gname)

        self.w.box = vanilla.Box((0, (y-9), -0, -30))
        self.setUpBaseWindowBehavior()
        self.w.open()

    # def getFontName(self, f):
    #     if f.info.familyName:
    #         family = f.info.familyName
    #     else:
    #         family = 'Family'
    #     if f.info.styleName:
    #         style = f.info.styleName
    #     else:
    #         style = 'Style'

    #     fontName = family+' '+style

    def interpSetGlyph(self, gname):
        
        font1 = self.font1
        font2 = self.font2

        if gname in font1 and gname in font2:

            i = self.interp(self.value, gname)

            # scales upm to 1000
            upm = font1.info.unitsPerEm
            scale_factor = 1000/float(upm)
            offset = (font2[gname].width) / 2

            
                           
            if version[0] >= '2':
                #updated for RF 2x 
                i.scaleBy((scale_factor, scale_factor), origin=(offset, 0))
            else:    
                #RF 1x version
                i.scale((scale_factor, scale_factor), center=(offset, 0))
                #pass
            



            self.w.preview.setGlyph(i)

            # Status: good
            reportText = u"😎"
            self.w.reportText.set(reportText)



        else:

            # Status: no good
            reportText = u"😡"
            self.w.reportText.set(reportText)

            

            # Glyphname must exist in both fonts
            pass

    def font1ChangeCallback(self, info):
        pick = info.get()
        self.font1 = self.available_fonts[pick]
        self.glyphChangeObserver(None)

    def font2ChangeCallback(self, info):
        pick = info.get()
        self.font2 = self.available_fonts[pick]
        self.glyphChangeObserver(None)

    def glyphChangeObserver(self, info):

        if CurrentGlyph() != None:
            g = CurrentGlyph()
        else:
            g = gInit

        gname = g.name

        # when glyph changes, check if it's interpolable
        self.updateReport(gname)

        self.interpSetGlyph(gname)
        # sets gname in box when glyph changes
        self.w.gnameTextInput.set(gname)

    def glyphOutlineChangeObserver(self, info):

        if CurrentGlyph() != None:
            g = CurrentGlyph()

        else:
            g = gInit

        gname = g.name

        self.interpSetGlyph(gname)


        # set gname in box when outline changes
        self.w.gnameTextInput.set(gname)

        self.updateReport(gname)

    def checkReport(self, gname):
        font1 = self.font1
        font2 = self.font2
        
        reportText = ''

        if gname in font1 and gname in font2:
            glyph1 = self.font1[gname]
            glyph2 = self.font2[gname]

            report = glyph1.isCompatible(glyph2)

            if report[0] == False:
                # no good
                reportText = u"😡 *** /" + gname + " is not compatible for interpolation ***"



            else:
                # Status: good
                reportText = u"😎"
        else:
            pass

        return reportText

    def generateCallback(self, sender):
        font1 = self.font1
        font2 = self.font2


        gname = self.w.gnameTextInput.get()

        # generates to new one
        # self.font1
        f = CurrentFont()

        pcnt = int((self.value)*100)

        instanceName = gname+'.'+str(pcnt)

        if gname in font1 and gname in font2:
            i = self.interp(self.value, gname)
            
            i.name = instanceName

            f.insertGlyph(i) 
            
#            f.insertGlyph(i, instanceName)
            
            if version >= '2':
                #updated for RF 2x 
                f.changed()
            else:
                #RF 1x version
                f.update()    
            

            print ('\nGlyph "'+instanceName+'" added to CurrentFont()')


        

    def updateReport(self, gname):

        reportText = ''
        reportText = self.checkReport(gname)
        self.w.reportText.set(reportText)

    def setterButtonCallback(self, sender):

        self.w.valueTextInput.get()

        # convert to float
        self.value = float(self.w.valueTextInput.get()) / 100

        # self.updateReport(gname)
        gname = self.w.gnameTextInput.get()

        self.interpSetGlyph(gname)

        pcnt = int(self.w.valueTextInput.get())


    def decomposeComponents(self, font, srcGlyph):
        
        #for RF3 and newer
        if version >= "3.0.0":
            from mojo.pens import DecomposePointPen
            dstGlyph = RGlyph()

            # copy the width of the source glyph to the destination glyph
            dstGlyph.width = srcGlyph.width

            # get a pen to draw into the destination glyph
            dstPen = dstGlyph.getPointPen()

            # create a decompose pen which writes its result into the destination pen
            decomposePen = DecomposePointPen(font, dstPen)

            # draw the source glyph into the decompose pen
            # which draws into the destination pen
            # which draws into the destination glyph
            srcGlyph.drawPoints(decomposePen)

        #for RF1x            
        else:
            dstGlyph = srcGlyph.copy()
            dstGlyph.naked().setParent(font)
            dstGlyph.decompose()

                                
        return dstGlyph


    def interp(self, value, gname):
        font1 = self.font1
        font2 = self.font2

        if len(font1[gname].components) > 0 or len(font2[gname].components) > 0:
            srcGlyph1 = font1[gname]
            glyph1 = self.decomposeComponents(font1, srcGlyph1)

            srcGlyph2 = font2[gname]
            glyph2 = self.decomposeComponents(font2, srcGlyph2)

        else:
            glyph1 = font1[gname]
            glyph2 = font2[gname]

        dest = RGlyph()
        dest.interpolate(value, glyph1, glyph2)

        return dest




    # do I still need this?
    def windowCloseCallback(self, sender):
        self.deactivateModule()
        BaseWindowController.windowCloseCallback(self, sender)


def runDelorean():
    # you must have 2 fonts open
    if len(AllFonts()) < 2:
        print ('Error: You must have two fonts open\nOpen two fonts and try again\n')
        #sys.exit()
        return


    else:
        af = AllFonts()
        if not all([f.path for f in af]):
            # A new font is open which never has been saved
            #sys.exit('\nError:Please save new fonts before continuing.')
            print ('\nError:Please save new fonts before continuing.')
            return


        if all([f.info.openTypeOS2WeightClass for f in af]):
            # Sorting font list by weight class if it is set
            available_fonts = AllFonts('openTypeOS2WeightClass')
        elif all([f.info.styleName for f in af]):
            # Alternatively, sorting font list by style name
            available_fonts = AllFonts('styleName')
        else:
            # If nothing is set, nothing is sorted. Could perhaps sort by
            # path, but that probably does not make a lot of sense.
            available_fonts = af

        current_index = available_fonts.index(CurrentFont())
        if current_index == len(available_fonts) - 1:
            next_index = 0
        else:
            next_index = current_index + 1

        font1 = available_fonts[current_index]
        font2 = available_fonts[next_index]


    # set Initial Glyph to notdef if it exists in font
    if len(font1.keys()) > 0:

        glyphInit = '.notdef'
        # checks to see if notdef exists
        if glyphInit in font1.keys():
            gInit = font1[glyphInit]
        else:
            # if it doesn't exist, this gets first glyph in font
            key = font1.keys()[0]
            gInit = font1[key]
    else:
        print ('Error: Both fonts must have glyphs\nDraw some glyphs and try again\n')
        #sys.exit()
        return



    # initial value for interpolation
    v = .5
    d = Dialog(v, font1, font2, available_fonts)

runDelorean()
