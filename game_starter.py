import arcade

# Define constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
GAME_TITLE = "Feed Zeke"
GAME_SPEED = 1/120

ZEKE_SCALING = 0.1
TILE_SCALING = 0.4
FOOTBALL_SCALING = 0.4

ZEKE_RIGHT = arcade.load_texture('images/Zeke_Right.png', mirrored = False, scale = ZEKE_SCALING)
ZEKE_LEFT = arcade.load_texture('images/Zeke_Right.png', mirrored = True, scale = ZEKE_SCALING)

MOVESPEED = 5
GRAVITY = 1

STARTSCREEN = 0
CONTROLSSCREEN = 1
GAME_RUNNING = 2
FINAL_SCREEN = 3

class FeedZeke(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.center_x = WINDOW_WIDTH/2
        self.center_y = WINDOW_HEIGHT/2
        self.player_list = None
        self.wall_list = None
        self.football_list = None
        self.defender_list = None
        self.start_button = None
        self.start_button_list = None
        self.button_list = None
        self.background = None
        self.score = None
        self.level = None
        self.jump = None
        self.defender = None
        self.defender_direction = None
        self.physics_engine = None
        self.current_state = STARTSCREEN
        self.flag = None
        self.play_game = None

        # Put the title, instructions, and congratulations screens into a list
        self.instructions = []
        texture = arcade.load_texture('images/Start Screen.jpg')
        self.instructions.append(texture)

        texture = arcade.load_texture('images/Introduction Screen.jpg')
        self.instructions.append(texture)

        texture = arcade.load_texture('images/ada.png')
        self.instructions.append(texture)

    def setup(self):
        """ Setup the game (or reset the game) """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.football_list = arcade.SpriteList()
        self.defender_list = arcade.SpriteList()
        self.start_button_list = []
        self.button_list = []
        self.background = arcade.load_texture('images/Cowboys_Stadium.jpeg')
        self.score = 0
        self.level = 1
        self.jump = 18
        self.defender_direction = -1
        self.flag = 1
        self.play_game = 0

        # Creates the Zeke player Sprite and create his starting position
        self.player_sprite = Zeke_Player()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # Set's up the Start Button
        self.start_button = StartTextButton(600, 90, self.game_start)
        self.start_button_list.append(self.start_button)

        # Set's up the text button's for the trivia answer's

        self.eagles_button = EaglesTextButton(300, 100, self.check_eagle_answer)
        self.button_list.append(self.eagles_button)

        self.redskins_button = RedskinsTextButton(600, 100, self.check_redskin_answer)
        self.button_list.append(self.redskins_button)

        self.giants_button = GiantsTextButton(900, 100, self.check_giant_answer)
        self.button_list.append(self.giants_button)

        # Update the game to go to the first level
        self.level_updater()

        # Create the physics engine between Zeke and all platforms
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game(self):
        """ Called when it is time to draw the world """
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT,
                                      self.background)
        # Draw's all of the sprites
        self.wall_list.draw()
        self.football_list.draw()
        self.player_list.draw()
        self.defender_list.draw()
        if self.level%3 == 0:
            for button in self.button_list:
              button.draw()

        # Displays the score and current level to the screen
        score = f"Score: {self.score}"
        arcade.draw_text(score, 10, 70, arcade.color.WHITE, 20)
        level = f"Level: {self.level}"
        arcade.draw_text(level, 10, 660, arcade.color.WHITE, 20)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == STARTSCREEN:
            self.draw_instructions_page(0)

        elif self.current_state == CONTROLSSCREEN:
            self.draw_instructions_page(1)
            self.start_button.draw()

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        elif self.current_state == FINAL_SCREEN:
            self.draw_instructions_page(2)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # If the player clicks on the title screen, move to the introduction screen
        if self.current_state == STARTSCREEN:
            self.current_state = CONTROLSSCREEN

        check_mouse_press_for_buttons(self, x, y, self.start_button_list)
        check_mouse_press_for_buttons(self, x, y, self.button_list)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        check_mouse_release_for_buttons(x, y, self.start_button_list)
        check_mouse_release_for_buttons(x, y, self.button_list)

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""
        self.player_list.update()
        self.defender_list.update()
        if self.current_state == GAME_RUNNING:
            self.physics_engine.update()
            self.defender_movement()
            self.if_tackled()
            self.collect_football()
            self.if_fall()
            self.next_level()
            if self.level == 13:
                self.current_state = FINAL_SCREEN

    # Defines the boundaries a defender can move in for each level
    def defender_movement(self):
        for defender in self.defender_list:
            defender.change_x = self.defender_direction
            if self.level == 7:
                if defender.center_x < 300:
                    self.defender_direction = 1
                elif defender.center_x > 1000:
                    self.defender_direction = -1
            elif self.level == 8:
                if defender.center_x < 200:
                    self.defender_direction = 1
                elif defender.center_x > 1000:
                    self.defender_direction = -1

    # If Zeke runs into a defender, reset the level, reset Zeke's position,
    # and remove ten points from the score
    def if_tackled(self):

        defender_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.defender_list)

        for defender in defender_hit_list:
            self.score -= 10
            self.level_updater()
            self.player_sprite.center_x = 64
            self.player_sprite.center_y = 150

    # When Zeke collects a football, remove it from the screen and add ten points to the score
    def collect_football(self):

        football_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.football_list)

        for football in football_hit_list:
            football.remove_from_sprite_lists()
            self.score += 10

    #If Zeke falls to the bottom of the screen, subtract his score by 10
    def if_fall(self):

        if self.player_sprite.top < 0:
            self.score -= 10

    # Moves Zeke to the next screen
    def next_level(self):

        if self.player_sprite.center_x >= WINDOW_WIDTH:
            self.level += 1
            self.jump += 1
            self.level_updater()
            self.player_sprite.center_x = 64
            self.player_sprite.center_y = self.player_sprite.center_y

    def on_key_press(self, key, modifiers):
        # Makes the Zeke Player Sprite jump up based on the current jump level
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = self.jump

        # Makes the Zeke Player move left and right on the screen
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVESPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVESPEED

        # This is a test to show off how Zeke needs to increase his jump by playing through each level
        if key == arcade.key.KEY_7:
            self.level = 7
            self.level_updater()


    def on_key_release(self, key, modifiers):

        # When the user stops pushing the up and down or A and D buttons,
        # Stop changing Zeke's direction from left to right
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    # Updates each level based on Tiled map files
    def level_updater(self):
        if self.level < 13:
            # Defines the format each Tiled map file should use
            map_name = f"map_level_{self.level}.tmx"

            # Defines the layers from the Tiled file that each list will correspond to
            platforms_layer_name = 'Platforms'
            footballs_layer_name = 'Football'
            defenders_layer_name = 'Defender'

            # Sets up the name of the map file that should be set up
            my_map = arcade.tilemap.read_tmx(map_name)

            # Connects each Sprite list to the Tiled Layers
            self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
            self.football_list = arcade.tilemap.process_layer(my_map, footballs_layer_name, FOOTBALL_SCALING)
            self.defender_list = arcade.tilemap.process_layer(my_map, defenders_layer_name, TILE_SCALING)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

            # Changes the background based on which level the user is currently on
            if self.level%3 == 0:
                self.flag = 0
                self.background = arcade.load_texture("images/Cowboys_Office.jpeg")
            else:
                self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")

    def game_start(self):
        if self.play_game == 0:
            self.setup()
            self.current_state = GAME_RUNNING
            self.play_game = 1

    def check_eagle_answer(self):
        if self.flag == 0:
            if self.level == 9:
                self.score += 50
                self.flag = 1
            else:
                self.score -= 20
                self.flag = 1

    def check_redskin_answer(self):
        if self.flag == 0:
            if self.level == 6:
                self.score += 50
                self.flag = 1
            else:
                self.score -= 20
                self.flag = 1

    def check_giant_answer(self):
        if self.flag == 0:
            if self.level == 3 or self.level == 12:
                self.score += 50
                self.flag = 1
            else:
                self.score -= 20
                self.flag = 1

class Zeke_Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        # Put the Zeke left and right textures in a list and set the player sprites texture
        # to the right by default
        self.textures.append(ZEKE_LEFT)
        self.textures.append(ZEKE_RIGHT)
        self.set_texture(1)

    def update(self):

        # Change Zeke's texture based on which direction he is moving
        if self.change_x > 0:
            self.set_texture(1)
        elif self.change_x < 0:
            self.set_texture(0)

        # Prevent Zeke from moving past the left edge of the screen
        if self.left < 0:
            self.left = 0

        # If Zeke falls to the bottom of a screen, reset his position
        if self.top < 0:
            self.center_x = 64
            self.center_y = 150

# The Parent Class for all text buttons
class TextButton:

    def __init__(self,
                 center_x, center_y,
                 width, height,
                 text,
                 font_size=18,
                 font_face="Times New Roman",
                 face_color=arcade.color.WHITE,
                 highlight_color=arcade.color.DARK_BLUE,
                 shadow_color=arcade.color.BLUE,
                 button_height=2):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.pressed = False
        self.face_color = face_color
        self.highlight_color = highlight_color
        self.shadow_color = shadow_color
        self.button_height = button_height

    def draw(self):
        """ Draw the button """
        if not self.pressed:
            color = self.face_color
        else:
            color = arcade.color.LIGHT_BLUE

        texture = arcade.load_texture("images/Button Texture.png")

        arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width,
                                     self.height, texture)

        x = self.center_x
        y = self.center_y
        if not self.pressed:
            x -= self.button_height
            y += self.button_height

        arcade.draw_text(self.text, x, y,
                         arcade.color.BLACK, font_size=self.font_size,
                         width=self.width, align="center",
                         anchor_x="center", anchor_y="center")

    # Change the boolean value if the button is pressed or released

    def on_press(self):
        self.pressed = True

    def on_release(self):
        self.pressed = False


# Function to check whether the users mouse clicks within the text box's boundaries
def check_mouse_press_for_buttons(self, x, y, button_list):

    for button in button_list:
        if x > button.center_x + button.width / 2:
            continue
        if x < button.center_x - button.width / 2:
            continue
        if y > button.center_y + button.height / 2:
            continue
        if y < button.center_y - button.height / 2:
            continue
        button.on_press()

# Determine what action must be taken after the button is pressed
def check_mouse_release_for_buttons(_x, _y, button_list):

    for button in button_list:
        if button.pressed:
            button.on_release()

# Create the Start Button on the Title Screen
class StartTextButton(TextButton):

    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "Start", 18, "Times New Roman")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class EaglesTextButton(TextButton):

    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "EAGLES", 18, "Times New Roman")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class RedskinsTextButton(TextButton):

    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "REDSKINS", 18, "Times New Roman")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

class GiantsTextButton(TextButton):

    def __init__(self, center_x, center_y, action_function):
        super().__init__(center_x, center_y, 100, 40, "GIANTS", 18, "Times New Roman")
        self.action_function = action_function

    def on_release(self):
        super().on_release()
        self.action_function()

def main():
    window = FeedZeke()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()