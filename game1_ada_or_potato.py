import arcade

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Ada or Potato"
GAME_SPEED = 1/60
TIMER_MAXIMUM = 100

IMAGE_ADA = arcade.load_texture("images/ada.png")
IMAGE_POTATO = arcade.load_texture("images/potato.png", scale = .2)

SCORE = 0
class AdaOrPotato(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.logo_list = None
        self.score = 0

    def setup(self):
        arcade.set_background_color(BACKGROUND_COLOR)
        self.score = 0
        self.logo_list = arcade.SpriteList()
        self.logo_list.append(ChangingLogo())

    def on_draw(self):
        arcade.start_render()
        self.logo_list.draw()
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

    def on_update(self, delta_time: float):
        self.logo_list.update()

    def on_mouse_press(self, x, y, button, modifiers):
        for logo in self.logo_list:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.score += logo.get_current_value()

class ChangingLogo(arcade.Sprite):
    phase: str
    timer: int

    def __init__(self):
        super().__init__()
        self.phase = 'waiting'
        self.timer = 0
        self.center_x = WINDOW_WIDTH/2
        self.center_y = WINDOW_HEIGHT/2
        self.texture = IMAGE_ADA

    def update(self):
        self.timer += 1
        if self.timer > TIMER_MAXIMUM:
            self.timer = 0
            self.switch_image()

    def switch_image(self):
        if self.texture == IMAGE_POTATO:
            self.texture = IMAGE_ADA
        else:
            self.texture = IMAGE_POTATO

    def get_current_value(self):
        if self.texture == IMAGE_ADA:
            return 1
        else:
            return -1

def main():
    window = AdaOrPotato()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
