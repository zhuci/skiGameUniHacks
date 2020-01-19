import arcade
import random
import os

SPRITE_SCALING = 0.5
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ski Game"
SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 50
SPRITE_SCALING_TREE = 0.15
SPRITE_SCALING_ROCK = 0.15
SPRITE_SCALING_LOG = 0.3

SPRITE_SCALING_BUNNY = 0.15

SPRITE_SCALING_PENGUIN = 0.1 #800x800
SPRITE_SCALING_FLAG = 0.6

MOVEMENT_SPEED = 5
JUMP_SPEED = 20 #6
JUMP_TIME = .5
DEFAULT_Y_POS = 50
BUNNY_SPEED = 2
LIVES = 5

BUFFER_TIME = 1.5 #for oops function



class MyGame(arcade.Window):
    """ Our custom Window Class"""
    time = 0 #every time on_update() runs, add delta_time to this - total time program running
    time_between_obstacles = 2
    time_last_obstacle = 0
    time_last_oops = 0

    time_last_flag = 0

    jumping = False
    time_jump_start = 0

    y_speed = 15

    score = 0


    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class initializer
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        # Don't show the mouse cursor
        self.set_mouse_visible(False)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_sprite_list = arcade.SpriteList()
        self.tree_sprite_list = arcade.SpriteList()
        self.rock_sprite_list = arcade.SpriteList()
        self.left_flag_sprite_list = arcade.SpriteList()
        self.right_flag_sprite_list = arcade.SpriteList()
        self.log_sprite_list = arcade.SpriteList()
        self.bunny_sprite_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("./images/penguin.png", SPRITE_SCALING_PENGUIN)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite_list.append(self.player_sprite)


    def on_draw(self):
        """ Draw everything """
        arcade.set_background_color(arcade.color.WHITE)
        arcade.start_render()
        point_list = ((0, 0), (SCREEN_WIDTH, 0), ((SCREEN_WIDTH/2), (2*SCREEN_HEIGHT)))
        arcade.draw_polygon_filled(point_list, arcade.color.ANTI_FLASH_WHITE)

        #draw non-player sprites
        self.tree_sprite_list.draw()
        self.rock_sprite_list.draw()
        self.left_flag_sprite_list.draw()
        self.right_flag_sprite_list.draw()
        self.log_sprite_list.draw()
        self.bunny_sprite_list.draw()

        #draw skis and shadow
        arcade.draw_ellipse_filled((self.player_sprite.center_x), (self.player_sprite.center_y - 50), 70, 50, arcade.color.MANATEE)
        arcade.draw_rectangle_filled((self.player_sprite.center_x - 15), (self.player_sprite.center_y - 40), 10, 20, arcade.color.LUST)
        arcade.draw_rectangle_filled((self.player_sprite.center_x + 15), (self.player_sprite.center_y -40), 10, 20, arcade.color.LUST)

        #draw player
        self.player_sprite_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 580, arcade.color.BLACK, 14)

        for i in range(LIVES):
            arcade.draw_ellipse_filled(300 + i * 50, 550, 20, 20, arcade.color.YELLOW)


    def on_update(self, delta_time): #delta_time is time since last call
        #self.coin_sprite_list.update()
        self.player_sprite_list.update()
        self.tree_sprite_list.update()
        self.rock_sprite_list.update()
        self.left_flag_sprite_list.update()
        self.right_flag_sprite_list.update()
        self.log_sprite_list.update()
        self.bunny_sprite_list.update()


        #check for collision with trees
        tree_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.tree_sprite_list)
        if(len(tree_hit_list) > 0):
            self.oops()


        #check for collision with rocks
        rock_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.rock_sprite_list)
        if(len(rock_hit_list) > 0 and not(self.jumping)):
            self.oops()


        #check for collision with logs
        log_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.log_sprite_list)
        if(len(log_hit_list) > 0 and not(self.jumping)):
            self.oops()

        #check for collision with bunnys
        bunny_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bunny_sprite_list)
        if(len(bunny_hit_list) > 0):
            self.oops()

        self.touch_border_check()

        #jumping stuff
        if(self.jumping):
            if(self.time - self.time_jump_start > JUMP_TIME):
                self.jumping = False
                self.player_sprite.center_y = DEFAULT_Y_POS
                self.player_sprite.change_y = 0
            elif(self.time - self.time_jump_start < 0.5*JUMP_TIME):
                self.player_sprite.change_y = JUMP_SPEED
            else:
                self.player_sprite.change_y = -JUMP_SPEED


        #launch obstacle
        if(self.time - self.time_last_obstacle > self.time_between_obstacles):
            n = random.random()
            if(n < 0.25):
                self.addTree()
            elif(n < 0.5):
                self.addLog()

            elif(n < 0.75):
                self.addRock()
            else:
                self.addBunny()

            self.time_last_obstacle = self.time

        #add flag
        if(self.time - self.time_last_flag > self.time_between_obstacles):
            self.addLFlag()
            self.addRFlag()
            self.time_last_flag = self.time

        #remove sprites
        for tree in self.tree_sprite_list:
            #check if tree left the screen
            if(tree.center_y < -300):
                tree.kill()
        for rock in self.rock_sprite_list:
            #check if tree left the screen
            if(rock.center_y < -300):
                rock.kill()
        for LFlag in self.left_flag_sprite_list:
            #check if tree left the screen
            if(LFlag.center_y < -300):
                LFlag.kill()
        for RFlag in self.right_flag_sprite_list:
            #check if tree left the screen
            if(RFlag.center_y < -300):
                RFlag.kill()
        for log in self.log_sprite_list:
            #check if tree left the screen
            if(log.center_y < -300):
                log.kill()
        for bunny in self.bunny_sprite_list:
            #check if tree left the screen
            if(bunny.center_y < -300):
                bunny.kill()

        #update times
        self.time += delta_time
        self.y_speed -= (1/(30*60))

        if(LIVES > 0):
            self.score = round(self.time,1)

    def addTree(self):
        #make tree
        tree = arcade.Sprite("./images/tree.png", SPRITE_SCALING_TREE)
        tree.center_x = 300
        tree.center_y = 1200 #fix this hack
        tree.change_y = -self.y_speed
        tree.change_x = (0.5*random.random() - 0.25) * tree.change_y
        #add tree to list
        self.tree_sprite_list.append(tree)

    def addRock(self):
        #make rock
        rock = arcade.Sprite("./images/rock.png", SPRITE_SCALING_ROCK)
        rock.center_x = 300
        rock.center_y = 1200 #fix this hack
        rock.change_y = -self.y_speed
        rock.change_x = (0.5*random.random() - 0.25) * rock.change_y
        #add rock to list
        self.rock_sprite_list.append(rock)

    def addLFlag(self):
        #make left flag
        flag = arcade.Sprite("./images/lFlag.png", SPRITE_SCALING_FLAG)
        flag.center_x = 300
        flag.center_y = 1200 #fix this hack
        flag.change_y = -self.y_speed
        flag.change_x = -0.25*flag.change_y
        self.left_flag_sprite_list.append(flag)

    def addRFlag(self):
        flag = arcade.Sprite("./images/rFlag.png", SPRITE_SCALING_FLAG)
        flag.center_x = 300
        flag.center_y = 1200 #fix this hack
        flag.change_y = -self.y_speed
        flag.change_x = 0.25 * flag.change_y
        self.right_flag_sprite_list.append(flag)

    def addLog(self):
        #make rock
        log = arcade.Sprite("./images/log.png", SPRITE_SCALING_LOG)
        log.center_x = 300
        log.center_y = 1200 #fix this hack
        log.change_y = -self.y_speed
        log.change_x = (0.5*random.random() - 0.25) * log.change_y
        #add rock to list
        self.log_sprite_list.append(log)

    def addBunny(self):
        #make rock
        bunny = arcade.Sprite("./images/bunny.png", SPRITE_SCALING_BUNNY)
        bunny.center_x = 0
        bunny.center_y = 700 #fix this hack
        bunny.change_y = -self.y_speed
        bunny.change_x = BUNNY_SPEED
        #add rock to list
        self.bunny_sprite_list.append(bunny)

    def on_key_press(self, key, modifiers):
        #Called whenever a key is pressed
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.jumping = True
            self.time_jump_start = self.time

    def on_key_release(self, key, modifiers):
        #Called when the user releases a key.
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def touch_border_check(self):
        player_width = 800 * SPRITE_SCALING_PENGUIN
        player_left = self.player_sprite.center_x - player_width/2
        player_right = self.player_sprite.center_x + player_width/2
        if player_left <= 0 or player_right >= 600:
            self.oops()


    counter = 0
    def oops(self):
        if(self.time - self.time_last_oops > BUFFER_TIME):
            self.time_last_oops = self.time
            global LIVES
            if LIVES > 1:
                LIVES -= 1
            elif LIVES == 1:
                LIVES -= 1
                self.y_speed = 0






def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
