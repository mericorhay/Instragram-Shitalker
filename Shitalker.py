import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def selenium():
    try:
        gidilecekadres = entry.get()

        ayarlar = webdriver.ChromeOptions()
        ayarlar.add_argument("--disable-blink-features=AutomationControlled")
        ayarlar.add_argument("--disable-extensions")
        ayarlar.add_argument("--disable-gpu")
        ayarlar.add_argument("--no-sandbox")
        ayarlar.add_experimental_option("detach", True)

        sürücü = webdriver.Chrome(options=ayarlar)
        sürücü.maximize_window()
        sürücü.get("https://www.instagram.com/")
        time.sleep(30)  # Instagram'ın yüklenmesi için bekliyoruz
        sürücü.get(gidilecekadres)
        time.sleep(5)   # Sayfa geçişinin tamamlanması için bekliyoruz

        # Takipçi listesinin üzerine tıklıyoruz
        sürücü.find_element(By.XPATH, "//ul/li[3]/div/a").click()
        time.sleep(4)

        # Scroll yapılabilir alanı seçiyoruz
        scroll_box = sürücü.find_element(By.CSS_SELECTOR, '.xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x1lliihq.x1iyjqo2.xs83m0k.xz65tgg.x1rife3k.x1n2onr6')

        start_time = time.time()  # Başlangıç zamanını alıyoruz
        duration = 90  # 1.5 dakika = 90 saniye

        while time.time() - start_time < duration:  # 1.5 dakika boyunca kaydırma
            sürücü.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", scroll_box)
            time.sleep(3)  # Yavaşça scroll yapıyoruz

        # Takipçileri alıyoruz
        followers = sürücü.find_elements(By.CSS_SELECTOR, '._ap3a._aaco._aacw._aacx._aad7._aade')

        # Takipçileri bir listeye kaydediyoruz
        follower_list = [follower.text for follower in followers]

        # CSV dosyasına yazdırma
        df = pd.DataFrame(follower_list, columns=["Followers"])
        df.to_csv("followers.csv", index=False)

        messagebox.showinfo("Başarılı", "Takip Ettikleri Listesi başarıyla CSV dosyasına kaydedildi!")

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

# GUI oluşturma
root = tk.Tk()
root.title("MERICH SHITALKER")
root.geometry("500x250")  # Pencere boyutunu ayarlıyoruz
root.config(bg="#f4f4f4")  # Arka plan rengini değiştirme

# Etiket stilini özelleştir
label = tk.Label(root, text="Instagram Profil URL'si:", font=("Arial", 12), bg="#f2f2d2")
label.grid(row=0, column=0, padx=20, pady=10)

# Giriş kutusu stilini özelleştir
entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.grid(row=1, column=0, padx=20, pady=10)

# Buton stilini özelleştir
button = tk.Button(root, text="Takipçileri Çek ve CSV'ye Kaydet", command=selenium,
                   bg="#4CAF50", fg="white", font=("Arial", 12), relief="flat", padx=20, pady=10)
button.grid(row=2, column=0, pady=20)

# GUI'yi çalıştırma
root.mainloop()
