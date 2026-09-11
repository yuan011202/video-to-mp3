# main.py - 视频转MP3 APP
import os
import subprocess
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.utils import platform


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        self.selected_file = None

        self.title = Label(
            text="视频提取MP3",
            font_size='24sp',
            size_hint=(1, 0.15),
            bold=True
        )
        self.add_widget(self.title)

        self.path_label = Label(
            text="未选择文件",
            font_size='14sp',
            size_hint=(1, 0.2),
            text_size=(None, None)
        )
        self.add_widget(self.path_label)

        self.select_btn = Button(
            text="选择视频",
            font_size='18sp',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.9, 1)
        )
        self.select_btn.bind(on_press=self.open_file_chooser)
        self.add_widget(self.select_btn)

        self.convert_btn = Button(
            text="开始提取MP3",
            font_size='18sp',
            size_hint=(1, 0.2),
            background_color=(0.3, 0.8, 0.3, 1),
            disabled=True
        )
        self.convert_btn.bind(on_press=self.start_convert)
        self.add_widget(self.convert_btn)

        self.status = Label(
            text="就绪",
            font_size='14sp',
            size_hint=(1, 0.15)
        )
        self.add_widget(self.status)

    def open_file_chooser(self, *args):
        content = BoxLayout(orientation='vertical')
        # 安卓默认从 /sdcard 开始
        start_path = '/sdcard' if platform == 'android' else os.path.expanduser('~')
        fc = FileChooserListView(path=start_path, filters=['*.mp4', '*.avi', '*.mov', '*.mkv', '*.3gp'])
        content.add_widget(fc)

        btn_box = BoxLayout(size_hint=(1, 0.15), spacing=10)
        ok_btn = Button(text="确定")
        cancel_btn = Button(text="取消")
        btn_box.add_widget(ok_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)

        popup = Popup(title="选择视频文件", content=content, size_hint=(0.95, 0.95))

        def on_ok(*a):
            if fc.selection:
                self.selected_file = fc.selection[0]
                self.path_label.text = os.path.basename(self.selected_file)
                self.convert_btn.disabled = False
                self.status.text = "已选择，可以开始"
            popup.dismiss()

        ok_btn.bind(on_press=on_ok)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()

    def start_convert(self, *args):
        if not self.selected_file:
            return
        self.convert_btn.disabled = True
        self.status.text = "正在提取，请稍候..."
        threading.Thread(target=self.do_convert, daemon=True).start()

    def do_convert(self):
        video = self.selected_file
        output = os.path.splitext(video)[0] + ".mp3"

        # APK 里的 ffmpeg 路径
        if platform == 'android':
            ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg')
            # 确保有执行权限
            try:
                os.chmod(ffmpeg_path, 0o755)
            except Exception:
                pass
        else:
            ffmpeg_path = 'ffmpeg'  # 电脑测试用系统的

        cmd = [
            ffmpeg_path,
            "-i", video,
            "-vn",
            "-acodec", "libmp3lame",
            "-b:a", "192k",
            "-y",
            output
        ]

        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            if r.returncode == 0 and os.path.exists(output):
                msg = f"完成！\n{output}"
            else:
                msg = "失败：" + (r.stderr or "")[-200:]
        except Exception as e:
            msg = "异常：" + str(e)

        Clock.schedule_once(lambda dt: self.show_result(msg))

    def show_result(self, msg):
        self.status.text = msg.split("\n")[0]
        self.convert_btn.disabled = False
        popup = Popup(
            title="结果",
            content=Label(text=msg),
            size_hint=(0.9, 0.4)
        )
        popup.open()


class VideoToMp3App(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    VideoToMp3App().run()