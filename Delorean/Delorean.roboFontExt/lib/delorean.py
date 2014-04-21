#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vanilla
from mojo.glyphPreview import GlyphPreview
from vanilla import Box
from lib.UI.stepper import SliderEditIntStepper
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver
import sys


#set Initial Glyph to glyphInit if it exists in font
glyphInit = '.notdef'
#checks to see if glyphInit exists
if glyphInit in CurrentFont().keys():
    gInit = CurrentFont()[glyphInit]
else:
    #if it doesn't exist, this gets first glyph in font
    key = CurrentFont().keys()[0]
    gInit = CurrentFont()[key]

class Dialog(BaseWindowController):
    
    def activateModule(self):
        #init for glyphChangeObserver
        addObserver(self, "glyphChangeObserver", "currentGlyphChanged")
        addObserver(self, "glyphOutlineChangeObserver", "draw")
        addObserver(self, "checkReport", "updateReport")
  
    
    def deactivateModule(self):
        removeObserver(self, "currentGlyphChanged")
        removeObserver(self, "draw")            
        removeObserver(self,  "updateReport")
        
        removeObserver(self,  "interpSetGlyph")
    

    def __init__(self, value, font1, font2):
        self.activateModule()
       
        
        x = 10
        y = 10
        yInit = y
        lineHeight = 23
        
       
        self.value = value
        self.font1 = font1 
        self.font2 = font2
        
        self.offset = ''
        
        #gname1
        if CurrentGlyph() != None:
            g = CurrentGlyph()

        else:
            g = gInit
                   
        self.gname = g

        #use minSize to make window re-sizable        
        self.w = vanilla.Window((400,400), 'Delorean: Interpolation Preview', minSize=(200,200))
        
        self.w.oneTextBox = vanilla.TextBox((x, y, 200, lineHeight), '[1] '+font1.info.fullName)
        self.w.twoTextBox = vanilla.TextBox((x+200, y, 200, lineHeight), '[2] '+font2.info.fullName)
             
        #Line Return
        y += lineHeight
        
        #vanilla.TextBox (not interactive field)
        self.w.gnameTextBox = vanilla.TextBox((x, y, 200, lineHeight), 'Glyph name')
        self.w.valueTextBox = vanilla.TextBox((x+105, y, 200, lineHeight), 'Interpolation %')
        
        #Line Return
        y += lineHeight
        
        
        # "Glyph name"
        self.w.gnameTextInput = vanilla.EditText((x, y, 80, lineHeight), self.gname.name , callback=self.setterButtonCallback)        
        
        # "Percentage" Slider
        #Value
        self.w.valueTextInput = SliderEditIntStepper((x+105, y, -10, 22), minValue=-200, maxValue=400, value=50, increment=10, callback=self.setterButtonCallback)
        
        y += lineHeight
        y += 15
    
        
        #-5 from bottom
        self.w.preview = GlyphPreview((0, y, -0, -5) )
        
        #Report
        self.w.reportText = vanilla.TextBox((x, -27, 400, lineHeight), '')

        if CurrentGlyph() != None:
            g = CurrentGlyph()
        else:
            g = gInit 

        gname = g.name

        self.interpSetGlyph(gname)


        self.w.box = Box((0, (y-9), -0, -30))

        self.setUpBaseWindowBehavior()    
        self.w.open()
 


    def interpSetGlyph(self, gname):
        if gname in font1 and gname in font2:
                    
            i = self.interp(self.value, gname)        
                        
            #scales upm to 1000
            upm = font1.info.unitsPerEm
            self.offset = (font2[gname].width) / 2
                
            i.scale(( (1000/float(upm)),(1000/float(upm)))  ,  center=(self.offset, 0)   )

            self.w.preview.setGlyph(i)
            
            #Status: good
            reportText = u"✓"
            self.w.reportText.set(reportText)
        else:
            #Status: no good
            reportText = u"☒"
            self.w.reportText.set(reportText)
            
            #Glyphname must exist in both fonts
             
            pass


    def glyphChangeObserver(self, info):
        
        #gname3
        if CurrentGlyph() != None:
            g = CurrentGlyph()
            

        else:
            g = gInit
        
            
        gname = g.name 
        
        #when glyph changes, check if it's interpolable
        self.updateReport(gname)
        self.interpSetGlyph(gname)

        #sets gname in box when glyph changes
        self.w.gnameTextInput.set(gname)
        
        
    def glyphOutlineChangeObserver(self, info):
        
        #gname4
        if CurrentGlyph() != None:
            g = CurrentGlyph()

        else:
            g = gInit 
                  
        gname = g.name 

        self.interpSetGlyph(gname)        
        #print 'glyphOutlineChangeObserver'
        #3
        
        #set gname in box when outline changes
        self.w.gnameTextInput.set(gname)
        
        self.updateReport(gname)


    def checkReport(self, gname):
        reportText = ''

        glyph1 = self.font1[gname]
        glyph2 = self.font2[gname]
        
        report = glyph1.isCompatible(glyph2)
        if report[0] == False:
            reportText = u"☒ *** /" + gname + " is not compatible for interpolation ***" 
        
        else:
            #Status: good
            reportText = u"✓"
        
        return reportText
            

    def updateReport(self, gname):
        reportText = ''
        reportText = self.checkReport(gname)
        self.w.reportText.set(reportText)
        
        
    def setterButtonCallback(self, sender):
        
        self.w.valueTextInput.get()        
        
        
        #convert to float
        self.value = float(self.w.valueTextInput.get()) / 100
        
        #self.updateReport(gname)
        gname = self.w.gnameTextInput.get()
        
        self.interpSetGlyph(gname)
        
            
    def interp(self, value, gname):
        font1 = self.font1
        font2 = self.font2
        
        if len(font1[gname].components) > 0 or len(font2[gname].components) > 0:
            g1 = font1[gname]
            glyph1 = g1.copy()
            glyph1.naked().setParent(font1)
            glyph1.decompose()
            
            
            g2 = font2[gname]
            glyph2 = g2.copy()
            glyph2.naked().setParent(font2)            
            glyph2.decompose()
            
            
            #gname, 'has components'      

        else: 
            glyph1 = font1[gname]
            glyph2 = font2[gname]      


        dest = RGlyph()
        dest.interpolate(value, glyph1, glyph2)
        
        return dest
        

    def windowCloseCallback(self, sender):
        self.deactivateModule()
        BaseWindowController.windowCloseCallback(self, sender)   

#you must have 2 fonts open
if len(AllFonts()) < 2:
    print 'You must have two fonts open'

else: 
    font1 = CurrentFont()
    font2 = AllFonts()[1]



    #initial value for interpolation
    v = .5
    d = Dialog(v, font1, font2)
