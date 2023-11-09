import wave
import numpy as np

def calculate_average_power_density(audio_file):
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

    # Calculate power for each sample
    power = audio_array ** 2

    # Calculate average power density
    average_power_density = np.sum(power) / len(power)

    return average_power_density

# Example usage
audio_file_path = 'path/to/your/audio_file.wav'
average_power = calculate_average_power_density(audio_file_path)
print("Average Power Density:", average_power)
