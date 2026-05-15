import sdl2
import sdl2.ext
import ctypes
import time
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
FRAME_TIME = 1.0 / FPS


class MotionTestSDL2:
    """PySDL2-based motion test to check for jitter."""

    def __init__(self):
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)

        # Create window with VSYNC flag
        self.window = sdl2.SDL_CreateWindow(
            b"PySDL2 Motion Test",
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            sdl2.SDL_WINDOW_SHOWN,
        )

        # Create renderer with VSYNC
        self.renderer = sdl2.SDL_CreateRenderer(
            self.window,
            -1,
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC,
        )

        # Movement properties
        self.x = 0.0
        self.x_prev = 0.0
        self.speed = 180  # Pixels per second

        # Timing
        self.last_update_time = time.perf_counter()
        self.running = True

    def handle_events(self):
        """Handle input events."""
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                self.running = False
            elif event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    self.running = False

    def update(self, delta_time: float):
        """Update game logic at fixed timestep."""
        self.x_prev = self.x
        self.x += self.speed * FRAME_TIME

        if self.x > SCREEN_WIDTH:
            self.x = 0.0
            self.x_prev = 0.0

        self.last_update_time = time.perf_counter()

    def render(self):
        """Render with interpolation."""
        # Calculate interpolation
        current_time = time.perf_counter()
        time_elapsed = current_time - self.last_update_time
        interpolation = min(time_elapsed / FRAME_TIME, 1.0)

        interpolated_x = self.x_prev + (self.x - self.x_prev) * interpolation

        # Clear screen (black)
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(self.renderer)

        # Draw blue rectangle
        rect = sdl2.SDL_Rect(int(interpolated_x), 300, 70, 80)
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0, 0, 255, 255)
        sdl2.SDL_RenderFillRect(self.renderer, ctypes.byref(rect))

        # Present
        sdl2.SDL_RenderPresent(self.renderer)

    def run(self):
        """Main loop."""
        clock = sdl2.SDL_GetTicks()
        frame_time_ms = int(FRAME_TIME * 1000)

        while self.running:
            self.handle_events()

            # Simple frame timing using SDL_Delay
            now = sdl2.SDL_GetTicks()
            elapsed = now - clock

            if elapsed >= frame_time_ms:
                self.update(FRAME_TIME)
                self.render()
                clock = now
            else:
                # Sleep a bit to avoid busy waiting
                sdl2.SDL_Delay(1)

    def cleanup(self):
        """Clean up SDL resources."""
        if self.renderer:
            sdl2.SDL_DestroyRenderer(self.renderer)
        if self.window:
            sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()


def main():
    """Run the test."""
    test = MotionTestSDL2()
    try:
        test.run()
    finally:
        test.cleanup()
    sys.exit(0)


if __name__ == "__main__":
    main()
