# @author David Aiken 9/30/26
from menu import Menu
from PPM_Image import *
import random
'''
when constructing a Menu, each option must start with "o".

functions:
create_new_canvas_from_ppm_file():
    reads line[2:] of a .ppm file and sets it as the new image
create_new_solid_canvas():
    creates a new canvas object to your specifications
add_rectangle():
    overlays a rectangle on your active canvas
save_canvas():
    writes your active image to a .ppm file
print_image():
    prints the tuple matrix in the terminal to help see your progress before
    writing to a .ppm file.
    I use it for testing.
    You probably don't want to call this if your canvas is huge.
quit():
    prints a goodbye message.
'''
ON = True
OFF = False
# initialize global i
i = None

def create_new_canvas_from_ppm_file():
    global i
    try:
        filename = input(f'What file would you like to use: ')
        i = PPM_Image('FROM_FILE', filename)
        print(f'\n{filename} has been imported.\n')
    except:
        print("\nLooks like there was a typo or that image isn't in the same file.\nPlease try again.\n")  

def create_new_solid_canvas():
    global i
    try:
        width = int(input("How many columns wide would you like your canvas: "))
        height = int(input("How many rows tall would you like your canvas: "))
        color = input("What hexidecimal color would you like the canvas to be: ")
        i = PPM_Image('ONE_COLOR', width, height, color)
        print(f'\nNew canvas has been created.\n')
    except:
        print(f'\nLooks like an invalid character was entered.\n'
              f'Select this option again and use only integers\n')

def add_rectangle():
    global i
    try:
        topLrow = int(input("What row would you like the top left corner of the rectangle to start: "))
        topLcol = int(input("What column would you like the top left corner of the rectangle to start: "))
        width = int(input("How many columns wide would you like your rectangle: "))
        height = int(input("How many rows tall would you like your rectangle: "))
        color = input("What hexidecimal color would you like the rectangle to be: ")
        i.draw_rect(topLrow, topLcol, height, width, color)
        print(f'\nRectangle has been added.\n')
    except:
        print(f'\nLooks like an invalid character was entered.\n'
              f'If you\'re serious about rectagles like I am, select this option again\n')

def create_color_map():
    global i
    a = int(input("How many colors would you like in your color map: "))
    while a < 1:
        print("\nCan't display a color map with less than 1 color.\n")
        a = int(input("Please Enter the >=1 colors you'd like to display: "))
    b = int(input("Threshold for color difference as an integer: "))
    while b < 0 or b > 255:
        if b < 0: print("\nThreshold cannot be negative.\n")
        if b > 255: print("\nThreshold cannot be greater than 255.\n")
        b = int(input("Please enter a threshold >0 and <255: "))
    i.create_color_map(a,b)

def overlay_image():
    global i
    filename = input(f'What file would you like to use: ')
    row  = int(input(f'What row would you like to start at: '))
    col = int(input(f'What column would you like to start at: '))
    i.overlay_image(filename, row, col)    

def save_canvas():
    global i
    try:
        i.save_canvas()
        print(f'\nImage has been printed to a .ppm file\n')
    except:
        print(f'\nLooks like we haven\'t built a canvas yet.\n')    

def print_image():
    global i
    try:
        for row in i.image:
            print(row)         
        print(f'height: {len(i.image)}, width; {len(i.image[0])}')   
    except:
        print("\nLooks like we haven't set up a canvas yet\n")

def quit():
    farewells =['Adios', 'Au revior', 'Goodbye', 'Auf Wiedersehen', 
                'Arrivederci', 'Sayonara']
    print()
    print(random.choice(farewells)) 
    print()  

while True:
    m = Menu(o1 = (ON, 'Create New Canvas from PPM File', create_new_canvas_from_ppm_file),
        o2 = (ON, 'Create New Solid Canvas', create_new_solid_canvas),
        o3 = (OFF if i is None else ON, 'Add Rectangle', add_rectangle),
        o4 = (OFF if i is None else ON, 'Create Color Map', create_color_map),
        o5 = (OFF if i is None else ON, 'Overlay Image from PPM File', overlay_image),
        oS = (OFF if i is None else ON, "Save Canvas", save_canvas),
        oP = (OFF if i is None else ON, 'Print Current Image \n(!!!only use Print with small canvases for testing!!!)', print_image),
        oQ = (ON, 'Quit', quit))

    func, *args = m.display_menu()
    func(*args)
    if func == quit:
        break
    