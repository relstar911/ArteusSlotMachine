import wave
import struct
import math
import os

def create_sine_wave(frequency, duration, amplitude=0.5, sample_rate=44100):
    n_samples = int(sample_rate * duration)
    wave_data = []
    for i in range(n_samples):
        t = float(i) / sample_rate
        wave_data.append(amplitude * math.sin(2 * math.pi * frequency * t))
    return wave_data

def save_wave(filename, wave_data, sample_rate=44100):
    wav_file = wave.open(filename, 'w')
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample
    wav_file.setframerate(sample_rate)
    
    # Convert floating point wave data to integer format
    scaled_wave = [int(sample * 32767) for sample in wave_data]
    
    # Pack wave data into binary string
    wave_packed = struct.pack('<%dh' % len(scaled_wave), *scaled_wave)
    
    wav_file.writeframes(wave_packed)
    wav_file.close()

# Create sounds directory if it doesn't exist
os.makedirs('assets/sounds', exist_ok=True)

# Create spin sound (descending tone)
spin_wave = []
for i in range(44100):  # 1 second
    t = float(i) / 44100
    frequency = 440 * (1 - t/2)  # Descending from 440Hz to 220Hz
    spin_wave.append(0.5 * math.sin(2 * math.pi * frequency * t))
save_wave('assets/sounds/spin.wav', spin_wave)

# Create stop sound (short beep)
stop_wave = create_sine_wave(880, 0.1)  # 880Hz for 0.1 seconds
save_wave('assets/sounds/stop.wav', stop_wave)

# Create jackpot sound (ascending arpeggio)
jackpot_wave = []
frequencies = [440, 550, 660, 880]  # A4, C#5, E5, A5
for freq in frequencies:
    jackpot_wave.extend(create_sine_wave(freq, 0.2))
save_wave('assets/sounds/jackpot.wav', jackpot_wave)

print("Sound files created successfully!")
