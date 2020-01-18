import arcade
import random
import os

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ski Game"
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
SPRITE_SCALING_TREE = 0.1
SPRITE_SCALING_WOLF = 0.5
SPRITE_SCALING_BOULDER = 0.5
SPRITE_SCALING_BUNNY = 0.4
MOVEMENT_SPEED = 5

def draw_background():
    arcade.set_background_color(arcade.color.WHITE)
    point_list = ((0, 0), (SCREEN_WIDTH, 0), ((SCREEN_WIDTH/2), (2*SCREEN_HEIGHT)))
    arcade.draw_polygon_filled(point_list, arcade.color.DESERT)


    """arcade.draw_lrtb_rectangle_filled(0,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_HEIGHT,
        arcade.color.WHITE)"""

class Person(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


"""
class Coin(arcade.Sprite):

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()
"""
class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        # Set up the player info
        self.player_sprite = None


        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.tree_sprite_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()


        # Set up the player
        self.player_sprite = ("./images/tree.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite_list.append(self.player_sprite)


    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.tree_sprite_list.draw()
        self.player_list.draw()
        arcade.stop_render()

    def on_update(self, delta_time):
        #self.coin_sprite_list.update()
        self.player_list.update()

    def addTree():
        #make tree
        tree = arcade.Sprite("./images/tree.png", SPRITE_SCALING_TREE)
        tree.center_x = 300
        tree.center_y = 300
        #add tree to list
        tree_sprite_list.append(tree)

    def addBunny():
        #make addBunny
        bunny = arcade.Sprite("./images/bunny.png", SPRITE_SCALING_BUNNY)



    def world_to_screen(x,y,scaling):
        pass


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        jump_progress = false
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            if jump_progress == False:
                self.player_sprite.change_y = 2*MOVEMENT_SPEED
                jump_progress == True
            elif jump_progress == True:
                    self.player_sprite.change_y = 0







    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    """arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.start_render()
    draw_background()
    window = MyGame()
    window.setup()
    arcade.finish_render()
    arcade.run()"""
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
