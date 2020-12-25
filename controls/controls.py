import typing
import arcade.key


class PlayerControlsObject():
    change_player_direction:typing.Callable
    reset_game:typing.Callable
    pause_game:typing.Callable

    up_pressed:bool
    down_pressed:bool
    left_pressed:bool
    right_pressed:bool

    most_recent_pressed = None

    def __init__(self,change_player_direction:typing.Callable,reset_game:typing.Callable,pause_game:typing.Callable,b_keyboard=True,b_mouse=True,b_controller=False):
        self.change_player_direction = change_player_direction
        self.reset_game = reset_game
        self.pause_game = pause_game
        self.reset_state()

    def reset_state(self):
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.most_recent_pressed = None


    def update_direction_based_on_keyboard(self):
        y_vel = 0
        x_vel = 0
        if self.up_pressed and not self.down_pressed:
            y_vel = 1
        if (not self.up_pressed) and self.down_pressed:
            y_vel = -1
        if self.up_pressed and self.down_pressed:
            if self.most_recent_pressed == arcade.key.UP:
                y_vel = 1
            if self.most_recent_pressed == arcade.key.DOWN:
                y_vel = -1
        if self.left_pressed and not self.right_pressed:
            x_vel = -1
        if (not self.left_pressed) and self.right_pressed:
            x_vel = 1
        if self.left_pressed and self.right_pressed:
            if self.most_recent_pressed == arcade.key.LEFT:
                x_vel = -1
            if self.most_recent_pressed == arcade.key.RIGHT:
                x_vel = 1
        self.change_player_direction((x_vel,y_vel))

    def on_keyboard_press(self,key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.R or key == arcade.key.BACKSPACE:
            self.reset_game()
            self.__init__(self.change_player_direction,self.reset_game,self.pause_game)
        elif key == arcade.key.SPACE:
            self.pause_game()
        self.most_recent_pressed = key
        self.update_direction_based_on_keyboard()

    def on_keyboard_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.update_direction_based_on_keyboard()

