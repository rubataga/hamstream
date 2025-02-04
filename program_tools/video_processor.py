import ffmpeg

def get_video_length(video_path):
    """Get the length of a video in seconds."""
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        duration = float(video_stream['duration'])
        return duration
    except Exception as e:
        print(f"[ERROR] Failed to get video length: {e}")
        return None

# Example usage
if __name__ == "__main__":
    video_path = 'path/to/your/video.mp4'
    length = get_video_length(video_path)
    if length is not None:
        print(f"Video length: {length} seconds")