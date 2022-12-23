import arcade

# extend arcade's built in Window class
class Game(arcade.Window):
    # constructor
    def __init__(self, width, height, title):
        # call the Window class's constructor
        super().__init__(width, height, title)

        # set background color
        arcade.set_background_color(arcade.color.WHITE)

    # draws things on screen 60 times a second
    def on_draw(self):
        # ready to start drawing
        arcade.start_render()

def main():
    # create game window with with width, height, and name
    window = Game(640, 480, "Drawing Example")
    
    # keep window open until user closes it
    arcade.run()

main()