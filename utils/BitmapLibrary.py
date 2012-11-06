#!/usr/bin/env python
# -*- coding: utf-8 -*-

#This file is part of PLCOpenEditor, a library implementing an IEC 61131-3 editor
#based on the plcopen standard. 
#
#Copyright (C) 2012: Edouard TISSERANT and Laurent BESSARD
#
#See COPYING file for copyrights details.
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#General Public License for more details.
#
#You should have received a copy of the GNU General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os

import wx

#-------------------------------------------------------------------------------
#                            Library Structures
#-------------------------------------------------------------------------------

BitmapLibrary = {}
BitmapFolders = []

#-------------------------------------------------------------------------------
#                             Library Helpers
#-------------------------------------------------------------------------------

def AddBitmapFolder(path):
    if path not in BitmapFolders:
        BitmapFolders.append(path)

def SearchBitmap(bmp_name):
    for folder in BitmapFolders:
        bmp_path = os.path.join(folder, bmp_name + ".png")
        if os.path.isfile(bmp_path):
            return wx.Bitmap(bmp_path)
    return None
    
def GetBitmap(bmp_name1, bmp_name2=None, size=None):
    bmp = BitmapLibrary.get((bmp_name1, bmp_name2, size))
    if bmp is not None:
        return bmp
    
    if bmp_name2 is None:
        bmp = SearchBitmap(bmp_name1)
    else:
        # Bitmap with two icon
        bmp1 = SearchBitmap(bmp_name1)
        bmp2 = SearchBitmap(bmp_name2)
        
        if bmp1 is not None and bmp2 is not None:
            # Calculate bitmap size
            width = bmp1.GetWidth() + bmp2.GetWidth() - 1
            height = max(bmp1.GetHeight(), bmp2.GetHeight())
            
            # Create bitmap with both icons
            bmp = wx.EmptyBitmap(width, height)
            dc = wx.MemoryDC()
            dc.SelectObject(bmp)
            dc.Clear()
            dc.DrawBitmap(bmp1, 0, 0)
            dc.DrawBitmap(bmp2, bmp1.GetWidth() - 1, 0)
            dc.Destroy()
        
        elif bmp1 is not None:
            bmp = bmp1
        elif bmp2 is not None:
            bmp = bmp2
    
    if bmp is not None:
        BitmapLibrary[(bmp_name1, bmp_name2, size)] = bmp
        
    return bmp
