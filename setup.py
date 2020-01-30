import os
import wget

URL_IMAGES = ''
URL_LABELS = ''
URL_WEIGHTS = "https://pjreddie.com/media/files/darknet53.conv.74"

def getPath():
  return os.getcwd()

def listDirectories(dir):
  return os.listdir(dir)

def createFolder(path,name):
  try:
    if not os.path.exists(path+name) and  not os.path.isdir(path+name):
      return os.mkdir(path+name)
    else:
      return 'folder exist'
  except:
    print("[Error]: Folder not created")

def downloadFile(url):
  return wget.download(url)


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
    with open(dest+"/"+fileName, 'w') as file:
      for line in imagesArray:
        i = i + 1
        if i > 10:
          file.write(pathImages+line+"\n")
    return file
  except:
    print("[Error]: train file not created")

def createTestFile(imagesArray, dest, pathImages,fileName):
  try:
    i = 0
    with open(dest+"/"+fileName, 'w') as file:
      for line in imagesArray:
        file.write(pathImages+line+"\n")
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
  PATH = getPath()+"/custom_data/";
  imagesArray = listDirectories(PATH+"/images") #Listado de imagenes 
  labelsArray = listDirectories(PATH+"/labels") #Listado de etiquetas
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
      pathImages=PATH+"/images/",
      fileName="train.txt"
    )
    
    if fileTrain != None:
      print("[-] Se creo el archivo train.txt correctamente.")

    fileTest = createTestFile(
      imagesArray,
      dest=PATH,
      pathImages=PATH+"/images/",
      fileName="test.txt"
    )

    if fileTest != None:
      print("[-] Se creo el archivo text.txt correctamente.")

    weightsFolder = createFolder(PATH, "weights")
    print(weightsFolder)
    if weightsFolder == 'folder exist':
      print("[-] Descargando pesos preentrenados.")
      downloadFile(URL_WEIGHTS)

main()