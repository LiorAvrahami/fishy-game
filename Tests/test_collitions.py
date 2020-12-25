"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade
import fish
from controls import PlayerControlsObject
from fish_generator import FishGenerator

GL_NEAREST = 9728  # open_gl scaling filter key for nearest neighbor

SCREEN_TITLE = "Eat or Be eaten"


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    fish_sprites: arcade.SpriteList
    player_fish: fish.PlayerFish
    active_buttons_sprites: arcade.SpriteList
    controls_handler: PlayerControlsObject

    fish_generator: FishGenerator

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AZURE)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.fish_sprites = arcade.SpriteList()
        self.player_fish = fish.PlayerFish(self,[0, 50])
        self.fish_sprites.append(self.player_fish)
        self.fish_sprites.append(fish.ComputerFish(self,True,self.width/2,0,3,0))
        self.active_buttons_sprites = arcade.SpriteList()
        self.controls_handler = PlayerControlsObject(self.player_fish.change_movement_direction)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        self.fish_sprites.draw(filter=GL_NEAREST)
        self.player_fish.draw_hit_box()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.fish_sprites.on_update()
        print(self.player_fish.position)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        self.controls_handler.on_keyboard_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.controls_handler.on_keyboard_release(key, key_modifiers)


def main():
    """ Main method """
    game = MyGame(1600, 800, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
