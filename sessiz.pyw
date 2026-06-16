import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import sys
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import logging
import ctypes

# Windows'ta yazıların bulanık görünmesini (DPI scaling) engellemek için
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


app = Flask(__name__)
CORS(app)

# Global reference to the UI instance so Flask can update it
ui_instance = None

@app.route('/api/download', methods=['POST'])
def handle_download():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"status": "error", "message": "URL eksik"}), 400
    
    video_url = data['url']
    headers = data.get('headers', {})
    
    if ui_instance:
        ui_instance.log(f"Eklentiden video linki alındı: {video_url[:60]}...")
        ui_instance.start_download(video_url, headers)
        
    return jsonify({"status": "success", "message": "İndirme başlatılıyor"})

class RetroUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sessiz - Chrome Eklentisi Bağlantılı")
        self.root.geometry("600x450")
        self.root.configure(bg="#d4d0c8")  # Win 98 Gray
        
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'S.png')
            if os.path.exists(icon_path):
                self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception:
            pass
        
        # Win 98 Style Font
        self.default_font = ("MS Sans Serif", 10)
        self.is_downloading = False
        
        self.setup_ui()
        
        global ui_instance
        ui_instance = self
        
        self.start_server()
        
    def setup_ui(self):
        # Top Frame for Status
        top_frame = tk.Frame(self.root, bg="#d4d0c8", padx=10, pady=10)
        top_frame.pack(fill=tk.X)
        
        tk.Label(top_frame, text="Bağlantı:", bg="#d4d0c8", font=self.default_font).pack(side=tk.LEFT)
        
        self.status_entry = tk.Entry(top_frame, width=50, font=self.default_font, relief=tk.SUNKEN, bd=2)
        self.status_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.status_entry.insert(0, "Eklentiden video bekleniyor... (Port: 5050)")
        self.status_entry.config(state="readonly")
        
        # Progress Frame (En alta sabitlemek için console'dan önce pack ediyoruz)
        progress_frame = tk.Frame(self.root, bg="#d4d0c8", padx=10, pady=10)
        progress_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))
        
        self.status_label = tk.Label(progress_frame, text="Hazır. Chrome Eklentisi bekleniyor...", bg="#d4d0c8", font=("MS Sans Serif", 10, "bold"))
        self.status_label.pack(side=tk.TOP, pady=2)
        
        # Log Console (Ortayı doldurması için en son pack ediyoruz)
        console_frame = tk.Frame(self.root, bg="#d4d0c8", padx=10, pady=5)
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(console_frame, text="İşlem Kayıtları:", bg="#d4d0c8", font=self.default_font).pack(anchor=tk.W)
        
        self.log_text = tk.Text(console_frame, bg="black", fg="#00ff00", font=("Consolas", 9), relief=tk.SUNKEN, bd=2)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

    def log(self, message):
        self.root.after(0, self._log, message)
        
    def _log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def update_status(self, text):
        self.root.after(0, lambda: self.status_label.config(text=text))
        
    def update_progress(self, percent):
        self.root.after(0, lambda: self.progress_var.set(percent))

    def start_server(self):
        self.log("Yerel sunucu başlatılıyor (localhost:5050)...")
        # Disable Flask logging to console
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        # Run Flask in a separate thread
        thread = threading.Thread(target=lambda: app.run(port=5050, use_reloader=False))
        thread.daemon = True
        thread.start()
        self.log("Sunucu çalışıyor. Tarayıcıda bir video açtığınızda eklenti buraya gönderecek.")

    def start_download(self, url, headers):
        if getattr(self, 'is_downloading', False):
            return
            
        self.is_downloading = True
        self.log("İndirme işlemi başlatılıyor...")
        self.update_progress(0)
        self.update_status("İndiriliyor...")
        
        thread = threading.Thread(target=self.run_download, args=(url, headers))
        thread.daemon = True
        thread.start()

    def run_download(self, url, headers):
        try:
            def hook(d):
                if d.get('status') == 'downloading':
                    try:
                        # yt-dlp sözlüğünde (dictionary) anahtarlar bazen 'None' değeri döndürebilir!
                        # .get('key', 'default') metodu eğer key varsa ama değeri None ise None döndürür.
                        # Bu yüzden direkt string'e çevirip strip yapmadan önce None kontrolü yapmalıyız.
                        p_val = d.get('_percent_str')
                        percent_str = str(p_val).strip() if p_val is not None else '0%'
                        
                        s_val = d.get('_speed_str')
                        speed_str = str(s_val).strip() if s_val is not None else 'N/A'
                        
                        e_val = d.get('_eta_str')
                        eta_str = str(e_val).strip() if e_val is not None else 'N/A'
                        
                        t_val = d.get('_total_bytes_str') or d.get('_total_bytes_estimate_str')
                        total_str = str(t_val).strip() if t_val is not None else 'N/A'
                        
                        import re
                        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                        
                        percent_str = ansi_escape.sub('', percent_str)
                        speed_str = ansi_escape.sub('', speed_str)
                        eta_str = ansi_escape.sub('', eta_str)
                        total_str = ansi_escape.sub('', total_str)
                        
                        # Yüzdeyi temizle
                        clean_percent = re.sub(r'[^\d.]', '', percent_str)
                        try:
                            percent = float(clean_percent) if clean_percent else 0.0
                        except ValueError:
                            percent = 0.0
                            
                        self.update_progress(percent)
                        
                        # İnsan dostu (human readable) çeviriler: GiB -> GB, KiB -> KB
                        speed_hr = speed_str.replace('KiB/s', ' KB/s').replace('MiB/s', ' MB/s').replace('GiB/s', ' GB/s')
                        total_hr = total_str.replace('KiB', ' KB').replace('MiB', ' MB').replace('GiB', ' GB').replace('~', 'Yaklaşık ')
                        
                        # Parça (fragment) bilgilerini al
                        frag_index = d.get('fragment_index')
                        frag_count = d.get('fragment_count')
                        
                        if frag_index and frag_count:
                            frag_info = f" (Parça: {frag_index}/{frag_count})"
                        else:
                            frag_info = ""
                            
                        # Eğer toplam boyut bilinmiyorsa inen miktarı göster
                        if total_hr and total_hr != 'N/A' and total_hr != 'Yaklaşık N/A':
                            boyut_bilgisi = f"Boyut: {total_hr}"
                        else:
                            downloaded_bytes = d.get('downloaded_bytes')
                            if downloaded_bytes:
                                downloaded_mb = downloaded_bytes / (1024 * 1024)
                                boyut_bilgisi = f"İnen: {downloaded_mb:.1f} MB"
                            else:
                                boyut_bilgisi = "Boyut: Bilinmiyor"
                            
                        # Ekrana basılacak son metin
                        status_text = f"⏳ %{percent:.1f}  |  💾 {boyut_bilgisi}  |  🚀 {speed_hr}  |  ⏱️ {eta_str}{frag_info}"
                        
                        self.update_status(status_text)
                    except Exception as e:
                        # Eğer bir hata olursa konsol yerine uygulamanın arayüzündeki siyah log ekranına yazdıralım.
                        self.log(f"Arayüz Güncelleme Hatası: {str(e)}")
                elif d.get('status') == 'finished':
                    self.log("İndirme bitti, dosya birleştiriliyor...")
                    self.update_progress(100)
                    self.update_status("İndirme tamamlandı! Ses ve görüntü birleştiriliyor...")

            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'progress_hooks': [hook],
                'quiet': True,
                'no_warnings': True,
                'http_headers': headers
            }

            self.log("yt-dlp ile indirme başlatıldı...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.log("İşlem başarıyla tamamlandı!")
            self.update_status("Tamamlandı. Yeni video bekleniyor...")
            self.update_progress(0)
            
        except Exception as e:
            self.log(f"Hata oluştu: {str(e)}")
            self.update_status("Hata.")
        finally:
            self.is_downloading = False

if __name__ == "__main__":
    root = tk.Tk()
    app_ui = RetroUI(root)
    root.mainloop()
