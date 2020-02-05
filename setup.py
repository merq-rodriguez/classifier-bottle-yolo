import os
import wget
import platform

URL_IMAGES = ''
URL_LABELS = ''
URL_WEIGHTS = "https://pjreddie.com/media/files/darknet53.conv.74"

#Version de sistema operativo
def getSystem():
  return platform.system()

def join(path,folder):
  return os.path.join(path, folder)

def getPath():
  return os.getcwd()

def listDirectories(dir):
  return os.listdir(dir)

def createFolder(path,name):
  try:
    route = join(path, name)
    if not os.path.exists(route) and  not os.path.isdir(route):
      os.mkdir(route)
      return True
    else:
      return 'folder exist'
  except:
    print("[Error]: Folder not created")

def downloadFile(url, output, fileName):
  try:
    return wget.download(url, out=join(output,fileName))
  except:
    print("Not download file: "+fileName)


def createAllDiretories(PATH):
  dirs =listDirectories(PATH)

  folderImg = [folder for folder in dirs if folder == 'images']
  folderLabels = [folder for folder in dirs if folder == 'labels']
  folderWeights = [folder for folder in dirs if folder == 'weights']

  
  if len(folderImg) > 0:
    print("Existe la carpeta images")
  else:
    createFolder('weights')

  if len(folderImg) > 0:
    print("Existe la carpeta images")
  else:
    createFolder('images')

  if len(folderLabels) > 0:
    print("Existe la carpeta labels")
  else:
      createFolder('labels')


def createTrainFile(imagesArray, dest, pathImages,fileName):
  try:
    i = 0
    with open(join(dest,fileName), 'w') as file:
      for line in imagesArray:
        i = i + 1
        if i > 10:
          file.write(join(pathImages, line)+"\n")
    return file
  except:
    print("[Error]: train file not created")

def createTestFile(imagesArray, dest, pathImages,fileName):
  try:
    i = 0
    with open(join(dest, fileName), 'w') as file:
      for line in imagesArray:
        file.write(join(pathImages, line)+"\n")
        i = i + 1
        if i > 11:
          break
    return file
  except:
    print("[Error]: test file not created")




def main():
  print("===========================================================")
  print("                        INICIANDO                          ")
  print("===========================================================")
  PATH = join(getPath(), "custom_data");
  print("XD: "+join(PATH, "images"))
  imagesArray = listDirectories(join(PATH, "images")) #Listado de imagenes 
  labelsArray = listDirectories(join(PATH, "labels")) #Listado de etiquetas
  missingData = []

  # Verificamos que todas las imagenes tengan su archivo de etiquetado
  for item in imagesArray:
    file, extension = item.split('.')
    if file+'.txt' in labelsArray:
      pass
    else:
      missingData.append(item)


  # Mostramos las imagenes que no tengan su archivo txt de equiquetado, de lo contrario,
  # si todo esta bien, creamos el archivo train.txt
  if(len(missingData) > 0):
    print("Se detectaron imagenes sin el archivo de etiquetado")
    for item in missingData:
      file, extension = item.split('.')
      print("No se encontro el archivo "+file+".txt")
  else:
    print("[-] Todas las imagenes tienen su archivo .txt de etiquetado.")

    #Creamos el archivo "train.txt" que contendrá la ruta absoluta de cada una de las imagenes de entrenamiento
    fileTrain = createTrainFile(
      imagesArray,
      dest=PATH,
      pathImages=join(PATH, "images"),
      fileName="train.txt"
    )
    
    if fileTrain != None:
      print("[-] Se creo el archivo train.txt correctamente.")

    fileTest = createTestFile(
      imagesArray,
      dest=PATH,
      pathImages=join(PATH, "images"),
      fileName="test.txt"
    )

    if fileTest != None:
      print("[-] Se creo el archivo text.txt correctamente.")

    weightsFolder = createFolder(PATH, "weights")
    fileName="darknet53.conv.74"
    PATH_WEIGHTS = join(PATH, "weights")

    if weightsFolder == 'folder exist' or weightsFolder == True:
      if not os.path.exists(join(PATH_WEIGHTS, fileName)):
        print("[-] Descargando pesos preentrenados.")
        downloadFile(
          url=URL_WEIGHTS, 
          output=PATH_WEIGHTS,
          fileName=fileName
        )
      else:
        print("[-] Los pesos ya existen.")
      
main()