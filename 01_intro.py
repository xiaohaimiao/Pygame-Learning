#pgzrun intro.py

alien = Actor('alien')
alien.pos = 0, 0
#width
WIDTH = 1000
HEIGHT = alien.height + 900

def draw():
    screen.clear()
    alien.draw()
def update():
    alien.left += 10
    alien.top += 5
    if alien.left > WIDTH:
        alien.right = 0
    if alien.top > HEIGHT:
        alien.bottom = 0
def on_mouse_down(pos):
    if alien.collidepoint(pos):
        print("Eek!")
        
    else:
        print("You missed me!")