import numpy as np
import cv2
import math
import sys

class detectorObjetos:

    def __init__(self,img):
        self.img = img

    def segmentar_por_color(self,limL1,limU1,limL2,limU2,firstFrame):

        '''
            Este metodo recibe una imagen y unos rangos para umbralizar por color,
            basados en HSV. Devuelve la imagen umbralizada en formato binario
            (en blanco lo que corresponde al valor detectado y en negro al resto)
            
             Valores para segmentar la imagen en RGB
             Segmentacion de rojo puro
            lower_red = np.array([0,100,100])
            upper_red = np.array([10,255,255])

             Segmentacion de azul puro
            lower_blue = np.array([110,50,50])
            lower_blue = np.array([130,255,255])

             Segmentacion de verde puro
            lower_green = np.array([50,100,100])
            lower_green = np.array([70,255,255])
        '''

        # Conversion de la imagen de entrada de RGB a HSV
        img_hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        #cv2.imshow('hsv',img_hsv)

        #La idea de las dos mascaras fue tomada de aqui:
        # https://stackoverflow.com/questions/32522989/opencv-better-detection-of-red-color
        # Umbralizar la imagen HSV para obtener solo los valores rojo (o verde o azul...)
        mask1 = cv2.inRange(img_hsv, limL1, limU1)
        mask2 = cv2.inRange(img_hsv, limL2, limU2)

        mask = mask1|mask2

        

        # Ignorar las fichas que quedaron no salieron completas a la izquierda
        # Esto tambien deberia estar en funcion del sentido de giro

        # VER COMO CORREGIR ESTO
        

        if firstFrame:
            alto,ancho ,profundo = self.img.shape
            limit = ancho
            for i in range(ancho-1,0,-1):
                auxFlag = True
                for j in range(alto-1,0,-1):
                    if mask[j][i] == 255:
                        #print("Ya")
                        auxFlag = False
                        j=0
                if auxFlag:
                    limit = i
                    #print(limit)
                    break

            #cv2.imshow("Mask Original",mask)
            #cv2.imshow("Mask cutted",mask[:,:limit])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            mask = mask[:,:limit]
    
        return mask

    def detectar_cubos(self,minArea,firstFrame):
        """
        Este metodo encuentra los contornos exteriores a partir de la imagen
        umbralizada, elimina contornos muy pequenhos (equivalentes a errores)
        saca los cuadrados minimos que contienen los contornos y retorna una
        lista con las coordenadas de dichos cuadrados
        """

        # Hacer la segmentacion por color rojo
        mask = self.segmentar_por_color(np.array([0,70,50]),np.array([10,255,255]),np.array([170,70,50]),np.array([180,255,255]),firstFrame)
        
        # Encontrar los contornos y adquirir los externos
        image, contours, hier = cv2.findContours(mask.copy(), cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)

        # Adquirir los cuadrados minimos
        rectCubos = []
        for c in contours:
            
            # Adquirir el min area rect
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            
            # Convertir las coordenadas de flotante a entero
            box = np.int0(box)

            # Descartar los contornos cuya area sea menor que un valor dado
            d1 = math.sqrt(pow(box[1][0]-box[0][0],2)+pow(box[0][1]-box[1][1],2))
            d2 = math.sqrt(pow(box[3][0]-box[0][0],2)+pow(box[3][1]-box[0][1],2))
            area = d1*d2
            if area > minArea:
                rectCubos.append(box)    
                # Dibujar los contornos hallados
                #cv2.drawContours(self.img, [box], 0, (128, 128, 255)) 
                #print(box)
        #print(len(rectCubos))         
        #cv2.imshow("contours", self.img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        return rectCubos

    @staticmethod
    def detectar_cubo_referencia(imgRef):

        # ACA SE PUEDEN HACER MUCHAS MEJORAS DE REUSABILIDAD DEL CODIGO
        # Conversion de la imagen de entrada de RGB a HSV
        img_hsv = cv2.cvtColor(imgRef, cv2.COLOR_BGR2HSV)
        #cv2.imshow('hsv',img_hsv)

        #La idea de las dos mascaras fue tomada de aqui:
        # https://stackoverflow.com/questions/32522989/opencv-better-detection-of-red-color
        # Umbralizar la imagen HSV para obtener solo los valores rojo (o verde o azul...)

         # Hacer la segmentacion por color rojo
        limL1 = np.array([0,70,50])
        limU1 = np.array([10,255,255])
        limL2 = np.array([170,70,50])
        limU2 = np.array([180,255,255])
        
        mask1 = cv2.inRange(img_hsv, limL1, limU1)
        mask2 = cv2.inRange(img_hsv, limL2, limU2)

        mask = mask1|mask2

        #cv2.imshow('mask',mask)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        
        # Encontrar los contornos y adquirir los externos
        image, contours, hier = cv2.findContours(mask.copy(), cv2.RETR_LIST,
                cv2.CHAIN_APPROX_SIMPLE)
            
        # Adquirir el min area rect
        rect = cv2.minAreaRect(contours[0])

        return rect


########## Pruebas ##########
#img = cv2.imread('images/varios_cubos2.jpg')
#det = detectorObjetos(img)
#det.detectar_cubos(20)


####### Read video
##video = cv2.VideoCapture("videos/mul_red_cubes_1.MOV")
##ok, frame = video.read()
##
##if not ok:
##    print('Cannot read video file')
##    sys.exit()
##
### Resize if resolution is big
##r = 800.0/frame.shape[1]
##dim = (800, int(frame.shape[0]*r))
##frame = cv2.resize(frame,dim, interpolation = cv2.INTER_AREA)
##
##det = detectorObjetos(frame)
##det.segmentar_por_color(np.array([0,70,50]),np.array([10,255,255]),np.array([170,70,50]),np.array([180,255,255]),True)
###det.detectar_cubos(20)


##
### Prueba de deteccion de cubo de referencia
#imgRef = cv2.imread('images/cubo_rojo_10cm.jpg')
##imgRef = cv2.imread('images/red_rect.jpg')
##rect = detectorObjetos.detectar_cubo_referencia(imgRef)
