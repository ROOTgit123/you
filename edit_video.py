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

def download_with_yt_dlp(url, output_name, extractor_args=None, use_aria2=False):
    print(f"Downloading with yt-dlp (aria2={use_aria2}, args={extractor_args})...")
    cmd = [
        'yt-dlp',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        '--merge-output-format', 'mp4',
        '-o', output_name,
    ]
    if extractor_args:
        cmd.extend(['--extractor-args', extractor_args])
    if use_aria2:
        cmd.extend(['--external-downloader', 'aria2c'])
    if os.path.exists('cookies.txt'):
        cmd.extend(['--cookies', 'cookies.txt'])
    cmd.append(url)
    subprocess.run(cmd, check=True)

def download_with_you_get(url, output_name):
    print("Downloading with you-get...")
    # you-get doesn't have a direct -o for filename including extension easily for all sites
    # so we download then rename
    subprocess.run(['you-get', '-o', '.', url], check=True)
    # Find the downloaded file (this is a bit naive but works for single download)
    files = [f for f in os.listdir('.') if f.endswith('.mp4') or f.endswith('.mkv')]
    if files:
        # Sort by mtime to get the latest if multiple exist
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        os.rename(files[0], output_name)
    else:
        raise Exception("you-get failed to download video")

def download_video(url, method="auto", output_name="input.mp4"):
    methods = {
        "yt-dlp-android": lambda: download_with_yt_dlp(url, output_name, extractor_args="youtube:player_client=android,web"),
        "yt-dlp-aria2c": lambda: download_with_yt_dlp(url, output_name, use_aria2=True),
        "you-get": lambda: download_with_you_get(url, output_name),
        "yt-dlp-basic": lambda: download_with_yt_dlp(url, output_name)
    }

    if method != "auto":
        if method in methods:
            methods[method]()
            return output_name
        else:
            print(f"Unknown method {method}, falling back to auto")

    # Auto fallback logic
    order = ["yt-dlp-android", "yt-dlp-aria2c", "you-get", "yt-dlp-basic"]
    for m in order:
        try:
            methods[m]()
            return output_name
        except Exception as e:
            print(f"Method {m} failed: {e}")
            continue

    raise Exception("All download methods failed")

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
        print("Usage: python edit_video.py <youtube_url> <timeline> [method]")
        sys.exit(1)

    url = sys.argv[1]
    timeline_str = sys.argv[2]
    method = sys.argv[3] if len(sys.argv) > 3 else "auto"

    segments = parse_timeline(timeline_str)
    if not segments:
        print("No valid segments found in timeline.")
        sys.exit(1)

    input_video = download_video(url, method=method)
    try:
        clips = clip_video(input_video, segments)
        concatenate_videos(clips)
    finally:
        if os.path.exists(input_video):
            os.remove(input_video)

    print(f"Done! Final video saved as final_video.mp4")

if __name__ == "__main__":
    main()
