import arcade
import random

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Ada or Potato"
GAME_SPEED = 1/60
TIMER_MAXIMUM = 100

NEXT_PHASE = {
    'spinning forward': 'waiting',
    'waiting': 'spinning backward',
    'spinning backward': 'waiting again',
    'waiting again': 'spinning forward'
    }

IMAGE_ADA = arcade.load_texture("images/ada.png")
IMAGE_POTATO = arcade.load_texture("images/potato.png")

class AdaOrPotato(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE)
        self.logo_list = None

    def setup(self):
        arcade.set_background_color(BACKGROUND_COLOR)
        self.logo_list = arcade.SpriteList()
        self.logo_list.append(ChangingLogo())
        potato = ChangingLogo()
        potato.phase = 'spinning backward'
        potato.center_x = 50
        potato.center_y = 50
        self.logo_list.append(potato)

    def on_draw(self):
        arcade.start_render()
        self.logo_list.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for logo in self.logo_list:
            logo.switch_image()

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

    def update_timer(self):
        if self.timer < TIMER_MAXIMUM:
                self.timer += 1
        else:
            self.timer = 0
            self.phase = NEXT_PHASE[self.phase]

    def update_angle(self):
        progress = self.timer / TIMER_MAXIMUM
        if self.phase == 'spinning forward':
            self.angle = 360 * progress
        elif self.phase == 'spinning backward':
            self.angle = 360 * (1 - progress)
        else:
            self.angle = random.randint(0, 360)

    def update(self):
        self.update_timer()
        self.update_angle()

    def switch_image(self):
        if self.texture == IMAGE_POTATO:
            self.texture = IMAGE_ADA
        else:
            self.texture = IMAGE_POTATO

def main():
    window = AdaOrPotato()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
