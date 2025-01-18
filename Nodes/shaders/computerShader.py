import moderngl


class ComputeShader:
    @staticmethod
    def create_compute_shader(ctx: moderngl.Context, compute_shader_path: str) -> moderngl.ComputeShader:
        with open(compute_shader_path) as f:
            return ctx.compute_shader(f.read())

    def __init__(self, computer_shader_path: str) -> None:
        self.ctx = moderngl.create_context(require=430)

        self.path = computer_shader_path
        self.program = ComputeShader.create_compute_shader(self.ctx, self.path)

    def dispatch(self, x: int, y: int, z: int) -> None:
        self.program.run(x, y, z)
