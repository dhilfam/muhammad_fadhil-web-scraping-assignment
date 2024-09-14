import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Variabel yang akan menampung hasil scraping
hasil_scrapping = [] 

# Parameter yang dapat diubah
file_path = "pajak_2018_6.csv" # NAMA FILE DENGAN FORMAT PAJAK_[TAHUN]_PAGE
daftar_halaman = range(6, 7) # TOTAL HALAMAN YANG INGIN DI SCRAPING, RANGE SELALU +1
base_link = "https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pajak-2/tahunjenis/putus/tahun/2018/page/"
base_link2 = ".html"

# Setiap halaman, kita akan menampung elemen yang diperlukan 
for halaman in daftar_halaman:
    # Membuat browser baru
    driver = webdriver.Chrome()

    # Mengakses halaman tersebut
    driver.get(base_link + str(halaman) + base_link2) 

    # Jumlah Konten yang akan diambil per halamannya
    for angka in range(1, 21):
        daftar_link = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/div[2]/div[1]/div/div/div[1]/div[1]/div[" + str(angka) + "]/div/strong/a")
        daftar_link.click()

        # Menunggu untuk memastikan halaman telah dimuat sepenuhnya, sering dipakai untuk mengatasi durasi loading
        time.sleep(3)

        # Mencari berbagai informasi
        judul = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[1]/td/h2") 
        nomor = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[2]/td[2]")
        tingkatproses = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[3]/td[2]")
        klasifikasi = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[4]/td[2]/a[2]")
        tahun = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[6]/td[2]")
        amar = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[13]/td[2]")
        amarlainnya = driver.find_element(By.XPATH, "/html/body/div[1]/section[2]/div/div/section/div/div/div[1]/div/div/div/div[1]/div/ul/table/tbody/tr[14]/td[2]")

        # Menyimpan data dalam format dictionary
        data_baru = {
            "Judul": judul.text,
            "Nomor": nomor.text,
            "Tingkat proses": tingkatproses.text,
            "Klasifikasi": klasifikasi.text,
            "Tahun": tahun.text,
            "Amar": amar.text,
            "Amar Lainnya atau catatan": amarlainnya.text
        }

        # Menambahkan data ke dalam list hasil_scrapping
        hasil_scrapping.append(data_baru)

        # Kembali ke halaman sebelumnya
        driver.back()

    # Menghentikan scrapping/browser virtual
    driver.quit()

# Menyimpan hasil ke dalam file CSV
with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Judul", "Nomor", "Tingkat proses", "Klasifikasi", "Tahun", "Amar", "Amar Lainnya atau catatan"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for data in hasil_scrapping:
        writer.writerow(data)