import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def peak_plot(x):
    t = np.arange(len(x))
    plt.plot(t, np.abs(np.max(x) - x), color="blue")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()

# def flipud(x):
#     return np.abs(np.max(x) - x)

# replaces invalid values with the mean of the valid values
def flipud(x):
    x = np.array(x, dtype=float)  # Convert to float if not already
    valid_values = x[~np.isnan(x)]  # Get valid (non-NaN) values
    mean_valid = np.mean(valid_values)  # Compute the mean of valid values
    x[np.isnan(x)] = mean_valid  # Replace NaN values with the mean
    return np.abs(np.max(x) - x)



def plot_ppg(x, plot_inverted=False, color="blue", title="PPG signal"):
    t = np.arange(len(x))
    if not plot_inverted:
        x = flipud(x)
    plt.plot(t, x, color=color)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.show()

def get_measurement(df, mid):
    measurement = df.loc[mid]
    x = np.array(measurement.iloc[6:])  # extract signal
    x = np.nan_to_num(x, nan=np.nanmean(x))  # replace NaNs with mean value
    return {"id": measurement["id"], "date": measurement["date"],
            "device": measurement["device"], "sys": measurement["sys"],
            "dia": measurement["dia"], "hr": measurement["hr"], "x": x}

def plot_measurement(df, mid):
    m = get_measurement(df, mid)
    plot_ppg(m["x"], title=f"PPG signal of MID: {mid}, PID: {m['id']}, Date: {m['date']}, Device: {m['device']}")

def get_time_of_frame(frame_number):
    n_frames = 11
    times = []
    for j in range(n_frames):
        start = j * 50 + 1
        times.append(f"{start}:{start + 99}")
    return times[frame_number]

def get_x_from_frames(frames_list):
    x = []
    for i in range(len(frames_list)):
        if i % 2 == 1:
            x.extend(frames_list[i])
    return x

def main():
    # Read the data
    df = pd.read_csv("./data/df-ac-measurements.csv")
    print(df.tail(30))

    # Plot peaks
    df_mat = df.values
    peak_plot(df_mat[7, 6:606])
    peak_plot(df_mat[24, 6:606])
    peak_plot(df_mat[23, 6:606])

    # Plot a specific measurement
    mid = 35
    plot_measurement(df, mid)

    # Process frames
    m = get_measurement(df, mid)
    x = m["x"]
    l_frame = 100  # time span = l_frame/10 sec, since we have 10 samples/sec
    n = len(x)
    q = n // l_frame
    x = x[:q * 100]  # drop the reminder dividing with 500

    frames_list = [x[j*50:j*50 + 100] for j in range((q - 1) * 2 + 1)]
    n_of_frames = len(frames_list)
    is_signal = np.zeros((1, n_of_frames))
    is_signal[0, [0, 1, 5, 7]] = [0.5, 0.5, 0.1, 0.5]

    threshold = 0.4
    parts = np.where(is_signal > threshold)[1]

    plot_measurement(df, mid)

    # color frames
    plot_color = 'red'
    for part in parts:

        part = str(part)  # Convert to string explicitly
        if ':' not in part:
            continue  # Skip if ':' is not present


        b1, b2 = part.split(":")
        b1, b2 = int(b1), int(b2)
        plt.axvline(x=b1, linestyle="--", color=plot_color)
        plt.axvline(x=b2, linestyle="--", color=plot_color)
        heights = np.linspace(np.min(flipud(x)), np.max(flipud(x)), num=100)
        for h in heights:
            plt.plot([b1, b2], [h, h], linestyle=":", color=plot_color)

    # color peak
    part = '264:291'
    plot_color = 'green'
    b1, b2 = part.split(":")
    b1, b2 = int(b1), int(b2)
    plt.axvline(x=b1, linestyle="--", color=plot_color)
    plt.axvline(x=b2, linestyle="--", color=plot_color)
    heights = np.linspace(np.min(flipud(x)), np.max(flipud(x)), num=100)
    for h in heights:
        plt.plot([b1, b2], [h, h], linestyle=":", color=plot_color)

    plt.show()

if __name__ == "__main__":
    main()
