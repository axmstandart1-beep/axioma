import os
import time
import subprocess

input_file = "/sdcard/Download/laamaian.mp4"
output_file = "/sdcard/Download/laamaian_axioma_perceptual.mp4"

def run_axioma_media(in_path, out_path):
    print("="*55)
    print("🧠 AXIOMA: PERCEPTUAL COMPRESSION (AV1)")
    print("="*55)

    in_size = os.path.getsize(in_path) / (1024 * 1024)
    print(f"📦 Source: {in_size:.2f} MB")
    print("⚡ Activating modules: Grain Synthesis + Adaptive Quantization...")

    cmd = [
        "ffmpeg", "-y", "-i", in_path,
        "-c:v", "libsvtav1",
        "-preset", "10",
        "-crf", "45",
        "-svtav1-params", "film-grain=15:enable-qm=1:aq-mode=2",
        "-vf", "scale=-2:480",
        "-c:a", "libopus",
        "-b:a", "32k",
        out_path
    ]

    t0 = time.time()
    process = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    t1 = time.time()

    if not os.path.exists(out_path):
        print("❌ Compression error. FFmpeg output:")
        print(process.stderr[:500])
        return

    out_size = os.path.getsize(out_path) / (1024 * 1024)
    ratio = ((in_size - out_size) / in_size) * 100

    print("-" * 55)
    print(f"✅ Output ready: {os.path.basename(out_path)}")
    print(f"📊 Original: {in_size:.2f} MB")
    print(f"📊 Compressed: {out_size:.2f} MB")
    print(f"🔥 Ratio: {ratio:.1f}%")
    print(f"⏱ Time: {t1 - t0:.1f} sec")
    print("-" * 55)

if __name__ == "__main__":
    if os.path.exists(input_file):
        run_axioma_media(input_file, output_file)
    else:
        print(f"❌ File not found: {input_file}")
