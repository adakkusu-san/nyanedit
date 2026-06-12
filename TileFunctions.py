import os
import struct
import pygame
import sys
from tkinter import filedialog, messagebox

from GetResources import *

#how bytes are grouped
groupSize = 2

def getFile(previousFileLength):
    if len(sys.argv) > 1:
        path = sys.argv[1]
        fileLength = os.path.getsize(path)
    else:
        path = filedialog.askopenfilename()
        if path != "":
            fileLength = os.path.getsize(path)
        else:
            fileLength = previousFileLength
    return path, fileLength

def getTileData(tileData, tileList, previousTileData, isFirstLoad):

    path, fileLength = getFile(0)
    if path == "" and not isFirstLoad:
        tileData = previousTileData
    else:

        if path == "" and isFirstLoad:
                path = "defaultmap.mpd"

        tileData = []
        with open(path, "rb") as file:
            
            if isFirstLoad and path == "defaultmap.mpd":
                fileLength = os.path.getsize(path)
  
            for i in range(int(fileLength / groupSize)):

                currentTile = int.from_bytes(file.read(groupSize))
                
                flag = 0
                for j in range(len(tileList)):
                    if tileList[j].hex == currentTile:
                        tileData.append(tileList[j].hex)
                        flag = 1
                    elif j == len(tileList)-1 and flag == 0:
                        print("Error: Could not read value " + hex(currentTile) + ". Displaying 0xFFFF (undefined).")
                        tileData.append(0xFFFF) #undefined tile
            file.close()
    return tileData

def getButtonData(tileList, extraButtonRows, lineWidth):
    #all tiles except undefined, save, and swap bg
    buttonData = []
    for i in range(5, len(tileList)):
        buttonData.append(tileList[i].hex)

    extraButtons = extraButtonRows * lineWidth

    for i in range(len(buttonData), extraButtons-3):
        buttonData.append(0xFFFB) #blank slot tile
    
    buttonData.append(0xFFFD) #swapbg
    buttonData.append(0xFFFC) #newfile
    buttonData.append(0xFFFE) #save

    return buttonData

def getClickedButton(pos, buttonData, previousSelected):
    x = pos[0]
    y = pos[1]
    newSelected = buttonData[(y-60)*40 + x]
    if newSelected == 0xFFFB: #blank slot
        selected = previousSelected
    else:
        selected = newSelected
    return selected

def editTile(pos, newTileType, tileData):
    x = pos[0]
    y = pos[1]
    tileData[y*40 + x] = tileList[tileHexList.index(newTileType)].hex
    return tileData

def saveFile(tileData):
        if 0xFFFF in tileData:
            return False
        else:
            savePath = filedialog.asksaveasfilename()
            if savePath != "":
                with open(savePath, "wb") as newFile:
                    for i in range(len(tileData)):
                        newFile.write(bytes(struct.pack(">H", tileData[i])))
                    newFile.close()
                    print("Saved!!")
            return True

def askForSave():
    answer = messagebox.askyesno(title="Save?", message="Would you like to save?")
    return answer

def displayCantSave():
    messagebox.showerror("Can't save!!", message="Can't save with undefined tiles!!")