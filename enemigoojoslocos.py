import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def draw_sphere(eye1_horizontal_angle, eye1_vertical_angle, eye2_horizontal_angle, eye2_vertical_angle):
    # Create a 3D metallic sphere using quadric object
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)

    # Set material for the sphere (metallic gray)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
    
    gluSphere(quad, 1, 50, 50)  # Large sphere with radius 1

    # Draw the first white eye
    glPushMatrix()
    # Set material for the white eye
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Apply eye1 movement based on horizontal and vertical angles
    glRotatef(eye1_horizontal_angle, 0.0, 1.0, 0.0)  # Horizontal eye movement
    glRotatef(eye1_vertical_angle, 1.0, 0.0, 0.0)    # Vertical eye movement
    glTranslatef(0.0, 0.0, 1.0)  # Position at the front of the large sphere
    gluSphere(quad, 0.1, 20, 20)  # Small white sphere as the eye
    glPopMatrix()

    # Draw the black pupil for the first eye
    glPushMatrix()
    # Set material for the black pupil
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

    # Apply the same rotations for the pupil
    glRotatef(eye1_horizontal_angle, 0.0, 1.0, 0.0)  # Horizontal pupil movement
    glRotatef(eye1_vertical_angle, 1.0, 0.0, 0.0)    # Vertical pupil movement
    glTranslatef(0.0, 0.0, 1.1)  # Slightly forward from the white eye
    gluSphere(quad, 0.03, 20, 20)  # Small black sphere as the pupil
    glPopMatrix()

    # Draw the second white eye
    glPushMatrix()
    # Set material for the white eye
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Apply eye2 movement based on horizontal and vertical angles
    glRotatef(eye2_horizontal_angle, 0.0, 1.0, 0.0)  # Horizontal eye movement
    glRotatef(eye2_vertical_angle, 1.0, 0.0, 0.0)    # Vertical eye movement
    glTranslatef(1.5, 0.0, 1.0)  # Position at the front of the large sphere but offset
    gluSphere(quad, 0.1, 20, 20)  # Small white sphere as the second eye
    glPopMatrix()

    # Draw the black pupil for the second eye
    glPushMatrix()
    # Set material for the black pupil
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

    # Apply the same rotations for the pupil
    glRotatef(eye2_horizontal_angle, 0.0, 1.0, 0.0)
    glRotatef(eye2_vertical_angle, 1.0, 0.0, 0.0)
    glTranslatef(1.5, 0.0, 1.1)  # Slightly forward from the second white eye
    gluSphere(quad, 0.03, 20, 20)  # Small black sphere as the pupil
    glPopMatrix()

def init_opengl():
    # Set up OpenGL lighting and shading
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Light and material properties for metallic look
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])

    # Material defaults (for white ambient/diffuse color)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

def main():
    # Initialize Pygame and create window
    pygame.init()
    display = (900, 900)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    init_opengl()  # Set up OpenGL
    
    # Perspective setup
    gluPerspective(45, display[0] / display[1], 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)  # Move back the camera

    # Main loop
    running = True
    sphere_rotation_angle = 0
    eye1_horizontal_angle = 0
    eye1_vertical_angle = 0
    eye2_horizontal_angle = 0
    eye2_vertical_angle = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear buffers

        # Rotate the sphere
        glPushMatrix()
        glRotatef(sphere_rotation_angle, 1, 1, 0)  # Rotate the whole sphere
        draw_sphere(eye1_horizontal_angle, eye1_vertical_angle, eye2_horizontal_angle, eye2_vertical_angle)  # Draw the sphere with the two eyes
        glPopMatrix()
        
        sphere_rotation_angle += 1  # Increment rotation for animation
        
        # Change the eyes' horizontal and vertical angles for gyroscopic movement
        eye1_horizontal_angle = (eye1_horizontal_angle + 1) % 360
        eye1_vertical_angle = (eye1_vertical_angle + 0.5) % 360
        eye2_horizontal_angle = (eye2_horizontal_angle + 0.5) % 360
        eye2_vertical_angle = (eye2_vertical_angle + 0.2) % 360

        pygame.display.flip()  # Update the display
        pygame.time.wait(10)  # Add delay for smoother animation

    pygame.quit()

if __name__ == "__main__":
    main()
