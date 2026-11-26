import matplotlib

matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import RadioButtons, TextBox


DT = 0.005
SIGNAL_NAMES = [
    "Sine Wave",
    "Cosine Wave",
    "Square Wave",
    "Triangular Wave",
    "Sawtooth Wave",
    "Exponential Decay",
    "Exponential Growth",
    "Damped Sine Wave",
]


def generate_signal(choice, time_values, amplitude, frequency):
    omega = 2 * np.pi * frequency

    if choice == 1:
        return amplitude * np.sin(omega * time_values)
    if choice == 2:
        return amplitude * np.cos(omega * time_values)
    if choice == 3:
        return amplitude * np.sign(np.sin(omega * time_values))
    if choice == 4:
        return (2 * amplitude / np.pi) * np.arcsin(
            np.sin(omega * time_values)
        )
    if choice == 5:
        return amplitude * (
            2 * (frequency * time_values - np.floor(frequency * time_values)) - 1
        )
    if choice == 6:
        return amplitude * np.exp(-2 * time_values)
    if choice == 7:
        return amplitude * np.exp(0.8 * time_values)
    if choice == 8:
        return (
            amplitude
            * np.exp(-2 * time_values)
            * np.sin(omega * time_values)
        )

    raise ValueError("Unknown signal choice")


def run():
    amplitude = 5.0
    frequency = 2.0
    duration = 2.0
    signal_choice = 1

    time_values = np.arange(0.0, duration, DT)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.subplots_adjust(left=0.10, right=0.75, bottom=0.18, top=0.88)
    fig.suptitle(
        "ANIMATED SIGNAL GENERATOR",
        fontsize=18,
        fontweight="bold",
        color="cyan",
    )

    ax.set_title("Live Signal Visualization")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3)

    y_values = generate_signal(
        signal_choice, time_values, amplitude, frequency
    )
    line, = ax.plot([], [], color="cyan", linewidth=2.5)
    ax.set_xlim(0, duration)
    maximum = max(np.max(np.abs(y_values)), 1)
    ax.set_ylim(-maximum * 1.2, maximum * 1.2)

    info_text = fig.text(
        0.77,
        0.75,
        "Signal: Sine Wave\nAmplitude: 5\n"
        "Frequency: 2 Hz\nDuration: 2 sec",
        fontsize=11,
        color="white",
        bbox=dict(
            facecolor="#182635",
            edgecolor="cyan",
            boxstyle="round,pad=0.6",
        ),
    )

    def animate(frame):
        line.set_data(time_values[:frame], y_values[:frame])
        return (line,)

    animation = FuncAnimation(
        fig,
        animate,
        frames=len(time_values),
        interval=10,
        blit=True,
        repeat=True,
    )

    ax_radio = plt.axes([0.78, 0.35, 0.19, 0.35])
    radio = RadioButtons(ax_radio, SIGNAL_NAMES, active=0)

    ax_amplitude = plt.axes([0.12, 0.07, 0.15, 0.05])
    amplitude_box = TextBox(ax_amplitude, "Amplitude", initial="5")
    ax_frequency = plt.axes([0.36, 0.07, 0.15, 0.05])
    frequency_box = TextBox(ax_frequency, "Frequency", initial="2")
    ax_duration = plt.axes([0.60, 0.07, 0.15, 0.05])
    duration_box = TextBox(ax_duration, "Duration", initial="2")

    def update_signal(label):
        nonlocal amplitude, frequency, duration, time_values, y_values
        nonlocal signal_choice

        try:
            new_amplitude = float(amplitude_box.text)
            new_frequency = float(frequency_box.text)
            new_duration = float(duration_box.text)

            if new_amplitude <= 0:
                raise ValueError("Amplitude must be positive")
            if new_frequency <= 0:
                raise ValueError("Frequency must be positive")
            if new_duration <= 0:
                raise ValueError("Duration must be positive")

            amplitude = new_amplitude
            frequency = new_frequency
            duration = new_duration
            signal_choice = SIGNAL_NAMES.index(label) + 1
            time_values = np.arange(0.0, duration, DT)
            y_values = generate_signal(
                signal_choice, time_values, amplitude, frequency
            )

            ax.set_xlim(0, duration)
            maximum = max(np.max(np.abs(y_values)), 1)
            ax.set_ylim(-maximum * 1.2, maximum * 1.2)
            info_text.set_text(
                f"Signal: {label}\nAmplitude: {amplitude:g}\n"
                f"Frequency: {frequency:g} Hz\nDuration: {duration:g} sec"
            )

            animation._frames = list(range(len(time_values)))
            fig.canvas.draw_idle()
        except ValueError as error:
            print(f"Invalid input: {error}")

    radio.on_clicked(update_signal)
    amplitude_box.on_submit(update_signal)
    frequency_box.on_submit(update_signal)
    duration_box.on_submit(update_signal)

    plt.show()


if __name__ == "__main__":
    run()
