import arcade

class maingame(arcade.Window):
    def __init__(self):
        super.__init__()

def main():
    window = maingame()
    window.setup()
    arcade.run()

# Run the main() function
if __name__ == '__main__':
    main()