import arcade
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Movement Test"
FPS = 60
FRAME_TIME = 1.0 / FPS


class MotionTestWindow(arcade.Window):
    """Test window to verify smooth motion without jitter using Arcade."""

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE,
            resizable=False,
            vsync=True,
            fullscreen=True,
        )

        # Movement properties
        self.x = 0.0
        self.x_prev = 0.0  # Previous frame position for interpolation
        self.speed = 180  # Pixels per second

        # Time tracking for interpolation
        self.last_update_time = time.perf_counter()

        # Set fixed update rate
        self.set_update_rate(FRAME_TIME)

        # Background color
        self.background_color = arcade.color.BLACK

    def on_update(self, delta_time: float) -> None:
        """
        Update game logic at fixed timestep.

        Store previous position for interpolation during render.
        """
        # Store previous position for interpolation
        self.x_prev = self.x

        # Move based on fixed timestep
        self.x += self.speed * FRAME_TIME

        # Reset position when it goes off screen
        if self.x > SCREEN_WIDTH:
            self.x = 0.0
            self.x_prev = 0.0

        # Update the timestamp
        self.last_update_time = time.perf_counter()

    def on_draw(self) -> None:
        """
        Render the game with frame interpolation.

        Interpolate between previous and current position to eliminate jitter
        caused by timing variations between update and draw calls.
        """
        # Arcade automatically clears the screen and handles double buffering
        self.clear()

        # Calculate time since last update
        current_time = time.perf_counter()
        time_elapsed = current_time - self.last_update_time

        # Calculate interpolation factor (0.0 to 1.0)
        interpolation = min(time_elapsed / FRAME_TIME, 1.0)

        # Interpolate position between previous and current
        interpolated_x = self.x_prev + (self.x - self.x_prev) * interpolation

        # Draw a blue rectangle at interpolated position
        arcade.draw_lrbt_rectangle_filled(
            left=interpolated_x,
            right=interpolated_x + 70,
            bottom=300,
            top=300 + 80,
            color=arcade.color.BLUE,
        )


def main():
    """Run the motion test."""
    window = MotionTestWindow()
    arcade.run()


if __name__ == "__main__":
    main()
