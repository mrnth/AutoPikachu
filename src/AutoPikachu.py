import time
from copy import deepcopy
from src.ScreenHandle import ScreenHandle


class AutoPikachu:
    def __init__(self):
        self.screenHandle = ScreenHandle()
        self.matrixID = []
        self.CreateMaxtrixID()
        self.listPokeImage = []
        self.matrixIDSorted = []

    def __del__(self):
        pass

    def CreateMaxtrixID(self):
        row = []
        for i in range(self.screenHandle.matrixSize[0] + 2):
            row.append(0)
        for i in range(self.screenHandle.matrixSize[1] + 2):
            self.matrixID.append(deepcopy(row))

    def SetMatrixPokemon(self):
        for y in range(1, self.screenHandle.matrixSize[1] + 1):
            for x in range(1, self.screenHandle.matrixSize[0] + 1):
                if y == 1 and x == 1:
                    self.matrixID[y][x] = 1
                    self.listPokeImage.append(self.screenHandle.CropPokeImage(0, 0))
                    continue

                pokeImage = self.screenHandle.CropPokeImage(x - 1, y - 1)
                # self.screenHandle.ShowImg(pokeImage, 10000)
                check = False
                for i in range(len(self.listPokeImage)):
                    compare = self.screenHandle.CompareImage(self.listPokeImage[i], pokeImage, 0.5)
                    # self.screenHandle.ShowImg(self.listPokeImage[i], 10000)
                    if compare is True:
                        self.matrixID[y][x] = i + 1
                        check = True
                        break

                if check is False:
                    self.matrixID[y][x] = len(self.listPokeImage) + 1
                    self.listPokeImage.append(pokeImage)

    def GetSumMaxtrixID(self):
        sumMatrixID = 0
        for row in self.matrixID:
            for col in row:
                sumMatrixID += col
        return sumMatrixID

    # Tinh tong row tu sau diem x1 den truoc diem x2
    def GetSumRow(self, y, x1, x2):
        if x2 > x1:
            minX = x1
            maxX = x2
        else:
            minX = x2
            maxX = x1
        sumRow = 0
        for x in range(minX + 1, maxX):
            sumRow += self.matrixID[y][x]
        return sumRow

    # Tinh tong cot tu sau diem y1 den truoc diem y2
    def GetSumCol(self, x, y1, y2):
        if y2 > y1:
            minY = y1
            maxY = y2
        else:
            minY = y2
            maxY = y1
        sumCol = 0
        for y in range(minY + 1, maxY):
            sumCol += self.matrixID[y][x]
        return sumCol

    def SortMatrixID(self):
        for pokeTypeId in range(1, len(self.listPokeImage) + 1):
            tempList = []
            for y in range(self.screenHandle.matrixSize[1] + 2):
                for x in range(self.screenHandle.matrixSize[0] + 2):
                    if self.matrixID[y][x] == pokeTypeId:
                        tempList.append([y, x])
            self.matrixIDSorted.append(deepcopy(tempList))

    def CheckConnectX(self, point1, point2):
        if point1[0] != point2[0]:
            return False
        if abs(point1[1] - point2[1]) == 1:
            return True

        if self.GetSumRow(point1[0], point1[1], point2[1]) == 0:
            return True
        else:
            return False

    def CheckConnectY(self, point1, point2):
        if point1[1] != point2[1]:
            return False
        if abs(point1[0] - point2[0]) == 1:
            return True
        if self.GetSumRow(point1[1], point1[0], point2[0]) == 0:
            return True
        else:
            return False

    def CheckConnectZX(self, point1, point2):
        if abs(point1[1] - point2[1]) < 2:
            return False

        if point1[1] < point2[1]:
            for x in range(point1[1] + 1, point2[1]):
                checkSum = self.GetSumRow(point1[0], point1[1], x + 1) + \
                           self.GetSumRow(point2[0], x - 1, point2[1]) + \
                           self.GetSumCol(x, point1[0], point1[1])
                if checkSum == 0:
                    return True
        else:
            for x in range(point2[1] + 1, point1[1]):
                checkSum = self.GetSumRow(point1[0], x - 1, point1[1]) + \
                           self.GetSumRow(point2[0], point2[1], x + 1) + \
                           self.GetSumCol(x, point1[0], point1[1])
                if checkSum == 0:
                    return True
        return False

    def CheckConnectZY(self, point1, point2):
        if abs(point1[0] - point2[0]) < 2:
            return False

        if point1[0] < point2[0]:
            for y in range(point1[0] + 1, point2[0] - 1):
                checkSum = self.GetSumCol(point1[1], point1[0], y + 1) + \
                           self.GetSumCol(point2[1], y - 1, point2[0]) + \
                           self.GetSumRow(y, point1[1], point1[1])
                if checkSum == 0:
                    return True
        else:
            for y in range(point2[0] + 1, point1[0] - 1):
                checkSum = self.GetSumCol(point1[1], y - 1, point1[0]) + \
                           self.GetSumCol(point2[1], point2[0], y + 1) + \
                           self.GetSumRow(y, point1[1], point1[1])
                if checkSum == 0:
                    return True
        return False

    def CheckConnectLX(self, point1, point2):
        if abs(point1[1] - point2[1]) == 0 or abs(point1[0] - point2[0]) == 0:
            return False
        if point1[1] < point2[1]:
            if point1[0] < point2[0]:
                checkSum = self.GetSumRow(point1[0], point1[1], point2[1] + 1) + \
                           self.GetSumCol(point2[1], point1[0], point2[0])
                if checkSum == 0:
                    return True
            else:
                checkSum = self.GetSumRow(point1[0], point1[1], point2[1] + 1) + \
                           self.GetSumCol(point2[1], point2[0], point1[0])
                if checkSum == 0:
                    return True
        else:
            if point1[0] < point2[0]:
                checkSum = self.GetSumRow(point2[0], point2[1], point1[1] + 1) + \
                           self.GetSumCol(point1[1], point1[0], point2[0])
                if checkSum == 0:
                    return True
            else:
                checkSum = self.GetSumRow(point2[0], point2[1], point1[1] + 1) + \
                           self.GetSumCol(point1[1], point2[0], point1[0])
                if checkSum == 0:
                    return True
        return False

    # def CheckConnectLY(self, point1, point2):
    #     if abs(point1[1] - point2[1]) == 0 or abs(point1[0] - point2[0]) == 0:
    #         return False
    #     if point1[0] < point2[0]:
    #         if point1[1] < point2[1]:
    #             checkSum = self.GetSumCol(point1[1], point1[0] + 1, point2[0]) + \
    #                        self.GetSumRow(point2[0], point1[1], point2[1] + 1)
    #             if checkSum == 0:
    #                 return True
    #         else:
    #             checkSum = self.GetSumCol(point1[1], point1[0] + 1, point2[0]) + \
    #                        self.GetSumRow(point2[0], point1[1], point2[1] - 1)
    #             if checkSum == 0:
    #                 return True
    #     else:
    #         if point1[1] < point2[1]:
    #             checkSum = self.GetSumCol(point2[1], point2[0] + 1, point1[0]) + \
    #                        self.GetSumRow(point1[0], point2[1], point1[1] + 1)
    #             if checkSum == 0:
    #                 return True
    #         else:
    #             checkSum = self.GetSumCol(point2[1], point2[0] + 1, point1[0]) + \
    #                        self.GetSumRow(point1[0], point2[1], point1[1] - 1)
    #             if checkSum == 0:
    #                 return True
    #     return False
    #
    # def CheckConnectUX(self, point1, point2):
    #     if point1[0] == point2[0]:
    #         return False
    #     if point1[1] < point2[1]:
    #         for x in range(point2[1] + 1, self.screenHandle.matrixSize[0] + 2)

    def StartAuto(self):
        self.screenHandle.CheckWindowApplication("Adobe Flash Player 11")
        self.screenHandle.SetWindowApplication()
        self.screenHandle.SetPokeTableRegion()
        self.SetMatrixPokemon()
        self.SortMatrixID()

        # while self.GetSumMaxtrixID() != 0:
        #     pass
