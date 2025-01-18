import numpy as np
import moderngl
import pygame as pg


class ScreenRect:
    @staticmethod
    def pygame_rect_to_screen_rect(rect: pg.Rect, size: tuple | pg.Vector2) -> pg.Rect:
        w, h = size
        return pg.Rect(((rect.x * 2) - w) + rect.w, ((rect.y * 2) + h) - rect.h, rect.w, rect.h)

    def build(self, win_size: pg.Vector2):
        offset = self._offset = self._offset.elementwise() / win_size
        self.current_w, self.current_h = win_size
        x, y = self.size.elementwise() / win_size

        self.vertices = [
            (-x + offset[0], y + offset[1]),
            (x + offset[0], y + offset[1]),
            (-x + offset[0], -y + offset[1]),

            (-x + offset[0], -y + offset[1]),
            (x + offset[0], y + offset[1]),
            (x + offset[0], -y + offset[1]),
        ]

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.data = np.hstack([self.vertices, self.tex_coords])

        self.vertex_count = 6

        self.vbo = self._ctx.buffer(self.data)

        try:
            self.vao = self._ctx.vertex_array(self.program, [
                (self.vbo, '2f 2f', 'vertexPos', 'vertexTexCoord'),
            ])
        except moderngl.Error:
            self.vbo = self._ctx.buffer(self.vertices)
            self.vao = self._ctx.vertex_array(self.program, [
                (self.vbo, '2f', 'vertexPos'),
            ])

    def __init__(self, size, win_size, offset, ctx, program):
        self.size = pg.Vector2(size)
        self._offset = pg.Vector2(offset)
        self._ctx = ctx
        self.program = program

        self.vbo = None
        self.vao = None

        self.tex_coords = [
            (0.0, 1.0),
            (1.0, 1.0),
            (0.0, 0.0),

            (0.0, 0.0),
            (1.0, 1.0),
            (1.0, 0.0),
        ]

        self.vertices = np.array([], dtype=np.float32)
        self.tex_coords = np.array(self.tex_coords, dtype=np.float32)
        self.data = np.array([], dtype=np.float32)

        self.vertex_count = 6

        self.build(pg.Vector2(win_size))
