# Classifier Bottle

# Yolo

### Detector.data file

**classes**=1: el conjunto de datos tiene 1 clase
**train** = ...: dónde encontrar la lista de archivos de entrenamiento
**valid** = ...: dónde encontrar la lista de archivos de validación
**names** = ...: dónde encontrar la lista de posibles clases
**backup** = ...: dónde guardar archivos de peso de respaldo durante el entrenamiento
## Lote
* **batch** la cantidad de imágenes elegidas en cada lote para reducir la pérdida

> Cuando el tamaño del lote se establece en 64, significa que se usan 64 imágenes en una iteración para actualizar los parámetros de la red neuronal.

### Subdivisiones

 **subdivisions** división del tamaño del lote a numero de sub lotes para procesamiento paralelo

> Aunque es posible que desee usar un tamaño de lote de 64 para entrenar su red neuronal, es posible que no tenga una GPU con suficiente memoria para usar un tamaño de lote de 64. Afortunadamente, Darknet le permite especificar una variable llamada subdivisiones que le permite procesar una fracción del tamaño del lote a la vez en su GPU.

> Puede comenzar el entrenamiento con subdivisiones = 1, y si obtiene un error de memoria insuficiente , aumente el parámetro de subdivisiones en múltiplos de 2 (por ejemplo, 2, 4, 8, 16) hasta que el entrenamiento continúe con éxito. La GPU procesará la lote / subdivisióncantidad de imágenes en cualquier momento, pero el lote completo o la iteración se completarán solo después de que se procesen las 64 imágenes (como se estableció anteriormente).

### El archivo de configuración contiene algunos parámetros que controlan cómo se actualiza el peso.
El archivo de configuración contiene algunos parámetros que controlan cómo se actualiza el peso.

* **momentum**=0.9
* **decay**=0.0005
 
>  Un ejemplo es cuando se actualizan los pesos de una red neuronal en función de un pequeño lote de imágenes y no de todo el conjunto de datos. Debido a esta razón, las actualizaciones de peso fluctúan bastante. Por esta razon se utiliza un **momentum** de parámetro para penalizar los cambios de peso grandes entre iteraciones. 
  
>  Una red neuronal típica tiene millones de pesos y, por lo tanto, puede sobreajustar fácilmente cualquier información de entrenamiento. El sobreajuste simplemente significa que funcionará muy bien en los datos de entrenamiento y mal en los datos de prueba. Es casi como si la red neuronal hubiera memorizado la respuesta a todas las imágenes del conjunto de entrenamiento, pero realmente no aprendió el concepto subyacente. Una de las formas de mitigar este problema es penalizar un gran valor para los pesos. La disminución de parámetros controla este término de penalización. El valor predeterminado funciona bien, pero es posible que desee ajustar esto si nota un sobreajuste.

### Ancho, Altura, Canales
 **channels** Canales se refiere al tamaño del canal de la imagen de entrada (3) para una imagen BGR

> Ancho, Altura, Canales
> Estos parámetros de configuración especifican el tamaño de la imagen de entrada y el > > número de canales.

* **width**=416
* **height**=416
* **channels**=3
> Las imágenes de entrenamiento de entrada primero se redimensionan a ancho  x  altura  antes del entrenamiento. Aquí usamos los valores predeterminados de 416 × 416. Los resultados podrían mejorar si lo aumentamos a 608 × 608, pero también llevaría más tiempo entrenar. canales = 3 indica que estaríamos procesando imágenes de entrada RGB de 3 canales.

* **filters** la cantidad de filtros utilizados para un algoritmo CNN

* **activation** la función de activación de CNN: se utiliza principalmente la función Leaky RELU (lo que he visto principalmente en los archivos de configuración)


### Tasa de aprendizaje, pasos, escalas, quemadura (warm-up)
* **learning_rate**=0.001
* **policy**=steps
* **steps**=3800
* **scales**=.1
* **burn_in**=400

> El parametro **learning_rate** (tasa de aprendizaje) controla cuán agresivamente debemos aprender en función del lote de datos actual. Por lo general, este es un número entre 0.01 y 0.0001.

> Al comienzo del proceso de capacitación, comenzamos con cero información y, por lo tanto, la tasa de aprendizaje debe ser alta. Pero a medida que la red neuronal ve muchos datos, los pesos deben cambiar de manera menos agresiva. En otras palabras, la tasa de aprendizaje debe reducirse con el tiempo. En el archivo de configuración, esta disminución en la tasa de aprendizaje se logra especificando primero que nuestra **policy** (política de disminución) de la tasa de aprendizaje son **steps** (pasos). 

> En el ejemplo anterior, la tasa de aprendizaje comenzará desde 0.001 y permanecerá constante durante 3800 iteraciones, y luego se multiplicará por **scales** (escalas) para obtener la nueva tasa de aprendizaje. También podríamos haber especificado múltiples pasos y escalas.

> Anteriormente se mencionó que la tasa de aprendizaje debe ser alta al principio y baja después. Si bien esa afirmación es en gran medida cierta, se ha encontrado empíricamente que la velocidad de entrenamiento tiende a aumentar si se tiene una tasa de aprendizaje más baja durante un corto período de tiempo desde el principio. Esto es controlado por el parámetro **burn_in**. A veces, este período de (quemado) también se llama período de calentamiento. 


### Aumento de datos
> Queremos aprovechar al máximo estos datos cocinando nuevos datos. Este proceso se llama aumento de datos. Por ejemplo, una imagen del muñeco de nieve girada 5 grados sigue siendo una imagen de un muñeco de nieve. El parámetro de ángulo en el archivo de configuración le permite rotar aleatoriamente la imagen dada por ± ángulo.

> Del mismo modo, si transformamos los colores de toda la imagen utilizando la saturación , la exposición y el tono , sigue siendo una imagen del muñeco de nieve.

* **angle**=0
* **saturation** = 1.5
* **exposure** = 1.5
* **hue**=.1

Utilizamos los valores predeterminados para el entrenamiento.


### Número de iteraciones

> Finalmente, necesitamos especificar cuántas iteraciones debe ejecutarse el proceso de capacitación.

* **max_batches**=5200

> Para los detectores de objetos de varias clases, el número de **max_batches** es mayor, es decir, necesitamos ejecutar más cantidad de lotes (por ejemplo, en yolov3-voc.cfg). Para un detector de objetos n-classes, es aconsejable ejecutar el entrenamiento durante al menos 2000 * n-lotes. En nuestro caso con solo 1 clase, 5200 parecía un número seguro para **max_batches**.

> filters = (classes +5)*3

### Entrenamiento YOLOv3

> `./darknet detector train /path/to/snowman/darknet.data /path/to/snowman/darknet-yolov3.cfg ./darknet53.conv.74 > /path/to/snowman/train.log`
 
 ### Pruebas 
 
> `./darknet detect cfg/yolov3.cfg yolov3.weights <imagen>`