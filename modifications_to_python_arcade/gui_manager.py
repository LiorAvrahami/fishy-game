import typing
from game_sprite_buttons.game_sprite_button_base_class import HideableGuiElement


class ModifiedUIManager:
    ui_elements : typing.List[HideableGuiElement]

    def __init__(self,window):
        self.window = window
        self.ui_elements = []

    def add_ui_element(self,v):
        self.ui_elements.append(v)

    def on_draw(self):
        for e in self.ui_elements:
            if e.is_visible == True:
                e.draw()

    def transform_xy_to_game_coordinates(self, x, y):
        # apply x,y transformation for stretched applications
        xv1, xv2, yv1, yv2 = self.window.get_viewport()  # load viewport rectangle
        return xv1 + (x / self.window.width) * (xv2 - xv1), yv1 + (y / self.window.height) * (yv2 - yv1)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_press()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.MOUSE_PRESS`
        """

        # apply x,y transformation for stretched applications
        x, y = self.transform_xy_to_game_coordinates(x, y)

        for e in self.ui_elements:
            if e.is_visible and e.collides_with_point((x,y)):
                e.on_press()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_release()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.MOUSE_RELEASE`
        """

        # apply x,y transformation for stretched applications
        x, y = self.transform_xy_to_game_coordinates(x, y)

        for e in self.ui_elements:
            if e.is_visible and e.collides_with_point((x,y)):
                e.on_release()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Dispatches :py:meth:`arcade.View.on_mouse_motion()` as :py:class:`arcade.gui.UIElement`
        with type :py:attr:`arcade.gui.MOUSE_MOTION`
        """

        # apply x,y transformation for stretched applications
        x, y = self.transform_xy_to_game_coordinates(x, y)

        for e in self.ui_elements:
            if e.is_visible and e.collides_with_point((x, y)):
                e.on_hover()
            else:
                e.on_unhover()
