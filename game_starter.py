import arcade


# Define constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Feed Zeke"
GAME_SPEED = 1/60

ZEKESCALING = 0.15
TILE_SCALING = 0.4
FOOTBALL_SCALING = 0.4

JUMPSPEED = 30
MOVESPEED = 5
GRAVITY = 1

STARTSCREEN = 0
CONTROLSSCREEN = 1
GAME_RUNNING = 2

'''class IntroductionScreens(arcade.Sprite):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.texture = STARTSCREEN

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.texture.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.texture == STARTSCREEN:
            self.texture == INTRODUCTIONSCREEN
        elif self.texture == INTRODUCTIONSCREEN:
            game = FeedZeke()'''

class FeedZeke(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.center_x = WINDOW_WIDTH/2
        self.center_y = WINDOW_HEIGHT/2
        self.player_list = None
        self.wall_list = None
        self.football_list = None
        self.background = None
        self.score = None
        self.level = None
        self.current_state = STARTSCREEN

        self.instructions = []
        texture = arcade.load_texture("images/ada.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/potato.png")
        self.instructions.append(texture)

    def setup(self):
        """ Setup the game (or reset the game) """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.football_list = arcade.SpriteList()
        self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")
        self.score = 0
        self.level = 1

        self.player_sprite = arcade.Sprite("images/Zeke_Right.png", ZEKESCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

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
        if self.current_state == GAME_RUNNING:
            self.physics_engine.update()

            football_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.football_list)

            for football in football_hit_list:
                football.remove_from_sprite_lists()
                self.score += 1

            if self.player_sprite.center_x >= WINDOW_WIDTH:
                self.level += 1
                self.level_updater()
                self.player_sprite.center_x = 64
                self.player_sprite.center_y = 150

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMPSPEED
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
        map_name = f"map_level_{self.level}.tmx"
        platforms_layer_name = 'Platforms'
        footballs_layer_name = 'Football'

        my_map = arcade.tilemap.read_tmx(map_name)

        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)
        self.football_list = arcade.tilemap.process_layer(my_map, footballs_layer_name, TILE_SCALING)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        if self.level%3 == 0:
            self.background = arcade.load_texture("images/Cowboys_Office.jpeg")
        else:
            self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")

def main():
    window = FeedZeke()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()