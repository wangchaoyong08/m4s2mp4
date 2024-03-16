import os
import json
import subprocess


def filter_invalid_win_chars(s):
    """Windows不允许的字符  """
    invalid_chars = '<>:"/\\|?*'
    # 替换所有无效字符为下划线
    for char in invalid_chars:
        s = s.replace(char, '_')
        # 如果文件名以空格或点号开头，也替换为下划线
    if s.startswith((' ', '.')):
        s = '_' + s[1:]
    return s


def merge_audio_video(video_path, audio_path, output_path):
    command = [
        ".\\ffmpeg.exe", "-y",  # 重复文件允许覆盖
        "-loglevel", "quiet",  # 不显示日志
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "copy",
        output_path]
    try:
        subprocess.run(command, check=True)
        print(f"合并成功，输出文件：{output_path}")
    except subprocess.CalledProcessError as e:
        print(f"合并失败，错误信息：{e}")


if __name__ == '__main__':
    # 指定根目录、输出目录
    rootdir = input("输入视频缓存文件根目录：")
    outdir = input("指定输出目录：")
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    for basic_dir, dirs, files in os.walk(rootdir):
        if "entry.json" in files:
            # 1.读取json文件
            with open(os.path.join(basic_dir, "entry.json"), encoding="utf-8") as f:
                data = json.load(f)
                title = filter_invalid_win_chars(data.get("title"))
                type_tag = data.get("type_tag")
                part = filter_invalid_win_chars(data.get("page_data").get("part"))
            # 2.创建输出目录，判断文件是否存在
            p_dirs = basic_dir[len(rootdir) + 1:].split("\\")
            if len(p_dirs) != 2:
                continue

            title_path = os.path.join(outdir, title)
            if not os.path.exists(title_path):
                os.mkdir(title_path)

            # 3.合并视频文件
            merge_audio_video(os.path.join(basic_dir, type_tag, "video.m4s"),
                              os.path.join(basic_dir, type_tag, "audio.m4s"), os.path.join(title_path, part + ".mp4"))
