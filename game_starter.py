import arcade


# Define constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Feed Zeke"
GAME_SPEED = 1/60

MATTHEWSCALING = 0.2
TILE_SCALING = 0.4
FOOTBALL_SCALING = 0.05

JUMPSPEED = 30
MOVESPEED = 5
GRAVITY = 1

class YourGameClassRenameThis(arcade.Window):
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


    def setup(self):
        """ Setup the game (or reset the game) """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.football_list = arcade.SpriteList()
        self.background = arcade.load_texture("images/Cowboys_Stadium.jpeg")
        self.score = 0

        self.player_sprite = arcade.Sprite("images/Zeke_Right.png", MATTHEWSCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150
        self.player_list.append(self.player_sprite)

        map_name = "map.tmx"
        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'Football'

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        self.football_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Called when it is time to draw the world """
        arcade.start_render()
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT,
                                      self.background)
        self.wall_list.draw()
        self.football_list.draw()
        self.player_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

    def on_update(self, delta_time):
        """ Called every frame of the game (1/GAME_SPEED times per second)"""
        self.physics_engine.update()

        football_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.football_list)

        for football in football_hit_list:
            football.remove_from_sprite_lists()
            self.score += 1


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



def main():
    window = YourGameClassRenameThis()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
