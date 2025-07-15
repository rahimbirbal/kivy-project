# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics import Color, Ellipse, InstructionGroup

import cv2
import joblib
import pandas as pd

# Load model warna
model = joblib.load("model_svm.pkl")

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text="Pilih metode deteksi warna", font_size=24))

        btn_upload = Button(text="Upload Gambar", size_hint=(1, 0.3))
        btn_upload.bind(on_press=self.goto_upload)

        btn_camera = Button(text="Gunakan Kamera", size_hint=(1, 0.3))
        btn_camera.bind(on_press=self.goto_camera)

        layout.add_widget(btn_upload)
        layout.add_widget(btn_camera)

        self.add_widget(layout)

    def goto_upload(self, instance):
        self.manager.current = 'upload_screen'

    def goto_camera(self, instance):
        self.manager.current = 'camera_screen'

# class UploadScreen(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

#         self.choose_btn = Button(text='Upload Gambar', size_hint_y=None, height=50)
#         self.choose_btn.bind(on_press=self.buka_filechooser)
#         self.layout.add_widget(self.choose_btn)

#         self.image = Image(size_hint=(1, None), allow_stretch=True, keep_ratio=True)
#         self.image.bind(on_touch_down=self.on_touch_image)
#         self.layout.add_widget(self.image)

#         self.result_label = Label(
#             text='Klik gambar untuk deteksi warna',
#             size_hint_y=None,
#             height=50,
#             color=(0, 0, 0, 1),
#             font_size=16
#         )
#         self.layout.add_widget(self.result_label)

#         self.add_widget(self.layout)
#         self.cv_img = None

#     def buka_filechooser(self, instance):
#         content = FileChooserIconView()
#         popup = Popup(title="Pilih Gambar", content=content, size_hint=(0.9, 0.9))

#         def select(*args):
#             if content.selection:
#                 self.img_path = content.selection[0]
#                 popup.dismiss()
#                 self.load_image(self.img_path)

#         content.bind(on_submit=lambda *args: select())
#         popup.open()

#     def load_image(self, path):
#         self.cv_img = cv2.imread(path)
#         if self.cv_img is None:
#             self.result_label.text = "Gagal membuka gambar."
#             return

#         self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2RGB)
#         h, w, _ = self.cv_img.shape

#         buf = self.cv_img.tobytes()
#         texture = Texture.create(size=(w, h), colorfmt='rgb')
#         texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
#         texture.flip_vertical()
#         self.image.texture = texture
#         self.image.size = (w, h)
#         self.result_label.text = "Klik gambar untuk deteksi warna"

#     def on_touch_image(self, instance, touch):
#         if not self.cv_img or not self.image.collide_point(*touch.pos):
#             return False

#         rel_x = touch.x - self.image.pos[0]
#         rel_y = touch.y - self.image.pos[1]

#         img_w, img_h = self.image.texture.size
#         tex_w, tex_h = self.cv_img.shape[1], self.cv_img.shape[0]

#         scale_x = tex_w / img_w
#         scale_y = tex_h / img_h

#         x = int(rel_x * scale_x)
#         y = int(rel_y * scale_y)

#         if 0 <= x < tex_w and 0 <= y < tex_h:
#             pixel = self.cv_img[y, x]
#             df = pd.DataFrame([[pixel[0], pixel[1], pixel[2]]],
#                               columns=["Red (8 bit)", "Green (8 bit)", "Blue (8 bit)"])
#             warna = model.predict(df)[0]
#             self.result_label.text = f"({x},{y}) → RGB: {tuple(pixel)} → Warna: {warna}"

#         return True
class UploadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Tombol Upload
        self.choose_btn = Button(text='Upload Gambar', size_hint_y=None, height=50)
        self.choose_btn.bind(on_press=self.buka_filechooser)
        self.layout.add_widget(self.choose_btn)

        # Widget untuk menampilkan gambar
        self.image = Image(size_hint=(1, None), allow_stretch=True, keep_ratio=True)
        self.image.bind(on_touch_down=self.on_touch_image)
        self.layout.add_widget(self.image)

        # Label hasil deteksi
        self.result_label = Label(
            text='Klik gambar untuk deteksi warna',
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1),
            font_size=16
        )
        self.layout.add_widget(self.result_label)

        self.add_widget(self.layout)

        # Inisialisasi
        self.cv_img = None  # Gambar OpenCV
        self.img_path = None

    def buka_filechooser(self, instance):
        chooser = FileChooserIconView()
        popup = Popup(title="Pilih Gambar", content=chooser, size_hint=(0.9, 0.9))

        def pilih(*args):
            if chooser.selection:
                self.img_path = chooser.selection[0]
                popup.dismiss()
                self.load_image(self.img_path)

        chooser.bind(on_submit=lambda *args: pilih())
        popup.open()

    def load_image(self, path):
        self.cv_img = cv2.imread(path)
        if self.cv_img is None:
            self.result_label.text = "Gagal membuka gambar."
            return

        self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2RGB)
        h, w, _ = self.cv_img.shape

        texture = Texture.create(size=(w, h), colorfmt='rgb')
        texture.blit_buffer(self.cv_img.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()

        self.image.texture = texture
        self.image.size_hint = (1, None)
        self.image.height = min(h, 500)  # Agar tidak terlalu tinggi

        self.image.canvas.after.clear()
        self.result_label.text = "Klik gambar untuk deteksi warna"

    def on_touch_image(self, instance, touch):
        if self.cv_img is None or not self.image.collide_point(*touch.pos):
            return False

        img_w, img_h = self.image.width, self.image.height
        tex_w, tex_h = self.cv_img.shape[1], self.cv_img.shape[0]

        rel_x = (touch.x - self.image.x) / img_w
        rel_y = (touch.y - self.image.y) / img_h

        if not (0 <= rel_x <= 1 and 0 <= rel_y <= 1):
            return False

        x = int(rel_x * tex_w)
        y = int((1 - rel_y) * tex_h)

        try:
            pixel = self.cv_img[y, x]
            r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
            df = pd.DataFrame([[r, g, b]], columns=["Red (8 bit)", "Green (8 bit)", "Blue (8 bit)"])
            warna = model.predict(df)[0]

            self.result_label.text = f"({x},{y}) → RGB: ({r},{g},{b}) → Warna: {warna}"
            self.result_label.color = (1, 0, 0, 1)  # Merah terang
            self.result_label.bold = True
            print(f"Klik di ({x}, {y}) → RGB: ({r}, {g}, {b}) → Warna: {warna}")



            self.image.canvas.after.clear()
            with self.image.canvas.after:
                Color(0, 1, 0, 1)
                Ellipse(pos=(touch.x - 5, touch.y - 5), size=(10, 10))

        except Exception as e:
            self.result_label.text = f"Error: {e}"
            print("Error saat prediksi:", e)

        return True


class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.image = Image()
        self.label = Label(text="Mendeteksi warna di tengah frame")

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

        self.capture = None
        self.event = None

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        from kivy.clock import Clock
        self.event = Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self):
        if self.capture:
            self.capture.release()
        if self.event:
            self.event.cancel()

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 0)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, _ = rgb_frame.shape
            center_x, center_y = w // 2, h // 2
            center_pixel = rgb_frame[center_y, center_x]

            df = pd.DataFrame([[center_pixel[0], center_pixel[1], center_pixel[2]]], columns=["Red (8 bit)", "Green (8 bit)", "Blue (8 bit)"])
            warna = model.predict(df)[0]

            # Tambahkan lingkaran hijau kecil di tengah
            cv2.circle(rgb_frame, (center_x, center_y), 10, (0, 255, 0), 2)

            buf = rgb_frame.tobytes()
            texture = Texture.create(size=(w, h), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.image.texture = texture

            self.label.text = f"Tengah → RGB: {tuple(center_pixel)} → Warna: {warna}"


class WarnaApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main'))
        sm.add_widget(UploadScreen(name='upload_screen'))
        sm.add_widget(CameraScreen(name='camera_screen'))
        return sm

if __name__ == '__main__':
    WarnaApp().run()
