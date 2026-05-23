import math
import os
import random

from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Pipe(Widget):
    width_size = NumericProperty(60)
    gap_size = NumericProperty(150)
    gap_y = NumericProperty(300)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.passed = False
        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas,
            gap_y=self.update_canvas,
            gap_size=self.update_canvas,
            width_size=self.update_canvas,
        )

    def configure(self, width_size, gap_size, gap_y, world_height):
        self.width_size = width_size
        self.gap_size = gap_size
        self.gap_y = gap_y
        self.size = (width_size, world_height)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            outer_color = (0.55, 0.35, 0.15, 1)
            band_color = (0.40, 0.25, 0.10, 1)
            edge_color = (0.25, 0.15, 0.06, 1)

            x = self.x
            w = self.width_size
            world_height = self.height or (self.parent.height if self.parent else 640)

            bottom_h = max(0, self.gap_y - self.gap_size / 2)
            top_pipe_y = self.gap_y + self.gap_size / 2
            top_h = max(0, world_height - top_pipe_y)

            Color(*outer_color)
            Rectangle(pos=(x, 0), size=(w, bottom_h))
            Rectangle(pos=(x, top_pipe_y), size=(w, top_h))

            band_h = max(10, min(22, w // 3))
            Color(*band_color)
            for i in range(3):
                by = 20 + i * (band_h + 6)
                if by + band_h <= bottom_h:
                    Rectangle(pos=(x, by), size=(w, band_h))

            for i in range(3):
                ty = top_pipe_y + 20 + i * (band_h + 6)
                if ty + band_h <= top_pipe_y + top_h:
                    Rectangle(pos=(x, ty), size=(w, band_h))

            cap_r = w / 2
            Color(*edge_color)
            Ellipse(pos=(x, -cap_r), size=(w, w))
            Ellipse(pos=(x, bottom_h - cap_r), size=(w, w))
            Ellipse(pos=(x, top_pipe_y - cap_r), size=(w, w))
            Ellipse(pos=(x, top_pipe_y + top_h - cap_r), size=(w, w))

            Color(0, 0, 0, 0.35)
            Line(rectangle=(x, 0, w, bottom_h), width=1.2)
            Line(rectangle=(x, top_pipe_y, w, top_h), width=1.2)

    def move(self, speed):
        self.x -= speed


class Bird(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    size_radius = NumericProperty(20)
    flap_state = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            pos=self.update_canvas,
            size=self.update_canvas,
            flap_state=self.update_canvas,
            size_radius=self._sync_size,
        )
        self._sync_size()

    def _sync_size(self, *args):
        r = self.size_radius
        self.size = (r * 3.2, r * 2.2)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            x, y = self.pos
            r = self.size_radius

            Color(1, 0.85, 0, 1)
            Ellipse(pos=(x, y), size=(r * 2.5, r * 2))

            Color(0.2, 0.1, 0, 1)
            Line(ellipse=(x, y, r * 2.5, r * 2), width=1.5)

            Color(1, 1, 1, 1)
            eye_size = r * 0.7
            Ellipse(pos=(x + r * 1.5, y + r * 1.1), size=(eye_size, eye_size))
            Color(0, 0, 0, 1)
            Ellipse(pos=(x + r * 1.8, y + r * 1.3), size=(eye_size * 0.4, eye_size * 0.4))

            Color(1, 0.4, 0, 1)
            beak_points = [
                x + r * 2.3, y + r * 1.1,
                x + r * 3.1, y + r * 0.8,
                x + r * 2.3, y + r * 0.5,
            ]
            Triangle(points=beak_points)
            Color(0.2, 0.1, 0, 1)
            Line(points=beak_points + [beak_points[0], beak_points[1]], width=1.2)

            Color(1, 1, 1, 0.8)
            wing_y_offset = (r * 0.4) * self.flap_state
            wing_pos = (x + r * 0.2, y + r * 0.6 + wing_y_offset)
            Ellipse(pos=wing_pos, size=(r * 1.2, r * 0.8))
            Color(0.2, 0.1, 0, 0.5)
            Line(ellipse=(wing_pos[0], wing_pos[1], r * 1.2, r * 0.8), width=1)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        self.flap_state = math.sin(Clock.get_time() * 15)


class GameWorld(Widget):
    bird = ObjectProperty(None)
    score = NumericProperty(0)

    REFERENCE_WIDTH = 360
    REFERENCE_HEIGHT = 640

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pipes = []
        self.game_over = False
        self.layout_ready = False

        self.scale = 1.0
        self.ground_height = 60
        self.pipe_speed = 4
        self.gravity = 0.35
        self.flap_velocity = 7
        self.pipe_width = 60
        self.pipe_gap = 150
        self.pipe_spawn_interval = 1.8
        self.bird_start_x = 100
        self.bird_start_y = 300

        base_path = os.path.dirname(os.path.abspath(__file__))

        def load_sound(*filenames):
            for filename in filenames:
                path = os.path.join(base_path, filename)
                sound = SoundLoader.load(path)
                if sound is not None:
                    return sound
            print(f"Warning: Could not load sound file(s) {filenames}")
            return None

        self.sound_flap = load_sound('flap.wav', 'flav.wav')
        self.sound_score = load_sound('score.wav')
        self.sound_hit = load_sound('hit.wav')

        self._score_label = Label(
            text="0",
            font_size='28sp',
            color=(0, 0, 0, 1),
            bold=True,
            size_hint=(None, None),
            size=(120, 40),
        )
        self._gameover_label = Label(
            text="GAME OVER",
            font_size='30sp',
            color=(0.1, 0.05, 0.0, 1),
            bold=True,
            opacity=0,
        )
        self._restart_hint = Label(
            text="Tap to restart",
            font_size='16sp',
            color=(0.1, 0.05, 0.0, 1),
            opacity=0,
        )

        self.bird = Bird()
        self.add_widget(self.bird)
        self.add_widget(self._score_label)
        self.add_widget(self._gameover_label)
        self.add_widget(self._restart_hint)

        self.bind(size=self._on_size, pos=self._on_size, score=self.update_score_canvas)
        self._on_size()

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)

        if self.game_over:
            self.reset_game()
            return True

        self.bird.velocity_y = self.flap_velocity
        if self.sound_flap:
            self.sound_flap.play()
        return True

    def _scaled(self, value):
        return value * self.scale

    def _sync_metrics(self):
        if not self.width or not self.height:
            return

        self.scale = max(
            0.85,
            min(self.width / self.REFERENCE_WIDTH, self.height / self.REFERENCE_HEIGHT),
        )
        self.ground_height = max(48, self._scaled(60))
        self.pipe_speed = self._scaled(4)
        self.gravity = self._scaled(0.35)
        self.flap_velocity = self._scaled(7)
        self.pipe_width = self._scaled(60)
        self.pipe_gap = min(self.height * 0.34, max(self._scaled(150), 140))
        self.pipe_spawn_interval = 1.8
        self.bird_start_x = self.width * 0.28
        self.bird_start_y = self.ground_height + (self.height - self.ground_height) * 0.48

        self.bird.size_radius = self._scaled(20)
        self._score_label.font_size = f"{int(self._scaled(28))}sp"
        self._gameover_label.font_size = f"{int(self._scaled(30))}sp"
        self._restart_hint.font_size = f"{int(self._scaled(16))}sp"

        for pipe in self.pipes:
            pipe.size = (pipe.width_size, self.height)
            pipe.update_canvas()

    def _draw_background(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.60, 0.85, 1.00, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.95, 0.85, 0.55, 1)
            Rectangle(pos=(self.x, self.y), size=(self.width, self.ground_height))

            Color(0.30, 0.20, 0.10, 0.20)
            Line(
                points=[
                    self.x,
                    self.y + self.ground_height,
                    self.x + self.width,
                    self.y + self.ground_height,
                ],
                width=max(1.5, self._scaled(2)),
            )

            Color(1, 1, 1, 0.75)
            cloud_specs = [
                (0.20, 0.74, 0.06),
                (0.52, 0.82, 0.07),
                (0.82, 0.74, 0.055),
            ]
            for x_factor, y_factor, radius_factor in cloud_specs:
                radius = min(self.width, self.height) * radius_factor
                cx = self.x + self.width * x_factor
                cy = self.y + self.height * y_factor
                Ellipse(pos=(cx - radius, cy - radius), size=(radius * 2, radius * 2))

    def _layout_labels(self):
        self._score_label.size = (self.width, self._scaled(44))
        self._score_label.pos = (0, self.height - self._scaled(56))

        self._gameover_label.size = (self.width, self._scaled(40))
        self._gameover_label.pos = (0, self.height / 2 - self._scaled(18))

        self._restart_hint.size = (self.width, self._scaled(30))
        self._restart_hint.pos = (0, self.height / 2 - self._scaled(52))

    def _position_bird(self):
        self.bird.pos = (self.bird_start_x, self.bird_start_y)
        self.bird.velocity = (0, 0)

    def _on_size(self, *args):
        self._sync_metrics()
        self._draw_background()
        self._layout_labels()

        if not self.layout_ready:
            self._position_bird()
            self.layout_ready = True

    def update_score_canvas(self, *args):
        self._score_label.text = str(self.score)
        self._gameover_label.opacity = 1 if self.game_over else 0
        self._restart_hint.opacity = 1 if self.game_over else 0

    def spawn_pipe(self, *args):
        if self.game_over or not self.width or not self.height:
            return

        play_height = self.height - self.ground_height
        gap_margin = max(self._scaled(70), self.bird.size_radius * 3)
        min_gap_center = self.ground_height + self.pipe_gap / 2 + gap_margin
        max_gap_center = self.ground_height + play_height - self.pipe_gap / 2 - gap_margin
        if min_gap_center >= max_gap_center:
            gap_y = self.height / 2
        else:
            gap_y = random.uniform(min_gap_center, max_gap_center)

        new_pipe = Pipe(pos=(self.width, 0))
        new_pipe.configure(self.pipe_width, self.pipe_gap, gap_y, self.height)
        self.add_widget(new_pipe)
        self.pipes.append(new_pipe)

    def update(self, dt):
        if self.game_over or not self.layout_ready:
            return

        self.bird.velocity_y -= self.gravity
        self.bird.move()

        if self.bird.y <= self.ground_height or self.bird.top >= self.height:
            self.end_game()
            return

        pipes_to_remove = []
        bird_center_x = self.bird.x + self.bird.size_radius
        bird_center_y = self.bird.y + self.bird.size_radius
        collision_radius = max(8, self.bird.size_radius - self._scaled(5))

        for pipe in self.pipes:
            pipe.move(self.pipe_speed)

            if (
                pipe.x < bird_center_x + collision_radius
                and pipe.x + pipe.width_size > bird_center_x - collision_radius
            ):
                lower_limit = pipe.gap_y - pipe.gap_size / 2
                upper_limit = pipe.gap_y + pipe.gap_size / 2
                if (
                    bird_center_y - self.bird.size_radius < lower_limit
                    or bird_center_y + self.bird.size_radius > upper_limit
                ):
                    self.end_game()
                    return

            if not pipe.passed and pipe.x + pipe.width_size < self.bird.x:
                pipe.passed = True
                self.score += 1
                if self.sound_score:
                    self.sound_score.play()

            if pipe.x < -pipe.width_size:
                pipes_to_remove.append(pipe)

        for pipe in pipes_to_remove:
            self.remove_widget(pipe)
            self.pipes.remove(pipe)

    def end_game(self):
        if self.game_over:
            return
        self.game_over = True
        if self.sound_hit:
            self.sound_hit.play()
        self.update_score_canvas()

    def reset_game(self):
        for pipe in self.pipes:
            self.remove_widget(pipe)
        self.pipes.clear()

        self._sync_metrics()
        self._position_bird()
        self.score = 0
        self.game_over = False
        self.update_score_canvas()
