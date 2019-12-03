import arcade

# Define constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
GAME_TITLE = "Feed Zeke"
GAME_SPEED = 1/60

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

class FeedZeke(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.center_x = WINDOW_WIDTH/2
        self.center_y = WINDOW_HEIGHT/2
        self.player_list = None
        self.wall_list = None
        self.moving_platform_list = None
        self.all_wall_list = None
        self.football_list = None
        self.defender_list = None
        self.background = None
        self.score = None
        self.level = None
        self.jump = None
        self.defender = None
        self.defender_direction = None
        self.physics_engine = None
        self.current_state = STARTSCREEN

        # Put the title and instructions screens into a list
        self.instructions = []
        texture = arcade.load_texture('images/Start Screen.jpg')
        self.instructions.append(texture)

        texture = arcade.load_texture('images/potato.png')
        self.instructions.append(texture)

    def setup(self):
        """ Setup the game (or reset the game) """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.football_list = arcade.SpriteList()
        self.defender_list = arcade.SpriteList()
        self.moving_platform_list = arcade.SpriteList()
        self.all_wall_list = arcade.SpriteList()
        self.background = arcade.load_texture('images/Cowboys_Stadium.jpeg')
        self.score = 0
        self.level = 1
        self.jump = 18
        self.defender_direction = -1

        # Creates the Zeke player Sprite and create his starting position
        self.player_sprite = Zeke_Player()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        # Update the game to go to the first level
        self.level_updater()

        # Create the physics engine between Zeke and all platforms
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.all_wall_list, GRAVITY)

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

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # If the player clicks on the title screen, move to the introduction screen
        if self.current_state == STARTSCREEN:
            self.current_state = CONTROLSSCREEN

        # If the player clicks on the introduction screen, move to the first level screen
        elif self.current_state == CONTROLSSCREEN:
            self.setup()
            self.current_state = GAME_RUNNING

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

    # Defines the boundaries a defender can move in for each level
    def defender_movement(self):
        for defender in self.defender_list:
            defender.change_x = self.defender_direction
            if self.level == 7:
                if defender.center_x < 400:
                    self.defender_direction = 1
                elif defender.center_x > 800:
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
            moving_platforms_name = 'Moving Platforms'

            # Sets up the name of the map file that should be set up
            my_map = arcade.tilemap.read_tmx(map_name)

            # Connects each Sprite list to the Tiled Layers
            self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
            self.football_list = arcade.tilemap.process_layer(my_map, footballs_layer_name, FOOTBALL_SCALING)
            self.defender_list = arcade.tilemap.process_layer(my_map, defenders_layer_name, TILE_SCALING)
            self.moving_platform_list = arcade.tilemap.process_layer(my_map, moving_platforms_name, TILE_SCALING)

            # Puts the stationary and moving platforms all into one list
            for wall in self.wall_list:
                self.all_wall_list.append(wall)
            for platform in self.moving_platform_list:
                self.all_wall_list.append(platform)

            # Changes the background based on which level the user is currently on
            if self.level%3 == 0:
                self.background = arcade.load_texture("images/Cowboys_Office.jpeg")
            else:
                self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")

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

        elif self.top > WINDOW_HEIGHT - 1:
            self.top = WINDOW_HEIGHT - 1


def main():
    window = FeedZeke()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()