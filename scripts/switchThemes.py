import difflib
import os
import shutil

def isDiff(file1, file2):
    fo1 = open(file1, 'r')
    fo2 = open(file2, 'r')

    reader1 = fo1.readlines()
    reader2 = fo2.readlines()
    return next(difflib.context_diff(reader1, reader2), None) is not None

def getCurrentTheme(home, themeDir):
    checkFile = ".Xresources"
    themeList = os.listdir(themeDir)

    for theme in themeList:
        if not isDiff('/'.join([themeDir, theme, checkFile]), '/'.join([home, checkFile])):
            return theme
    
    return ''

def askUserTheme(themeList):
    print("I will print a numbered list of themes from your .rice/themes directory. Please enter the number of the theme you would like to use.")
    for idx, theme in enumerate(themeList):
        print(str(idx) + ": " + theme)

    userInput = input("please enter the number of your selection:")

    return themeList[int(userInput)]

def getNewTheme(home, themeDir, currentTheme):
    themeList = os.listdir(themeDir)

    if(len(themeList) == 1):
        return themeList[0]
    elif(currentTheme):
        if(len(themeList) == 2):
            if(currentTheme == themeList[0]):
                return themeList[1]
            else:
                return themeList[0]
        
    return askUserTheme(themeList)

def getFiles(folder):
    FileList = []

    print("Files to be themed")

    for root, folderList, localFileList in os.walk(folder):
        for file in localFileList:
            #removes themeDir from path to produce path from home directory
            shortPath = root[len(folder):] + '/' + file
            print(shortPath)
            FileList.append(shortPath)
    
    return FileList

def switchTheme():
    #automatically determines the path of .rice/themes based on the location of this script
    themeDir = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]) + '/themes'
    #automatically determines the home directory
    home = os.environ["HOME"]

    currentTheme = getCurrentTheme(home, themeDir)
    newTheme = getNewTheme(home, themeDir, currentTheme)
    exitWithoutChanges = False

    if currentTheme != newTheme:
        if currentTheme:
            currentFileList = getFiles(themeDir + '/' + currentTheme)

            for file in currentFileList:
                if isDiff(home + file, themeDir + '/' + currentTheme + file):
                    print("You changed your config for " + file + ", please update the configs in .rice")
                    exitWithoutChanges = True
        else:
            userInput = input("Your theme doesn't match anything in your Themes folder. We found this through comparing your .Xresources. This script will destroy your current configuration files. Continue?(y/n):")
            
            if userInput != 'y':
                exitWithoutChanges = True
    else:
        print("You are already using this theme")
        exitWithoutChanges = True

    if not exitWithoutChanges:
        newFileList = getFiles(themeDir + '/' + newTheme)

        for file in newFileList:
            print('copying: ' + file)
            shutil.copyfile(themeDir + '/' + newTheme + file, home + file)
        os.system('i3-msg restart')

switchTheme()
