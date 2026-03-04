import subprocess
import sys
import os

def parse_timeline(timeline_str):
    # Example: 01:10-01:15, 03:20-03:35
    segments = []
    parts = timeline_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            segments.append((start.strip(), end.strip()))
    return segments

def download_video(url, output_name="input.mp4"):
    print(f"Downloading video from {url}...")
    # Using -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' to ensure mp4 format for easier processing
    subprocess.run([
        'yt-dlp',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', output_name,
        url
    ], check=True)
    return output_name

def clip_video(input_file, segments):
    clip_files = []
    for i, (start, end) in enumerate(segments):
        output_clip = f"clip_{i}.mp4"
        print(f"Clipping segment {i}: {start} to {end}...")
        # ffmpeg -ss start -to end -i input -c copy output
        # Using -c copy might be fast but can be inaccurate with keyframes.
        # Since we want to mix them, maybe re-encoding is safer.
        subprocess.run([
            'ffmpeg', '-y',
            '-ss', start,
            '-to', end,
            '-i', input_file,
            '-c:v', 'libx264', '-c:a', 'aac',
            output_clip
        ], check=True)
        clip_files.append(output_clip)
    return clip_files

def concatenate_videos(clip_files, output_file="final_video.mp4"):
    print("Concatenating clips...")
    with open('clips.txt', 'w') as f:
        for clip in clip_files:
            f.write(f"file '{clip}'\n")

    subprocess.run([
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'clips.txt',
        '-c', 'copy',
        output_file
    ], check=True)

    # Cleanup
    os.remove('clips.txt')
    for clip in clip_files:
        os.remove(clip)

def main():
    if len(sys.argv) < 3:
        print("Usage: python edit_video.py <youtube_url> <timeline>")
        sys.exit(1)

    url = sys.argv[1]
    timeline_str = sys.argv[2]

    segments = parse_timeline(timeline_str)
    if not segments:
        print("No valid segments found in timeline.")
        sys.exit(1)

    input_video = download_video(url)
    try:
        clips = clip_video(input_video, segments)
        concatenate_videos(clips)
    finally:
        if os.path.exists(input_video):
            os.remove(input_video)

    print(f"Done! Final video saved as final_video.mp4")

if __name__ == "__main__":
    main()
