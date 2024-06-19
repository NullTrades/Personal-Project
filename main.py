import subprocess
import threading
from collections import deque
from datetime import datetime
import argparse
import os
import time

def capture_stream_with_buffer(streamer, buffer_duration=15):
    stream_url = 'https://www.twitch.tv/' + streamer
    # Streamlink command to stream directly to stdout at the best available quality
    command = ['streamlink', '--twitch-disable-ads', '--stdout', stream_url, 'best']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=10**8)

    # Approximate size of a chunk based on average bitrate and buffer duration
    avg_bitrate = 5000000
    bytes_per_second = avg_bitrate // 8
    buffer_size = bytes_per_second * buffer_duration

    # Initialize a deque as a buffer with a calculated maximum length to hold the last 15 seconds of data
    buffer = deque(maxlen=buffer_size)

    def check_input():
        while True:
            if os.path.exists('end_clip.txt'):
                try:
                    os.remove('end_clip.txt')
                    process.terminate()  # Stops the stream capture when "end_clip.txt" is created
                    break
                except PermissionError:
                    time.sleep(0.1)  # Wait a bit before trying again

    # Start the input thread
    input_thread = threading.Thread(target=check_input)
    input_thread.start()

    try:
        # Keep reading data from the stream until the process is alive
        while process.poll() is None:
            data = process.stdout.read(1880)  # Read in chunks equivalent to one TS packet
            if data:
                buffer.append(data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        process.terminate()

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{streamer}_saved_segment_{timestamp}.mp4'

    # Write the data from the buffer to a file with timestamp in filename
    with open(filename, 'wb') as file:
        for chunk in buffer:
            file.write(chunk)
        print(f"Saved the last 15 seconds of the stream to '{filename}'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("streamer", help="the name of the streamer")
    args = parser.parse_args()

    streamer = args.streamer
    print(f'Program operation on the following channel https://www.twitch.tv/{streamer}')
    capture_stream_with_buffer(streamer, 15)
