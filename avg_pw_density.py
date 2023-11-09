import wave
import numpy as np
import os
import csv

def calculate_power_densities(audio_file, interval=30):
    # Load the WAV file
    with wave.open(audio_file, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        audio_data = wav_file.readframes(num_frames)

    # Convert binary data to a numpy array
    dtype = np.int16 if sample_width == 2 else np.int32
    audio_array = np.frombuffer(audio_data, dtype=dtype)

    # If stereo, take only one channel (mono)
    if num_channels == 2:
        audio_array = audio_array[::2]

    # Convert to floating-point values in the range [-1, 1]
    max_value = 2 ** (8 * sample_width - 1) - 1
    audio_array = audio_array.astype(np.float32) / max_value

    # Calculate the number of frames in the desired interval (30 seconds)
    interval_frames = int(interval * frame_rate)

    # Calculate the number of intervals in the audio data
    num_intervals = int(np.ceil(len(audio_array) / interval_frames))

    # Initialize lists to store average and peak power densities for each interval
    average_power_densities = []
    peak_power_densities = []

    # Calculate power densities for each interval
    for i in range(num_intervals):
        start_idx = i * interval_frames
        end_idx = (i + 1) * interval_frames
        audio_interval = audio_array[start_idx:end_idx]

        # Calculate power for each sample in the interval
        power = audio_interval ** 2

        # Calculate average power density for the interval
        average_power_density = np.sum(power) / len(power)

        # Calculate peak power density for the interval
        peak_power_density = np.max(power)

        average_power_densities.append(average_power_density)
        peak_power_densities.append(peak_power_density)

    return average_power_densities, peak_power_densities

def process_sound_samples(folder_path):
    audio_files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    results = []

    for audio_file in audio_files:
        file_path = os.path.join(folder_path, audio_file)
        avg_power, peak_power = calculate_power_densities(file_path)

        # Append the results for each file to the list
        results.append((audio_file, avg_power, peak_power))

    return results

def save_to_csv(results, output_csv_file):
    with open(output_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row to the CSV file
        csv_writer.writerow(['Audio File', 'Interval', 'Average Power Density', 'Peak Power Density'])

        # Write results for each audio file to the CSV file
        for file_result in results:
            audio_file, avg_power_list, peak_power_list = file_result
            for i, (avg_power, peak_power) in enumerate(zip(avg_power_list, peak_power_list)):
                interval = f"{i+1}"  # Interval number (starting from 1)
                csv_writer.writerow([audio_file, interval, avg_power, peak_power])

# Example usage
sound_samples_folder = 'path/to/your/sound_samples_folder'
output_csv_file = 'power_densities_results.csv'

results = process_sound_samples(sound_samples_folder)
save_to_csv(results, output_csv_file)
