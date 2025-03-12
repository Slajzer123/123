import tkinter as tk
from PIL import Image, ImageTk
import time
import os


class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("какаято хуєта")
        self.root.resizable(False, False)

        self.digit_images = []

        for i in range(10):
            img_path = ""
            if i == 0:
                img_path = os.path.join('images', '0_number.png')
                if not os.path.exists(img_path):
                    img_path = os.path.join('images', '0_number.png')
            else:
                img_path = os.path.join('images', f'{i}_number.png')

                if not os.path.exists(img_path):
                    img_path = os.path.join('images', f'{i}_number.png')

            if os.path.exists(img_path):
                image = Image.open(img_path)
                image = image.resize((100, 150), Image.Resampling.LANCZOS)
                self.digit_images.append(ImageTk.PhotoImage(image))
            else:
                print(f"ніхуя не знайдено")
                empty_img = Image.new('RGB', (100, 150), color=(255, 255, 255))
                self.digit_images.append(ImageTk.PhotoImage(empty_img))

        colon_path = os.path.join('images', 'colon.png')
        if os.path.exists(colon_path):
            colon_image = Image.open(colon_path)
            self.colon_image = ImageTk.PhotoImage(colon_image)
        else:
            temp_img = Image.new('RGB', (50, 150), color=(255, 255, 255))
            self.colon_image = ImageTk.PhotoImage(temp_img)

        self.clock_frame = tk.Frame(root, bg='white', padx=20, pady=20)
        self.clock_frame.pack(padx=10, pady=10)

        self.hour_tens = tk.Label(self.clock_frame, bg='white')
        self.hour_tens.grid(row=0, column=0)

        self.hour_ones = tk.Label(self.clock_frame, bg='white')
        self.hour_ones.grid(row=0, column=1)

        self.colon1 = tk.Label(self.clock_frame, image=self.colon_image, bg='white')
        self.colon1.grid(row=0, column=2)

        self.minute_tens = tk.Label(self.clock_frame, bg='white')
        self.minute_tens.grid(row=0, column=3)

        self.minute_ones = tk.Label(self.clock_frame, bg='white')
        self.minute_ones.grid(row=0, column=4)

        self.colon2 = tk.Label(self.clock_frame, image=self.colon_image, bg='white')
        self.colon2.grid(row=0, column=5)

        self.second_tens = tk.Label(self.clock_frame, bg='white')
        self.second_tens.grid(row=0, column=6)

        self.second_ones = tk.Label(self.clock_frame, bg='white')
        self.second_ones.grid(row=0, column=7)

        self.root.configure(bg='white')

        self.update_time()

    def update_time(self):
        current_time = time.localtime()
        hours = current_time.tm_hour
        minutes = current_time.tm_min
        seconds = current_time.tm_sec

        hour_tens_digit = hours // 10
        hour_ones_digit = hours % 10

        minute_tens_digit = minutes // 10
        minute_ones_digit = minutes % 10

        second_tens_digit = seconds // 10
        second_ones_digit = seconds % 10

        self.hour_tens.config(image=self.digit_images[hour_tens_digit])
        self.hour_ones.config(image=self.digit_images[hour_ones_digit])
        self.minute_tens.config(image=self.digit_images[minute_tens_digit])
        self.minute_ones.config(image=self.digit_images[minute_ones_digit])
        self.second_tens.config(image=self.digit_images[second_tens_digit])
        self.second_ones.config(image=self.digit_images[second_ones_digit])

        self.root.after(1000, self.update_time)


if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalClock(root)
    root.mainloop()

