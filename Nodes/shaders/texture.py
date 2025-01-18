import os
import typing

import pygame as pg
import moderngl

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Texture:
    def __init__(self, image: pg.Surface, ctx: moderngl.Context):
        image = pg.transform.flip(image, False, True)
        self.image_width, self.image_height = image.get_size()
        img_data = pg.image.tostring(image, "RGBA")
        self.texture = ctx.texture(size=image.get_size(), components=4, data=img_data)
        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

    def update(self, image: pg.Surface):
        image = pg.transform.flip(image, False, True)
        img_data = pg.image.tostring(image, "RGBA")

        self.texture.write(img_data)

    def as_surface(self) -> pg.Surface:
        buffer = self.texture.read()
        surf = pg.image.frombuffer(buffer, (self.image_width, self.image_height), "RGBA")
        return surf

    def bind(self, unit: int, read: bool = True, write: bool = True) -> None:
        self.texture.bind_to_image(unit, read=read, write=write)

    def use(self, _id: typing.Union[None, int] = None) -> None:
        if not _id:
            self.texture.use()
        else:
            self.texture.use(_id)
