import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
import time


class ScreenHandle:
    def __init__(self):
        self.hwndMain = None
        self.mWindowBox = [0, 0, 0, 0]
        self.mFrameSize = [0, 0]
        self.mCheckMouseRunning = False
        self.pokeTableRegion = [0, 0, 0, 0]
        self.matrixSize = [12, 8]
        self.gameFrame = None

    def CheckWindowApplication(self, window_name):
        self.hwndMain = win32gui.FindWindow(None, window_name)
        if not self.hwndMain:
            print("Cannot find windows name")
            return False
        return True

    def SetWindowApplication(self):
        # get the window box
        window_rect = win32gui.GetWindowRect(self.hwndMain)
        self.mWindowBox[0] = window_rect[0]
        self.mWindowBox[1] = window_rect[1]
        self.mWindowBox[2] = window_rect[2] - window_rect[0]
        self.mWindowBox[3] = window_rect[3] - window_rect[1]
        self.mFrameSize[0] = self.mWindowBox[2]
        self.mFrameSize[1] = self.mWindowBox[3]

    def WindowScreenShot(self):
        left_offset = 0
        top_offset = 0
        try:
            # get the window image data
            wDC = win32gui.GetWindowDC(self.hwndMain)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, self.mFrameSize[0], self.mFrameSize[1])
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (self.mFrameSize[0], self.mFrameSize[1]), dcObj, (left_offset, top_offset),
                       win32con.SRCCOPY)

            # convert the raw data into a format opencv can read
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.frombuffer(signedIntsArray, dtype='uint8')
            img.shape = (self.mFrameSize[1], self.mFrameSize[0], 4)

            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwndMain, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            img = img[..., :3]
            img = np.ascontiguousarray(img)
        except (ValueError, Exception):
            return None
        return img

    def Stream(self):
        while True:
            cv2.imshow("nth", self.gameFrame)
            cv2.waitKey(1)

    def ActivateWindow(self):
        win32gui.ShowWindow(self.hwndMain, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self.hwndMain)

    def RegionScreenshot(self, mRegion: list):
        frame = self.WindowScreenShot()
        try:
            outFrame = frame[mRegion[1]:mRegion[1] + mRegion[3], mRegion[0]:mRegion[0] + mRegion[2]]
        except (ValueError, Exception):
            return None
        return outFrame

    def CropPokeImage(self, x, y):
        pokeRegion = self.GetPokeRegion(x, y)
        outFrame = self.gameFrame[pokeRegion[1]:pokeRegion[1] + pokeRegion[3],
                   pokeRegion[0]:pokeRegion[0] + pokeRegion[2]]
        return outFrame

    # input: big image, small image gray, confidence float
    @staticmethod
    def CompareImage(big_image, small_image, confidence: float):
        res = cv2.matchTemplate(big_image, small_image, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= confidence)
        for pt in zip(*loc[::-1]):
            return True
        return False

    @staticmethod
    def CheckLeftMouseClick():
        if win32api.GetKeyState(0x01) < 0:
            return True
        return False

    def GetClickPosition(self):
        self.mCheckMouseRunning = True
        mousePos = [0, 0]
        while self.mCheckMouseRunning is True:
            mousePos = win32gui.GetCursorPos()
            for i in range(30):
                if self.CheckLeftMouseClick() is True:
                    self.mCheckMouseRunning = False
                time.sleep(0.001)
        return mousePos[0], mousePos[1]

    def SetPokeTableRegion(self):
        time.sleep(0.5)
        print("Click top left corner of region")
        self.pokeTableRegion[0], self.pokeTableRegion[1] = self.GetClickPosition()
        time.sleep(0.5)
        print("Click bottom right corner of region")
        self.pokeTableRegion[2], self.pokeTableRegion[3] = self.GetClickPosition()

        self.pokeTableRegion[2] = self.pokeTableRegion[2] - self.pokeTableRegion[0]
        self.pokeTableRegion[3] = self.pokeTableRegion[3] - self.pokeTableRegion[1]
        self.pokeTableRegion[0] = self.pokeTableRegion[0] - self.mWindowBox[0]
        self.pokeTableRegion[1] = self.pokeTableRegion[1] - self.mWindowBox[1]

        input("Uncheck all box in game. Press Enter to continue...")
        self.gameFrame = self.WindowScreenShot()
        self.gameFrame = cv2.cvtColor(self.gameFrame, cv2.COLOR_BGR2GRAY)

    def GetPokeRegion(self, x: int, y: int):
        region = [0, 0, 0, 0]
        leftOffset = self.pokeTableRegion[0]
        topOffset = self.pokeTableRegion[1]
        pokeWidth = self.pokeTableRegion[2] / self.matrixSize[0]
        pokeHeight = self.pokeTableRegion[3] / self.matrixSize[1]
        region[0] = int(pokeWidth * x + leftOffset + pokeWidth * 0.05)
        region[1] = int(pokeHeight * y + topOffset + pokeHeight * 0.05)
        region[2] = int(pokeWidth * 0.9)
        region[3] = int(pokeHeight * 0.9)
        # print(region)
        return region

    @staticmethod
    def ShowImg(img, sleep: int):
        cv2.imshow("ShowImg", img)
        cv2.waitKey(sleep)

    @staticmethod
    def WriteImg(img, name):
        cv2.imwrite(name, img)
