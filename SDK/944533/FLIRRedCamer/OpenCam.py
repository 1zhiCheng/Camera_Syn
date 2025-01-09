import numpy as np
import os
import clr
import sys

sys.path.append(r"C:\Program Files (x86)\FLIR Systems\FLIR Atlas SDK 4\bin\x64")

clr.FindAssembly("Flir.Atlas.Image.dll")
clr.FindAssembly("Flir.Atlas.Live.dll")
# clr.AddReference("Flir.Atlas.Image")
# clr.AddReference("Flir.Atlas.Live")
# clr.AddReference("Flir.Atlas.Live.Device")
# clr.AddReference("Flir.Atlas.Live.Discovery")

from System.Threading import *
from Flir.Atlas.Live import *
from Flir.Atlas.Live.Device import *
from Flir.Atlas.Live.Discovery import *
from Flir.Atlas.Image import *
from Flir.Atlas.Image.Measurements import *
from System.Drawing import *
from System.Drawing.Imaging import ImageFormat
from Flir.Atlas.Image.Palettes import PaletteManager
from Flir.Atlas.Image.Measurements import MeasurementRectangle

cam=ThermalCamera()
tif=ThermalImage()
camdevinfo=CameraDeviceInfo.Create('192.168.1.107',Interface.All)
if (camdevinfo == None):
    print("找不到相机设备")
else:
    print("存在相机设备")
    cam.Connect(camdevinfo)
    Thread.Sleep(2000)
    if(cam.ConnectionStatus==2):
        print("连接成功")
        Thread.Sleep(5000)
        image=cam.GetImage()
        image.Palette = PaletteManager.Rainbow
        Rbuffer=Bitmap(image.Image, 320, 256)
        Rbuffer.Save("BitMap.jpg",  ImageFormat.Jpeg)
        image.Measurements.Clear()
        mr=image.Measurements.Add(Rectangle(0, 0, image.Width, image.Height))
        #温度获取
        hotPoint=mr.HotSpot
        hotTemp=mr.Max.Value
        coldPoint=mr.ColdSpot
        coldTemp=mr.Min.Value




