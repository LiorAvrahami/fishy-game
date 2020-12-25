from arcade import Window

class ResizeableWindow(Window):
    def __init__(self,*args,stretch_game_with_window:bool=False,**kwargs):
        self.stretch_game_with_window = stretch_game_with_window
        super().__init__(*args,**kwargs)

    def on_resize(self, width: float, height: float):
        """
        Override this function to add custom code to be called any time the window
        is resized. The only responsibility here is to update the viewport.

        :param float width: New width
        :param float height: New height
        """
        try:
            original_viewport = self.get_viewport()
        except Exception as ex:
            print("Error getting viewport:", ex)
            return

        # unscaled_viewport = self.get_viewport_size()
        # scaling = unscaled_viewport[0] / width

        if not self.stretch_game_with_window:
            self.set_viewport(original_viewport[0],
                              original_viewport[0] + width,
                              original_viewport[2],
                              original_viewport[2] + height)
        else:
            self.set_viewport(*original_viewport)