# Sessiz Video Downloader / Sessiz Video İndirme Uygulaması

[English](#english) | [Türkçe](#türkçe)

---

## English

**Sessiz** is a lightweight, high-performance desktop application designed to capture and download video streams at their highest available quality without authorization or permission errors. It uses a Chrome extension to intercept video stream requests (such as `.m3u8` or `.mp4`) and forwards them to a local Python Flask server, which triggers `yt-dlp` to download and merge the audio and video streams using `ffmpeg`.

### Features
* **Automatic Link Capture:** Seamless Chrome extension detects streaming links as you watch videos.
* **Maximum Quality:** Automatically downloads the best video + best audio and merges them.
* **Retro Win98 Aesthetic:** Clean and classic Tkinter graphical user interface.
* **Real-time Progress:** Live speed, ETA, download size, and fragment tracking display.

---

### Prerequisites

#### 1. Install FFmpeg
The application requires **FFmpeg** to merge separate audio and video streams.

* **Windows:**
  Open PowerShell as Administrator and run:
  ```powershell
  winget install ffmpeg
  ```
  *Restart your terminal or computer afterward.*
* **macOS:**
  Open Terminal and run:
  ```bash
  brew install ffmpeg
  ```

To verify the installation, run the following command in your terminal:
```bash
ffmpeg -version
```

#### 2. Install Python Dependencies
Install the required packages using `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### How to Use

#### Step 1: Run the Desktop Application
Start the desktop application by running the following command in the project directory:
```bash
python sessiz.py
```
*(Or double-click `sessiz.pyw` to run it silently in the background if Python launcher is configured.)*

You should see the UI window showing **"Eklentiden video bekleniyor... (Port: 5050)"** (Waiting for video from extension...).

#### Step 2: Install the Chrome Extension
1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer Mode** using the toggle in the top-right corner.
3. Click **Load unpacked** (Paketlenmemiş öğe yükle) in the top-left corner.
4. Select the `sessiz_extension` folder from this project directory.

#### Step 3: Start Downloading
1. Open any video in your Chrome browser and play it.
2. The extension will automatically capture the streaming URL and headers, then forward them to the desktop application.
3. The desktop app will automatically begin downloading the video in the highest quality and display the progress.
4. Once completed, the final merged `.mp4` file will be saved in the project directory.

> [!NOTE]
> **Important Note:** Once a download completes, rename or move the downloaded video file. If you attempt to download another video, the program might skip it if it detects a file with the exact same name to prevent overwriting.

---

### Creator / Developer
* **Username:** tembel teneke

---

## Türkçe

**Sessiz**, yetki hatası almadan videoları en yüksek kalitede indirmenizi sağlayan, hafif ve yüksek performanslı bir masaüstü uygulamasıdır. Tarayıcınızda oynatılan video akışlarını (`.m3u8`, `.mp4` vb.) yakalayan bir Chrome eklentisiyle birlikte çalışır. Yakalanan bağlantılar yerel Flask sunucusuna iletilir ve `yt-dlp` ile `ffmpeg` aracılığıyla ses/video birleştirilerek indirilir.

### Özellikler
* **Otomatik Bağlantı Yakalama:** Chrome eklentisi, siz tarayıcıda gezinirken video bağlantılarını arka planda otomatik olarak yakalar.
* **En Yüksek Kalite:** En iyi görüntü ve ses kalitesini otomatik olarak tespit edip indirir, ardından birleştirir.
* **Klasik Win98 Tasarımı:** Sade ve nostaljik Tkinter grafik arayüzü.
* **Canlı Durum Takibi:** İndirme hızı, kalan süre, dosya boyutu ve parça ilerlemesi anlık olarak gösterilir.

---

### Gereksinimler

#### 1. FFmpeg Kurulumu
Uygulamanın indirilen ses ve görüntü parçalarını sorunsuz birleştirebilmesi için **FFmpeg** bilgisayarınızda kurulu olmalıdır.

* **Windows İçin:**
  PowerShell'i yönetici olarak açın ve şu komutu çalıştırın:
  ```powershell
  winget install ffmpeg
  ```
  *Kurulum tamamlandıktan sonra terminali kapatıp yeniden açın.*
* **macOS İçin:**
  Terminali açıp şu komutu çalıştırın:
  ```bash
  brew install ffmpeg
  ```

Kurulumun doğruluğunu kontrol etmek için terminalde şu komutu çalıştırın:
```bash
ffmpeg -version
```

#### 2. Python Kütüphanelerinin Kurulumu
Gerekli bağımlılıkları yüklemek için proje dizininde şu komutu çalıştırın:
```bash
pip install -r requirements.txt
```

---

### Kullanım Adımları

#### 1. Adım: Masaüstü Uygulamasını Başlatın
Proje klasöründeyken terminalde şu komutu çalıştırarak uygulamayı açın:
```bash
python sessiz.py
```
*(Eğer bilgisayarınızda Python Launcher yüklü ise `sessiz.pyw` dosyasına çift tıklayarak da arka planda çalıştırabilirsiniz.)*

Arayüzde **"Eklentiden video bekleniyor... (Port: 5050)"** ifadesini görmelisiniz.

#### 2. Adım: Eklentiyi Chrome'a Yükleyin
1. Chrome tarayıcınızda `chrome://extensions/` adresine gidin.
2. Sağ üst köşeden **Geliştirici Modu**'nu (Developer Mode) aktif hale getirin.
3. Sol üstte çıkan **Paketlenmemiş öğe yükle** (Load unpacked) butonuna tıklayın.
4. Bu proje klasörünün içindeki `sessiz_extension` klasörünü seçip yükleyin.

#### 3. Adım: İndirmeye Başlayın
1. Tarayıcınızda indirmek istediğiniz bir videoyu açıp oynatın.
2. Eklenti video linkini ve gerekli başlık bilgilerini yakalayarak masaüstü uygulamasına iletecektir.
3. Uygulama indirme işlemini otomatik olarak başlatır ve ilerleme durumunu ekranda gösterir.
4. İşlem bittiğinde, birleştirilmiş nihai `.mp4` dosyası proje klasöründe oluşturulur.

> [!NOTE]
> **Önemli Not:** İndirme işlemi bittiğinde inen videonun ismini değiştirin veya dosyayı başka bir klasöre taşıyın. Aksi takdirde, program aynı isimde başka bir dosya indirmeye çalıştığında üzerine yazılmasını önlemek amacıyla indirmeyi atlayabilir.

---

### Geliştirici
* **Kullanıcı Adı:** tembel teneke
