from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D
from engine.core_ext.collision.collision2D.buttons.BaseButton import BaseButton

class TextureButton(BaseButton):
    def __init__(self, hit_area_type: Hitarea2D):
        super().__init__(hit_area_type)