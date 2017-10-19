
import cv2
import sys
from detectorObjetos6 import *

class medidorDistancia:
    def __init__(self,pixError,rotationDir,thickWindowCube, thickWindowDetect,umbralIn,umbralOut,distRef):

        # Vector de distancias para cada cubo detectado
        self.distancias = []

        # Vector de angulos para cada cubo detectado
        self.angulos = []

        # Minimo de pixeles de error tolerados en la deteccion por color
        self.pixError = pixError

        # Direccion de la rotacion de la camara
        self.rotationDir = rotationDir

        # Ancho de la ventana de deteccion de cubos nuevas completas
        self.thickWindowCube = thickWindowCube

        # Ancho de la ventana de deteccion de transito de cubos por el borde del frame
        self.thickWindowDetect = thickWindowDetect

        # Umbral de tolerancia para dejar de hacer tracking a las fichas que salen del frame
        self.umbralOut = umbralOut

        # Umbral para determinar si un cubo esta pasando o no por el borde de entrada del frame
        self.umbralIn = umbralIn


        # Parametro basado en una imagen de referencia, para medir la distancia de los cubos
        self.distRef = distRef

        # Parametros para calcular los angulos de los cubos con respecto al de la camara
        self.R = 60 # Rango en grados que abarca cada frame
        self.alpha = 0 # Angulo entre la referencia y el extremo izquierdo del frame
        self.alphaStep = None # Angulo que se suma cada vez que pasa un frame.. Depende de
        # la cantidad total de frames
        self.width = 800


        #######VECTOR DE SALIDA CON LA SIGUIENTE ESTRUCTURA [ [ang,dist], [ang,dist] ...]
        ###### CADA PAR [ANG,DIST] CORRESPONDE A UN CUBO
        self.angs_dists = []
           
    @staticmethod
    def get_dist_ref(imgRef):
        # Variables para determinar la distancia a los cubos
        # initialize the known distance from the camera to the object, which
        # in this case is 15 cm
        knownDistance = 15
         
        # initialize the known object width, which in this case, the piece of
        # paper is 11 inches wide
        # ancho de la ficha = 1.5cm
        knownWidth = 1.5
        
        marker = detectorObjetos.detectar_cubo_referencia(imgRef)
        focalLength = (marker[1][0] * knownDistance) /knownWidth
        # El primer valor retornado es util para hallar distancias cubo a camara
        # El segundo valor es util para hacer relaciones de distancia entre objetos del frame
        return [knownWidth*focalLength,knownWidth/marker[1][0]]

    def get_angs_dists(self):
        '''
        Este metodo devuelve una lista con los angulos y distancias promedio por cada cubo
        '''
        for (angulo,distancia) in zip(self.angulos,self.distancias):
            angProm = 0
            distProm = 0
            size = 0
            for (ang,dist) in zip(angulo,distancia):
                angProm = angProm + ang
                distProm = distProm + dist
                size = size + 1

            angProm = angProm/size
            distProm = distProm/size
            self.angs_dists.append([angProm,distProm])

        return self.angs_dists


            


    def get_dist_to_cam(self,box):
        #minX = min(box[0][0],box[1][0],box[2][0],box[3][0])
        #maxX = max(box[0][0],box[1][0],box[2][0],box[3][0])
        #cubeDist = maxX-minX

        # Formato de Box (minX,minY,ancho,alto)
        cubeDist = box[2]
        return self.distRef[0] / cubeDist
        


    def get_angulo_cubo(self,box):
        # Este metodo debe poder conocer el angulo de la camara
        # Tal vez deberia provenir de otra clase
        # Para entender las variables, ver cuaderno
        # Formato de Box (minX,minY,ancho,alto)

        # Hallar las coordenadas del centro, por ahora solo en X
        #minX = min(box[0][0],box[1][0],box[2][0],box[3][0])
        #maxX = max(box[0][0],box[1][0],box[2][0],box[3][0])
        #Lpix = (minX+maxX)/2 # Distancia desde el borde izq del frame a el centro del cubo
        Lpix = (2*box[0]+box[2])/2
        #print("Lpix="+str(Lpix))
        #Lreal = Lpix*self.distRef[1] # creo que no necesito esto
        #print("Lreal="+str(Lreal))
        # Se calcula el angulo
        #print("Alpha="+str(self.alpha))
        alphaCube = (Lpix*self.R/self.width) + self.alpha
        #print("AlphaCube="+str(alphaCube)+"\n")
        return alphaCube
        

    def detectar_cubo_entrante(self,frame,detector,alto,ancho):
        # Este metodo es usado para agregar las fichas que van
        # entrando por cualquier lado del video

        windowDetect = self.get_window_detect(frame,alto,ancho)
        detector.img = windowDetect
        # Umbralizar por rojo
        mask = detector.segmentar_por_color(np.array([0,70,50]),
                                            np.array([10,255,255]),
                                            np.array([170,70,50]),
                                            np.array([180,255,255]),
                                            False)
        #cv2.imshow("Mask entrada",mask)
        #print("Pixeles de cubo nuevo:"+str(cv2.countNonZero(mask)))
        if cv2.countNonZero(mask) > self.umbralIn:
            # Hay un cubo entrando
            return True
        else:
            return False


    def get_window_cube(self,frame):
        if self.rotationDir == 'right':
            windowCube = frame[:,frame.shape[1]-self.thickWindowCube:,:]
            #print("frame.shape = "+str(frame.shape))
            
        elif self.rotationDir == 'left':
            # Hacerlo de acuerdo al sentido de rotacion
            windowCube = 0
            

        elif self.rotationDir == 'up':
            # Hacerlo de acuerdo al sentido de rotacion
            windowCube = 0

        elif self.rotationDir == 'down':
            # Hacerlo de acuerdo al sentido de rotacion
            windowCube = 0
            
        #print("windowCube = "+str(windowCube.shape))
        return windowCube


    # ESTO DEBERIA SER UNA CLASE, SERIA MUCHO MAS EFECTIVO
    def get_window_detect(self,frame,alto,ancho):
        if self.rotationDir == 'right':
            
            windowDetect = frame[:,ancho-self.thickWindowDetect:,:]
            #print("frame.shape = "+str(frame.shape))
            
        elif self.rotationDir == 'left':
            # Hacerlo de acuerdo al sentido de rotacion
            windowDetect = 0
            

        elif self.rotationDir == 'up':
            # Hacerlo de acuerdo al sentido de rotacion
            windowDetect = 0

        elif self.rotationDir == 'down':
            # Hacerlo de acuerdo al sentido de rotacion
            windowDetect = 0
            
        #print("windowDetect = "+str(windowDetect.shape))
        return windowDetect
        

    def get_trackers(self,frame,frameOrg,detector,newCubes,altoImg,anchoImg,oldBoxes,firstFrame):
        # Este metodo se usa para retornar la cantidad de trackers
        # dependiendo de cuantas fichas fueron halladas
        
        # Determinar los cuadros de area minima que incluyen a las fichas
        detector.img = frame
        boxes = detector.detectar_cubos(self.pixError,firstFrame)

        # Se parametrizan las coordenadas para que coincidan con la entrada del tracker
        # y se crea un cuadrado de tracking por cada ficha detectada
        bbox = []
        trackers = []
        checkers = []
        dists = []
        angs = []
        
        for box in boxes:
            minX = min(box[0][0],box[1][0],box[2][0],box[3][0])
            minY = min(box[0][1],box[1][1],box[2][1],box[3][1])
            maxX = max(box[0][0],box[1][0],box[2][0],box[3][0])
            maxY = max(box[0][1],box[1][1],box[2][1],box[3][1])

            ancho = int(maxX-minX)
            alto = int(maxY-minY)

            overlap = False
            if newCubes:
                # Ajuste de coordenadas de windowCube al size original
                # El ajuste depende de la direccion de rotacion
                if self.rotationDir == 'right':
                    minX = np.int32(anchoImg-self.thickWindowCube+minX)

                # Evitar traslapes entre fichas
                puntasNew = [[minX,minY],[minX+ancho,minY],[minX,minY+alto],[minX+ancho,minY+alto]]
                for oldBox in oldBoxes:
                    oldBoxList = list(oldBox)
                    #print(oldBoxList)

                    # Se evaluan si alguno de los 4 puntos del cuadrado esta por dentro
                    # del cuadrado de otro cubo
                    for punta in puntasNew:
                        # Esta en X
                        if punta[0]>=oldBoxList[0] and punta[0]<=oldBoxList[0]+oldBoxList[2]:
                            # Esta en Y
                            if punta[1]>=oldBoxList[1] and punta[1]<=oldBoxList[1]+oldBoxList[3]:
                                overlap=True
                                #print("\nOVERLAP!\n")
                                                           
            if not(overlap):
                #minX y minY son el origen del cuadrado
                actualBox = (minX,minY,ancho,alto)
                #print("Cuadro cubo nuevo="+str(actualBox))
                bbox.append(actualBox)

                # Instanciacion de los trackers
                trackers.append(cv2.TrackerMIL_create())

                if newCubes:
                    checkers.append(trackers[-1].init(frameOrg,actualBox))
                else:
                    checkers.append(trackers[-1].init(detector.img,actualBox))

                # Creacion de la lista de distancias por cubo
                dists.append([])

                # Creacion de la lista de angulos por cubo
                angs.append([])
                

        return [bbox,trackers,checkers,dists,angs]



    
    def track_cubos(self,video):
        # Crear el objeto que hace el tracking
        #tracker = cv2.TrackerMIL_create()

        # Salir si el video no abre
        if not video.isOpened():
            print("No se pudo abrir el video")
            sys.exit()

        # determinar el numero de frames en el video
        # SI ESTO SE PUEDE EVITAR, AHORRARIA TIEMPO
        totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.alphaStep = (float)(180-self.R)/totalFrames
        #print("TotalFrames = "+str(totalFrames))
        #print("AlphaStep = "+str((self.alphaStep)))

        # Leer el primer frame
        ok,frame = video.read()
        if not ok:
            print('No se pudo leer el video')
            sys.exit()

        ###### ESTO ES SOLO PARA VIDEOS MUY GRANDES, SE ELIMINARA
        r = 800.0/frame.shape[1]
        dim = (800, int(frame.shape[0]*r))
        frame = cv2.resize(frame,dim, interpolation = cv2.INTER_AREA)
        altoImg,anchoImg,profundoImg = frame.shape
        #cv2.imshow("original", frame)

        # Setear el ancho global del video con fines de medicion de distancia
        self.width = anchoImg


        # Quitarle al frame la ventana el espacio de el windowCube
        ########frame = frame[:,:frame.shape[1]-self.thickWindowCube,:]
        #cv2.imshow("cortado", frame)
        #cv2.waitKey(0)

        # Usar una instancia de detectorObjetos, para determinar los cubos
        # en el primer frame
        detector = detectorObjetos(frame)
        firstFrame = True
        # Obtener los parametros del primer frame para hacer tracking 
        detectedCubes = self.get_trackers(frame,None,detector,False,altoImg,anchoImg,None,firstFrame)
        bbox = detectedCubes[0]
        trackers = detectedCubes[1]
        checkers = detectedCubes[2]
        dists = detectedCubes[3]
        angs = detectedCubes[4]

        firstFrame = False
        auxFlag = False

        while True:
            # Leer un nuevo frame
            check,frame = video.read()
            
            
            # Ventana para umbralizar nuevas fichas entrantes
            #windowCube = self.get_window_cube(frameOrg)
            
            if not check:
                # Esto se hace para los cubos que no salieron del video antes de que se terminara
                for (distVec,angVec) in zip(dists,angs):
                    self.distancias.append(distVec)
                    self.angulos.append(angVec)
                print("\nSe acabo el video")
                break
            
            ###### ESTO ES SOLO PARA VIDEOS MUY GRANDES, SE ELIMINARA
            frame = cv2.resize(frame,dim, interpolation = cv2.INTER_AREA)
            frameOrg = frame.copy()
            #auxFlag = False ####TROUBLE

            #print("Numero de cubos en tracking = "+str(len(bbox)))
            
            for idx,box in enumerate(bbox):
                checkers[idx] = check

                # Actualizar el tracker
                checkers[idx],box = trackers[idx].update(frame)
                bbox[idx] = box

                # Dibujar el recuadro
                if checkers[idx]:

                    # Calcular la distancia y meterla en la lista
                    # En esta lista se guarda la distancia hallada, relacionada con
                    # el angulo de la camara al tomar esa distancia

                    # Se evalua si la ventana horizontal esta cerca de los bordes verticales
                    if self.rotationDir == 'right':
                        if box[0] < self.umbralOut:
                            #print("\nSALIO UN CUBO DEL TRACKING\n")
                            self.distancias.append(dists[idx])
                            self.angulos.append(angs[idx])
                            trackers.remove(trackers[idx])
                            checkers.remove(checkers[idx])
                            bbox.remove(bbox[idx])
                            dists.remove(dists[idx])
                            angs.remove(angs[idx])

                        else:
                            '''
                            En cada frame se halla la distancia a cada ficha
                            por ahora ese valor va a ser igual siempre
                            ya que la deteccion se hace a partir de los cuadrados
                            que contienen a los cubos y actualmente, estos cuadrados
                            no cambian de tamanho
                            '''
                            #print(box)
                            dists[idx].append(self.get_dist_to_cam(box))
                            angs[idx].append(self.get_angulo_cubo(box))
                            #print("ok")
                            p1 = (int(box[0]), int(box[1]))
                            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
                            cv2.rectangle(frame, p1, p2, (0,255,0))

                    elif self.rotationDir == 'left':
                        # Se escoje otra coordenada de box y se compara
                        alasn = 0

                    elif self.rotationDir == 'up':
                        # Se escoje otra coordenada de box y se compara
                        alasn = 0

                    elif self.rotationDir == 'down':
                        # Se escoje otra coordenada de box y se compara
                        alasn = 0

            # Detectar nuevas fichas entrantes
            cuboEntrando = self.detectar_cubo_entrante(frame,detector,altoImg,anchoImg)
            #if cuboEntrando:
                #print("Hay cubos entrando\n")
            #else:
            if not cuboEntrando:
                if auxFlag:
                    # Ya se puede detectar el nuevo cubo
                   # print("\nLISTO PARA DETECTAR\n")
                    windowCube = self.get_window_cube(frameOrg)
                   # cv2.imshow("Franja detectora de nuevas fichas",windowCube)
                   # cv2.waitKey(0)
                    
                    newCubes = self.get_trackers(windowCube,frameOrg,detector,True,altoImg,anchoImg,bbox,firstFrame)
                    for (box,tracker,checker,dist,ang) in zip(newCubes[0],newCubes[1],newCubes[2],newCubes[3],newCubes[4]):

                        bbox.append(box)
                        trackers.append(tracker)
                        checkers.append(checker)
                        dists.append(dist)
                        angs.append(ang)
                           
                #else:
                   # print("No hay cubos entrando\n")
                
            auxFlag = cuboEntrando

            # Actualizar el angulo de la camara
            self.alpha = self.alpha + self.alphaStep
                
        
            #cv2.imshow("Tracking", frame)
            #cv2.waitKey(0)

        #cv2.destroyAllWindows()
        print("Se detectaron "+str(len(self.distancias))+" cubos, si,"+str(len(self.angulos)))


    @staticmethod
    def prueba():
        print('Hola, soy una prueba')
        return 5
        
##############################################################################
######PRUEBAS
##video = cv2.VideoCapture("videos/mul_red_cubes_1.MOV")
##imgRef = cv2.imread('images/cubo_rojo_15cm.jpg')
##
### Igualar el size de la imgref al del video
##imgRef = cv2.resize(imgRef, (800,448), interpolation = cv2.INTER_AREA)
###cv2.imshow("ImgRef", imgRef)
###cv2.waitKey(0)
###video = cv2.VideoCapture("videos/red_cube2.MOV")
###video = cv2.VideoCapture("videos/red_cube1.MOV")
##
##pixError = 20
##rotationDir = 'right'
##thickWindowCube = 200
##thickWindowDetect = 10
##umbralIn = 20
##umbralOut = 5
##
### Hallar los datos de distancia de la imagen de referencia (metodo estatico)
##rectRef = medidorDistancia.get_dist_ref(imgRef)
##
##
##med = medidorDistancia(pixError,rotationDir,thickWindowCube,
##                       thickWindowDetect,umbralIn,umbralOut,
##                       rectRef)
##med.track_cubos(video)
##
### Adquirir vector de salida con los angulos y distancias de cada cubo
##angs_dists = med.get_angs_dists()



        

        
        

    
 

