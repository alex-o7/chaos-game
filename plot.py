import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from chaos import generate_attractor

TAIL = 20

# precompute tail colors: index 0 = newest (red), index 19 = oldest (dark grey)
TAIL_COLORS = np.zeros((TAIL, 4))
TAIL_COLORS[:, 0] = np.linspace(1.0, 0.66, TAIL)   # R
TAIL_COLORS[:, 1] = np.linspace(0.0, 0.66, TAIL)   # G
TAIL_COLORS[:, 2] = np.linspace(0.0, 0.66, TAIL)   # B
TAIL_COLORS[:, 3] = 1.0                              # alpha

def plot_points(seed=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-0.9, 0.9)
    ax.set_ylim(-0.7, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')
    fig.patch.set_facecolor('white')

    pts = generate_attractor(n=1_000, seed=seed)

    sc_old = ax.scatter([], [], s=15, alpha=0.6, color='#a8a8a8')
    sc_hot = ax.scatter([], [], s=20, alpha=0.9, color='red')

    ax_slider = fig.add_axes([0.15, 0.10, 0.55, 0.03])
    slider = Slider(ax_slider, label='n', valmin=1, valmax=1000, valinit=1, valstep=1)

    ax_speed = fig.add_axes([0.15, 0.05, 0.55, 0.03])
    slider_speed = Slider(ax_speed, label='speed', valmin=1, valmax=100, valinit=50, valstep=1)

    ax_reset = fig.add_axes([0.75, 0.09, 0.11, 0.04])
    btn_reset = Button(ax_reset, label='reset')

    ax_seed = fig.add_axes([0.75, 0.04, 0.11, 0.04])
    btn_seed = Button(ax_seed, label='new seed')

    ax_play = fig.add_axes([0.87, 0.09, 0.11, 0.04])
    btn_play = Button(ax_play, label='play')

    playing = [False]
    timer = fig.canvas.new_timer(interval=50)

    def update_canvas(val):
        n = int(slider.val)
        tail_start = max(0, n - TAIL)

        sc_old.set_offsets(pts[:tail_start])

        tail_pts = pts[tail_start:n]
        tail_len = len(tail_pts)
        colors = TAIL_COLORS[TAIL - tail_len:]
        sc_hot.set_offsets(tail_pts[::-1])
        sc_hot.set_color(colors)

        fig.canvas.draw_idle()

    def update_speed(val):
        interval = int(205 - 2 * val)
        timer.interval = interval
        if playing[0]:
            timer.stop()
            timer.start()

    def advance(event=None):
        n = int(slider.val)
        if n < 1000:
            slider.set_val(n + 1)
        else:
            slider.set_val(1)

    def toggle_play(event):
        if playing[0]:
            timer.stop()
            playing[0] = False
            btn_play.label.set_text('play')
        else:
            timer.start()
            playing[0] = True
            btn_play.label.set_text('pause')
        fig.canvas.draw_idle()

    def reset_canvas(event):
        if playing[0]:
            timer.stop()
            playing[0] = False
            btn_play.label.set_text('play')
        slider.set_val(1)

    def new_seed(event):
        nonlocal pts
        if playing[0]:
            timer.stop()
            playing[0] = False
            btn_play.label.set_text('play')
        pts = generate_attractor(n=1_000, seed=np.random.randint(0, 10_000))
        slider.set_val(1)

    timer.add_callback(advance)

    slider.on_changed(update_canvas)
    slider_speed.on_changed(update_speed)
    btn_reset.on_clicked(reset_canvas)
    btn_seed.on_clicked(new_seed)
    btn_play.on_clicked(toggle_play)

    update_canvas(1)
    plt.show()

if __name__ == "__main__":
    plot_points()