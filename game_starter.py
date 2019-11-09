import arcade


# Define constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Introduction"
GAME_SPEED = 1/60

MATTHEWSCALING = 0.25
TILE_SCALING = 0.05

JUMPSPEED = 3
MOVESPEED = 5

class YourGameClassRenameThis(arcade.Window):
    def __init__(self):
        """ Initialize variables """
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.center_x = WINDOW_WIDTH/2
        self.center_y = WINDOW_HEIGHT/2
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.background = None

    def setup(self):
        """ Setup the game (or reset the game) """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")

        self.player_sprite = arcade.Sprite("images/ada.png", MATTHEWSCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 280
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images/potato.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT,
                                      self.background)

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = JUMPSPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -JUMPSPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = MOVESPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -MOVESPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0



def main():
    window = YourGameClassRenameThis()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
