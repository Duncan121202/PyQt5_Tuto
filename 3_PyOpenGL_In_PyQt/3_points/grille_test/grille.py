from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# importation du module PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# importation du module contenant la class générée par Qtdesigner
from grille_ui import Ui_Dialog
from gen_grill import *


class mainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.angle = 0  # utilisé pour tourner la camera
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.openGLWidget = self.ui.openGLWidget  # raccourci

        self.l = flou(3, 5, 1)

    def setupUI(self):  # initialisation de la vue et création du timer
        self.openGLWidget.initializeGL() # appelé au premier affichage uniquement
        self.openGLWidget.resizeGL(800, 600)
        self.openGLWidget.paintGL = self.paintGL # raccourci

        timer = QTimer(self)  # Le timer
        timer.timeout.connect(self.openGLWidget.update)  # appelle la fonction en argument (sans parenthèse )
        #ici update appelle la fonction resizeGL et paintGL
        timer.start(10)  # lance le timer pour un temps de 10 ms entre chaque timeout

    def paintGL(self):  # réécriture de la fonction de base pour afficher la scène
                        # appelé a chaque 'update' lancé par le timer
        self.angle += 1
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)  # définition de la couleur du font,le dernier nombre est l'alpha/la transparence

        glEnable(GL_POINT_SMOOTH) # rond
        glPointSize(60) #taille initiale
        """changement de la taille des points avec la distance"""
        glPointParameterfv(GL_POINT_DISTANCE_ATTENUATION, (1, 1, 1)) #permet de diminuer la taille des points avec
        # la distance, (surtout les 2 derniers)
        glPointParameterfv(GL_POINT_SIZE_MAX, 32.0) # définit la taille maximum des points
        glPointParameterfv(GL_POINT_SIZE_MIN, 0.01) # définit la taille minimum des points
        """affichage de points"""
        glBegin(GL_LINES) # début de l'affichage des lignes

        glColor3f(1, 0, 0)
        for i in range(len(self.l)):
            if i%2==0:
                glVertex3fv(self.l[i])
                glVertex3fv(self.l[i+1])

        glEnd() # fin de l'affichage des lignes
        glMatrixMode(GL_PROJECTION)  # charge la matrice de projection
        """ on change ici les options de la projection sur l'écran """
        glLoadIdentity()  # charge une matrice identité
        gluPerspective(45.0, 4.0 / 3.0, 1, 200)  # fov , ratio , distance de vue proche, distance de vue de loin

        glMatrixMode(GL_MODELVIEW)  # charge la matrice de caméra
        """ on change ici la position de la caméra """
        glLoadIdentity()  # charge une matrice identité
        gluLookAt(0, 30, -30,
                  0, 10, 0,
                  0, 1, 0)
        # coordonnées de la position de la caméra  ,coordonnées du point vers lequel elle est dirigée, axe vertical de la caméra
        glRotatef(0.4*self.angle, 0, 1, 0)  # permet de tourner la caméra autour de l'axe x ,y ,z

        #glTranslatef( 0, 0, 0.1*self.angle)#permet de déplacer la camera ,
        # mais est impacté par la rotation de la camera



app = QApplication(sys.argv)
window = mainWindow()
window.setupUI() # on initialize le QOpenGLwidget
window.show()
sys.exit(app.exec_())
