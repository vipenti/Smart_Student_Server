import pyaudio
import wave
import keyboard
import winsound
import soundfile as sf
import io
import numpy as np
import wave
import webrtcvad
import os


class AudioManager:
    # Frame duration in ms
    MAX_SILENT_FRAMES = 30  # ms of silence to end recording; must 10/20/30ms for VAD
    # Allowed sample rates for VAD
    VAD_ALLOWED_SAMPLERATES = [8000, 16000, 32000, 48000]
    # Default folder to save the recordings
    DEFAULT_SAVING_FOLDER = "recordings"

    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=1, sample_rate=32000, max_silent_seconds=5, max_sample_length=30):
        self.recording = False  # Flag to indicate if the recording is ongoing
        self.frames = []        # List to store the audio frames
        self.chunk = chunk      # Number of frames per buffer
        self.sample_format = sample_format  # Format of the audio samples
        self.channels = channels            # Number of audio channels
        self.sample_rate = sample_rate      # Number of samples per second
        self.p = None                       # PyAudio object
        self.stream = None                  # PyAudio stream
        self.vad = webrtcvad.Vad(2)         # Voice Activity Detection object
        self.samples_per_frame = int(
            sample_rate / 1000 * self.MAX_SILENT_FRAMES) # Number of samples per frame duration
        
        self.max_silent_seconds = max_silent_seconds     # Maximum number of seconds of silence to end recording
        self.max_sample_length = max_sample_length       # Maximum number of seconds of recording allowed

    def time_to_frames(self, time):
        return int(time * 1000 / self.MAX_SILENT_FRAMES)

    # Starts live recording
    def start(self, voice_activity_detection=False, interrupt_key='q'):
        try:
            if self.channels > 1 or self.sample_format != pyaudio.paInt16 or self.sample_rate not in self.VAD_ALLOWED_SAMPLERATES:
                raise Exception(
                    "Invalid configuration for Voice Activation Detection")
        except Exception as e:
            print(e)
            voice_activity_detection = False  # Disable VAD if the configuration is invalid

        self.recording = True
        self.frames = []    # Reset the frames list

        # silence time divided in terms of frames
        silent_frames = int(self.max_silent_seconds *
                            1000 / self.MAX_SILENT_FRAMES)
        max_frames = int(self.max_sample_length *
                         1000 / self.MAX_SILENT_FRAMES)

        silences = speaking_frames = 0

        # Signal to notify the start of recording
        winsound.Beep(1000, 200)

        # Open the audio stream
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  frames_per_buffer=self.chunk,
                                  input=True)

        # Start recording
        while self.recording:
            # Read the audio frames and append them to the list
            detectable_frames = self.stream.read(self.samples_per_frame)
            self.frames.append(detectable_frames)

            # Voice Activity Detection
            if voice_activity_detection:
                if not self.vad.is_speech(detectable_frames, self.sample_rate):
                    silences += 1

                    # If the number of silences is greater than the time subdivisions (it reaches the seconds of silence) then stop the recording
                    if silences >= silent_frames:
                        print('[Recording Stopped] Reached Silence Threshold')
                        self.stop()

                    if speaking_frames >= max_frames:
                        print(
                            '[Recording Stopped] Reached Maximum Recording Length')
                        self.stop()

                else:
                    silences = 0
                    speaking_frames += 1

                    silent_frames -= int(silent_frames / 5)

            # Manual termination of the recording by pressing specified key
            if keyboard.is_pressed(interrupt_key):
                print('[Recording Stopped] Manual Termination')
                self.stop()

    # Stops live recording
    def stop(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    # Saves the recording to a .wav file
    def save(self, filename, folder=None):
        if not filename:
            raise Exception("Invalid filename")

        if not folder:
            folder = self.DEFAULT_SAVING_FOLDER

        filename = os.path.join(folder, filename)

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()

    # Saves recording to a byte buffer and returns it
    def save_temp(self):
        buffer = io.BytesIO()

        with wave.open(buffer, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()

        return buffer

    # Plays the audio file at the given file path
    def play_audio(self, audio_file_path):
        if not (audio_file_path or os.path.exists(audio_file_path)):
            raise Exception("Invalid audio file path")

        # Opens the file and reads in groups of "chunk" frames
        with sf.SoundFile(audio_file_path, 'r') as sound_file:
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=sound_file.channels,
                                rate=sound_file.samplerate, output=True)
            data = sound_file.read(self.chunk, dtype='int16')

            while len(data) > 0:
                stream.write(data.tobytes())
                data = sound_file.read(self.chunk, dtype='int16')

            stream.stop_stream()
            stream.close()
            audio.terminate()
