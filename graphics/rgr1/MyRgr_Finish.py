from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
import colorsys

import math
import sys

xRot = 0
xPos = 0
zPos = 0
playerHeight = 0

isPlayerLightEnabled = True
isFireplaceLightEnabled = True
isMoonLightEnabled = True
isMoon = True

global tl_texture
global floor_texture
global wall1_texture
global wall2_texture
global wall3_texture
global wall4_texture

posDelta = 1


def togglePlayerLight():
    global isPlayerLightEnabled
    isPlayerLightEnabled = (isPlayerLightEnabled != True)

    if isPlayerLightEnabled:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)


def toggleFireplaceLight():
    global isFireplaceLightEnabled
    isFireplaceLightEnabled = (isFireplaceLightEnabled != True)

    if isFireplaceLightEnabled:
        glEnable(GL_LIGHT2)
    else:
        glDisable(GL_LIGHT2)


def toggleMoonLight():
    global isMoonLightEnabled
    isMoonLightEnabled = (isMoonLightEnabled != True)

    if isMoonLightEnabled:
        glEnable(GL_LIGHT3)
    else:
        glDisable(GL_LIGHT3)


def toggleMoonLight4():
    global isMoon
    isMoon = (isMoon != True)

    if isMoon:
        glEnable(GL_LIGHT4)
    else:
        glDisable(GL_LIGHT4)


def specialKeys(key, x, y):
    global xRot
    global zPos
    global xPos
    global playerHeight

    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        zPos += posDelta * math.cos(math.radians(xRot))
        xPos += posDelta * math.sin(math.radians(xRot))
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        zPos -= posDelta * math.cos(math.radians(xRot))
        xPos -= posDelta * math.sin(math.radians(xRot))
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        xRot -= 5
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        xRot += 5
    if key == GLUT_KEY_F1:
        togglePlayerLight()
        print("Player light toggled")
    if key == GLUT_KEY_F2:
        toggleFireplaceLight()
        print("Fireplace light toggled")
    if key == GLUT_KEY_F3:
        toggleMoonLight()
        print("Moon light toggled")
    if key == GLUT_KEY_F4:
        toggleMoonLight4()
        print("Moon light toggled")

    print("x={}, z={}, angle={}".format(xPos, zPos, xRot))
    glutPostRedisplay()  # Вызываем процедуру перерисовки


def load_texture(file_name: str):
    image = Image.open(file_name)
    image.load()  # this is not a list, nor is it list()'able
    width, height = image.size
    textureData = np.asarray(image)
    textureData = textureData[::-1]
    image.close()

    texId = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texId)

    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    if "png" in file_name:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    else:
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)

    return texId


def drawWalls(xSize, ySize, zSize):
    glPushMatrix()

    glTranslatef(-xSize / 2, -ySize / 2, -zSize / 2)
    glEnable(GL_TEXTURE_2D)

    # front
    glBindTexture(GL_TEXTURE_2D, wall1_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glEnd()

    # back
    glBindTexture(GL_TEXTURE_2D, wall2_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, zSize)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)
    glEnd()

    # right
    glBindTexture(GL_TEXTURE_2D, wall3_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(xSize, 0, 0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(xSize, ySize, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, zSize)
    glEnd()

    # left
    glBindTexture(GL_TEXTURE_2D, wall4_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, zSize)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, ySize, zSize)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glEnd()

    # bottom
    glBindTexture(GL_TEXTURE_2D, floor_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, 0, zSize)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 0, zSize)
    glEnd()

    # top
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, ySize, 0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, zSize)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, zSize)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, ySize, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def drawRoom():
    glPushMatrix()
    drawWalls(80, 40, 80)

    glPushMatrix()
    glTranslate(-20, 0, -30)
    drawTl(10, 20)
    glPopMatrix()

    drawFireplaceLight()
    glPopMatrix()


def drawTl(xSize, ySize):
    glPushMatrix()

    glTranslatef(-xSize / 2, -(ySize + 4) / 2, 0)
    glEnable(GL_TEXTURE_2D)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D, tl_texture)

    glTranslatef(xSize / 2, -6, xSize)
    glRotate(90, 0, 1, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(xSize, 0, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(xSize, ySize, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, ySize, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glPopMatrix()


def drawPlayerLight():
    global xRot
    global xPos
    global zPos
    if isPlayerLightEnabled:
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glEnable(GL_LIGHT1)
        glLight(GL_LIGHT1, GL_POSITION, (xPos, 0, -zPos + 20, 1))
        glLight(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glLight(GL_LIGHT1, GL_DIFFUSE, (0.4, 0.4, 0.4, 1))
        glLight(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0)
        glLight(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.0004)
        glPopMatrix()
    else:
        glDisable(GL_LIGHT1)


def drawMoonLight():
    if isMoonLightEnabled:
        glPushMatrix()
        glLoadIdentity()

        glLight(GL_LIGHT3, GL_POSITION, (1, 0, -1, 0))
        glLight(GL_LIGHT3, GL_DIFFUSE, (0, 14, 60, 255))
        glLight(GL_LIGHT3, GL_SPECULAR, (0, 14, 60, 255))
        glPopMatrix()
    else:
        glDisable(GL_LIGHT3)


def drawMoonLight4():
    if isMoon:
        glPushMatrix()
        glLoadIdentity()

        glLight(GL_LIGHT4, GL_POSITION, (1, 1, 1, 0))
        glLight(GL_LIGHT4, GL_DIFFUSE, (0, 14 / 255, 60 / 255, 1))
        glLight(GL_LIGHT4, GL_SPECULAR, (0, 14 / 255, 60 / 255, 1))
        glPopMatrix()
    else:
        glDisable(GL_LIGHT4)


def drawFireplaceLight():
    if isFireplaceLightEnabled:
        glPushMatrix()
        glLoadIdentity()

        glEnable(GL_LIGHT2)
        glLight(GL_LIGHT2, GL_POSITION, (0, 1, 75, 1))
        glLight(GL_LIGHT2, GL_DIFFUSE, (241, 128, 53, 255))
        glLight(GL_LIGHT2, GL_SPECULAR, (241, 128, 53, 255))

        glLight(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 0)
        glLight(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.0008)
        glPopMatrix()
    else:
        glDisable(GL_LIGHT2)


def draw():
    global xRot
    global zPos
    global xPos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    drawPlayerLight()
    drawMoonLight()
    drawMoonLight4()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-10.0, 10.0, -10.0, 10.0, 10.0, 500.0)
    glRotate(xRot, 0, 1, 0)

    y = -math.sin(math.radians(playerHeight)) * 3
    glTranslate(-xPos, y, zPos)
    glMatrixMode(GL_MODELVIEW)
    drawRoom()
    glutSwapBuffers()


def init():
    global tl_texture
    global floor_texture
    global wall1_texture
    global wall2_texture
    global wall3_texture
    global wall4_texture

    glClearColor(0, 0, 0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glFrustum(-10.0, 10.0, -10.0, 10.0, 10.0, 500.0)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glAlphaFunc(GL_GREATER, 0.5)
    glEnable(GL_ALPHA_TEST)

    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT4)

    tl_texture = load_texture("im/xx.png")
    floor_texture = load_texture("im/floor.jpg")
    wall1_texture = load_texture("im/stenR_L.jpg")
    wall2_texture = load_texture("im/zad.jpg")
    wall3_texture = load_texture("im/dor.jpg")
    wall4_texture = load_texture("im/stenR_L.jpg")


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(350, 20)

    glutInit(sys.argv)

    glutCreateWindow(b'RGR')
    glutDisplayFunc(draw)
    glutSpecialFunc(specialKeys)

    init()

    glutMainLoop()
