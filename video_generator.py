import os
import cv2
import glob
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips

def get_image_files(image_dir, batch_size=10):
    """获取图片文件列表，每次返回batch_size个图片"""
    image_files = sorted(glob.glob(os.path.join(image_dir, "*.png")))
    for i in range(0, len(image_files), batch_size):
        yield image_files[i:i+batch_size]

def create_video_from_images(image_files, output_video_path, duration_per_image=2):
    """创建带缩放效果的视频"""
    clips = []
    
    for img_path in image_files:
        # 读取图片
        img = ImageClip(img_path)
        
        # 创建缩放效果
        def zoom(t):
            # 从1.0缩放到1.2
            return 1 + (0.2 * t/duration_per_image)
        
        # 应用缩放效果
        img = img.resize(zoom)
        
        # 设置持续时间
        img = img.set_duration(duration_per_image)
        
        clips.append(img)
    
    # 连接所有片段
    final_clip = CompositeVideoClip(clips)
    
    # 保存视频（暂时不带音频）
    final_clip.write_videofile(output_video_path, fps=30)
    
    return final_clip.duration

def add_background_music(video_path, audio_path, output_path):
    """添加背景音乐"""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # 裁剪音频至视频长度
    audio = audio.subclip(0, video.duration)
    
    # 合并视频和音频
    final_video = video.set_audio(audio)
    
    # 保存最终视频
    final_video.write_videofile(output_path)
    
    # 清理
    video.close()
    audio.close()
    final_video.close()

def merge_videos(video_files, output_path):
    """合并多个视频文件"""
    clips = [VideoFileClip(video) for video in video_files]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path)
    
    # 清理
    for clip in clips:
        clip.close()
    final_clip.close()

def main():
    image_dir = "演示图"
    final_video_path = "final_output.mp4"
    audio_path = "biubiubiu.m4a"
    batch_videos = []
    
    # 处理每一批图片
    for batch_num, image_batch in enumerate(get_image_files(image_dir)):
        output_path = f"batch_{batch_num}.mp4"
        final_batch_path = f"final_batch_{batch_num}.mp4"
        
        print(f"Processing batch {batch_num + 1}...")
        duration = create_video_from_images(image_batch, output_path)
        
        # 添加背景音乐
        print("Adding background music...")
        add_background_music(output_path, audio_path, final_batch_path)
        
        # 清理临时文件
        os.remove(output_path)
        batch_videos.append(final_batch_path)
        
        print(f"Batch {batch_num + 1} completed!")
    
    # 合并所有批次的视频
    print("Merging all videos...")
    merge_videos(batch_videos, final_video_path)
    
    # 清理批次视频文件
    for video in batch_videos:
        os.remove(video)
    
    print("All done! Final video saved as:", final_video_path)

if __name__ == "__main__":
    main() 