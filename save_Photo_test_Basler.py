
"""This sample shows how grabbed images can be saved using pypylon only (no
need to use openCV).
Available image formats are     (depending on platform):
 - pylon.ImageFileFormat_Bmp    (Windows)
 - pylon.ImageFileFormat_Tiff   (Linux, Windows)
 - pylon.ImageFileFormat_Jpeg   (Windows)
 - pylon.ImageFileFormat_Png    (Linux, Windows)
 - pylon.ImageFileFormat_Raw    (Windows)
"""
from pypylon import pylon
import platform
import datetime
import time
num_img_to_save = 1  #количество фото
img = pylon.PylonImage()
IP_CAMERA1='192.168.10.228'
IP_CAMERA2='192.168.10.229'
time_now  = str(datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S'))
def photo_kowa(ExposureTimeAbs):
    factory = pylon.TlFactory.GetInstance()
    ptl = factory.CreateTl('BaslerGigE')
    empty_camera_info = ptl.CreateDeviceInfo()
    empty_camera_info.SetPropertyValue('IpAddress', IP_CAMERA1)
    camera_device = factory.CreateDevice(empty_camera_info)
    cam = pylon.InstantCamera(camera_device)
    cam.Open()
    cam.ExposureTimeAbs.SetValue(ExposureTimeAbs)
    cam.StartGrabbing()
    for i in range(num_img_to_save):
        with cam.RetrieveResult(5000) as result:
            img.AttachGrabResultBuffer(result)

            if platform.system() == 'Windows':
                # quality (100 -> лучшее качество, 0 -> худшее).
                ipo = pylon.ImagePersistenceOptions()
                # quality = 90 - i * 10
                quality = 100
                ipo.SetQuality(quality) 
                filename = "%s_exposure_time_%d.png" % (time_now, ExposureTimeAbs)
                img.Save(pylon.ImageFileFormat_Png, filename)
            img.Release()

    cam.StopGrabbing()
    cam.Close()
# def photo_fusion(ExposureTimeAbs):
#     factory = pylon.TlFactory.GetInstance()
#     ptl = factory.CreateTl('BaslerGigE')
#     empty_camera_info = ptl.CreateDeviceInfo()
#     empty_camera_info.SetPropertyValue('IpAddress', IP_CAMERA2)
#     camera_device = factory.CreateDevice(empty_camera_info)
#     cam = pylon.InstantCamera(camera_device)
#     cam.Open()
#     cam.ExposureTimeAbs.SetValue(ExposureTimeAbs)
#     cam.StartGrabbing()
#     for i in range(num_img_to_save):
#         with cam.RetrieveResult(5000) as result:
#             img.AttachGrabResultBuffer(result)

#             if platform.system() == 'Windows':
#                 # quality (100 -> лучшее качество, 0 -> худшее).
#                 ipo = pylon.ImagePersistenceOptions()
#                 # quality = 90 - i * 10
#                 quality = 100
#                 ipo.SetQuality(quality) 
#                 filename = "fusion" + "%s_exposure_time_%d.png" % (time_now, ExposureTimeAbs)
#                 img.Save(pylon.ImageFileFormat_Png, filename)
#             img.Release()

#     cam.StopGrabbing()
#     cam.Close()
t1 = time.perf_counter()
photo_kowa(40000)
# photo_kowa(50000)
# photo_kowa(55000)
# photo_kowa(60000)
# photo_kowa(65000)
# photo_kowa(70000)
# photo_kowa(80000)
# photo_kowa(90000)
# photo_kowa(100000)
# photo_fusion(200000)#в скобках значение экспозиции
t2 = time.perf_counter()
print(f"сохранение фото заняло {t2 - t1} секунд")
