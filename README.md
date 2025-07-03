# Görüntü Şifreleme ve Şifre Çözme Aracı

![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)

Bu proje, gri tonlamalı (grayscale) görüntüleri AES şifreleme standardını kullanarak **ECB (Electronic Codebook)** ve **CBC (Cipher Block Chaining)** modlarında şifrelemek ve çözmek için geliştirilmiş bir komut satırı aracıdır (CLI).

Projenin temel amacı, farklı blok şifreleme modlarının görseller üzerindeki etkilerini pratik olarak göstermektir. Özellikle, ECB modunun desen koruma zafiyeti ile CBC modunun bu zafiyeti nasıl ortadan kaldırdığı görsel olarak sergilenmektedir.

## ✨ Öne Çıkan Özellik: ECB vs. CBC

ECB modu, her bloğu aynı anahtarla bağımsız olarak şifreler. Bu durum, orijinal görüntüdeki desenlerin şifrelenmiş görüntüde de korunmasına neden olur. CBC modu ise her bloğu bir önceki şifreli blokla zincirleyerek bu sorunu çözer ve çok daha güvenli bir şifreleme sağlar.

| Orijinal Görüntü | ECB Modunda Şifrelenmiş | CBC Modunda Şifrelenmiş |
| :--------------: | :----------------------: | :----------------------: |
| ![Original Image](./assets/original.png) | ![ECB Encrypted](./assets/ecb_encrypted.png) | ![CBC Encrypted](./assets/cbc_encrypted.png) |

> **Analiz:** Görüldüğü gibi, ECB modunda şifrelenmiş görüntünün yapısı hala tahmin edilebilirken, CBC modunda şifrelenmiş görüntü tamamen rastgele bir gürültüye dönüşmüştür.

---

## 📂 İçindekiler

- [Özellikler](#-özellikler)
- [Gereksinimler](#-gereksinimler)
- [Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)
- [Kullanım](#-kullanım)
  - [Terminal Menüsü](#terminal-menüsü)
  - [Örnek İş Akışı](#örnek-i̇ş-akışı)
- [Teknik Detaylar](#-teknik-detaylar)
- [Dosya Adlandırma Standartları](#-dosya-adlandırma-standartları)

## 🌟 Özellikler

- **Anahtar Üretimi:** ECB ve CBC modları için 128, 192 veya 256-bit AES anahtarları ve IV (Initialization Vector) üretir.
- **ECB Modu:** Görüntüleri ECB modu ile şifreler ve çözer.
- **CBC Modu:** Görüntüleri CBC modu ile şifreler ve çözer.
- **Otomatik Doldurma (Padding):** Görüntü boyutlarını AES blok boyutu olan 16 byte'ın katı olacak şekilde otomatik olarak doldurur.
- **Kullanıcı Dostu Arayüz:** Terminal üzerinden menü tabanlı kolay bir kullanım sunar.
- **Otomatik Dosya Adlandırma:** Oluşturulan anahtar, IV ve şifreli/çözülmüş görüntü dosyalarını standart bir formata göre isimlendirir.

## ⚙️ Gereksinimler

- Python 3.7 veya daha yeni bir sürüm.
- Aşağıdaki Python kütüphaneleri:
  - `opencv-python`
  - `numpy`
  - `pycryptodome`

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

1.  **Projeyi Klonlayın:**
    ```bash
    git clone https://github.com/kullanici-adiniz/image_cipher.git
    cd image_cipher
    ```
    *Not: Yukarıdaki URL'i kendi GitHub repo URL'iniz ile güncelleyin.*

2.  **Sanal Ortam Oluşturun ve Aktif Edin (Önerilir):**
    ```bash
    # Sanal ortam oluştur
    python -m venv myenv

    # Linux / macOS
    source myenv/bin/activate

    # Windows
    myenv\Scripts\activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install opencv-python numpy pycryptodome
    ```

4.  **Betiği Çalıştırın:**
    ```bash
    python image_cipher.py
    ```

## 📋 Kullanım

### Terminal Menüsü

Betiği çalıştırdığınızda sizi aşağıdaki gibi bir menü karşılar:

![Terminal Arayüzü](./assets/terminal_interface.png)

### Örnek İş Akışı

1.  **256-bit bir CBC anahtarı ve IV oluşturun:**
    - Menüden `2`'yi seçin.
    - Anahtar boyutu olarak `256` girin.
    - `cbc_key_256.bin` ve `cbc_iv_256.bin` dosyaları oluşturulacaktır.

2.  **Bir görüntüyü bu anahtarla şifreleyin:**
    - Menüden `5`'i seçin.
    - Şifrelenecek görüntünün yolunu girin (örn: `original.png`).
    - Listeden `cbc_key_256.bin` anahtarını seçin.
    - `original_cbc_256_encrypted.png` adında şifreli bir görüntü oluşturulacaktır.

3.  **Şifrelenmiş görüntüyü çözün:**
    - Menüden `7`'yi seçin.
    - Şifresi çözülecek görüntünün yolunu girin (`original_cbc_256_encrypted.png`).
    - Listeden ilgili anahtarı (`cbc_key_256.bin`) seçin.
    - `original_cbc_256_encrypted_cbc_256_decrypted.png` adında, orijinal görüntünün aynısı olan bir dosya oluşturulacaktır.

## 🛠️ Teknik Detaylar

- **AES (Advanced Encryption Standard):** 128, 192 veya 256 bit anahtar uzunluklarını destekleyen simetrik bir blok şifreleme algoritmasıdır.
- **ECB (Electronic Codebook):** En basit şifreleme modudur. Her bloğu bağımsız olarak şifreler. Bu nedenle, aynı içeriğe sahip bloklar aynı şifreli metni üretir ve desenleri korur.
- **CBC (Cipher Block Chaining):** Her düz metin bloğunu şifrelemeden önce bir önceki şifreli metin bloğu ile XOR işlemine tabi tutar. Bu, aynı içeriğe sahip blokların farklı şifreli metinler üretmesini sağlar ve desenleri gizler.
- **IV (Initialization Vector):** CBC modunda ilk bloğu şifrelemek için kullanılan rastgele bir değerdir. Tekrar saldırılarını (replay attacks) önlemeye yardımcı olur.

## 📁 Dosya Adlandırma Standartları

Betik, karışıklığı önlemek için oluşturulan dosyaları aşağıdaki standartlara göre adlandırır:

- **Anahtar Dosyaları:**
  - ECB Anahtarı: `ecb_key_[bit_boyutu].bin` (örn: `ecb_key_128.bin`)
  - CBC Anahtarı: `cbc_key_[bit_boyutu].bin` (örn: `cbc_key_256.bin`)
  - CBC IV: `cbc_iv_[bit_boyutu].bin` (örn: `cbc_iv_256.bin`)

- **Şifreli Görüntüler:**
  - `[orijinal_ad]_[mod]_[bit_boyutu]_encrypted.png` (örn: `logo_cbc_128_encrypted.png`)

- **Çözülmüş Görüntüler:**
  - `[şifreli_ad]_[mod]_[bit_boyutu]_decrypted.png` (örn: `logo_cbc_128_encrypted_cbc_128_decrypted.png`)
