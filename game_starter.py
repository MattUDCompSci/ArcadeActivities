import arcade


# Define constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Feed Zeke"
GAME_SPEED = 1/60

ZEKE_SCALING = 0.125
TILE_SCALING = 0.4
FOOTBALL_SCALING = 0.4
ZEKE_TACKLED = 0

ZEKERIGHT = arcade.load_texture("images/Zeke_Right.png", mirrored = False, scale = ZEKE_SCALING)
ZEKELEFT = arcade.load_texture("images/Zeke_Right.png", mirrored = True, scale = ZEKE_SCALING)

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
        self.football_list = None
        self.defender_list = None
        self.background = None
        self.score = None
        self.level = None
        self.jump = None
        self.tackled = None
        self.defender = None
        self.current_state = STARTSCREEN

        self.instructions = []
        texture = arcade.load_texture("images/Start Screen.jpg")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/potato.png")
        self.instructions.append(texture)

    def setup(self):
        """ Setup the game (or reset the game) """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.football_list = arcade.SpriteList()
        self.defender_list = arcade.SpriteList()
        self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")
        self.score = 0
        self.level = 1
        self.jump = 18
        self.tackled = False

        self.player_sprite = Zeke_Player()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        self.defender = Defender_Class()
        self.defender_list.append(self.defender)

        self.level_updater()

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
        self.wall_list.draw()
        self.football_list.draw()
        self.player_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 20)

        if self.level == 4:
            self.defender_list.draw()

    def on_draw(self):
        arcade.start_render()
        if self.current_state == STARTSCREEN:
            self.draw_instructions_page(0)

        elif self.current_state == CONTROLSSCREEN:
            self.draw_instructions_page(1)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.current_state == STARTSCREEN:
            self.current_state = CONTROLSSCREEN
        elif self.current_state == CONTROLSSCREEN:
            self.setup()
            self.current_state = GAME_RUNNING

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""
        self.player_list.update()
        if self.current_state == GAME_RUNNING:
            self.physics_engine.update()

            football_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.football_list)

            for football in football_hit_list:
                football.remove_from_sprite_lists()
                self.score += 10

            if self.player_sprite.top < 0:
                self.score -= 10

            if self.player_sprite.center_x >= WINDOW_WIDTH:
                self.level += 1
                self.jump += 1
                self.level_updater()
                self.player_sprite.center_x = 64
                self.player_sprite.center_y = self.player_sprite.center_y

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = self.jump
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVESPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVESPEED


    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def level_updater(self):
        if self.level < 13:
            map_name = f"map_level_{self.level}.tmx"
            platforms_layer_name = 'Platforms'
            footballs_layer_name = 'Football'

            my_map = arcade.tilemap.read_tmx(map_name)

            self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
            self.football_list = arcade.tilemap.process_layer(my_map, footballs_layer_name, FOOTBALL_SCALING)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

            if self.level%3 == 0:
                self.background = arcade.load_texture("images/Cowboys_Office.jpeg")
            else:
                self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")

class Zeke_Player(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.textures.append(ZEKELEFT)
        self.textures.append(ZEKERIGHT)
        self.set_texture(1)

    def update(self):

        if self.change_x > 0:
            self.set_texture(1)
        elif self.change_x < 0:
            self.set_texture(0)

        if self.left < 0:
            self.left = 0

        if self.top < 0:
            self.center_x = 64
            self.center_y = 150

        elif self.top > WINDOW_HEIGHT - 1:
            self.top = WINDOW_HEIGHT - 1

class Defender_Class(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.textures.append(ZEKELEFT)
        self.textures.append(ZEKERIGHT)
        self.set_texture(0)

    def update(self):
        if self.level == 4:
            self.set_texture(ZEKELEFT)
            self.center_x = 400
            self.center_y = 150
        elif self.level == 5:
            self.set_texture(ZEKERIGHT)

def main():
    window = FeedZeke()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()