import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import math
import requests
import json
import os

# Konstanta gas ideal (J/mol·K)
R = 8.314

# --- FUNGSI KALKULATOR PROSES TERMODINAMIKA ---

def calculate_isobaric():
    """Menghitung proses Isobarik."""
    print("\n--- Kalkulator Proses Isobarik (Tekanan Konstan) ---")
    try:
        p = float(input("Masukkan Tekanan (p) dalam Pascal: "))
        v1 = float(input("Masukkan Volume Awal (V₁) dalam m³: "))
        v2 = float(input("Masukkan Volume Akhir (V₂) dalam m³: "))
        n = float(input("Masukkan Jumlah mol (n): "))
        t1 = float(input("Masukkan Suhu Awal (T₁) dalam Kelvin: "))
        t2 = float(input("Masukkan Suhu Akhir (T₂) dalam Kelvin: "))

        delta_v = v2 - v1
        delta_t = t2 - t1
        
        # W = p * ΔV
        work = p * delta_v
        # ΔU = 3/2 * n * R * ΔT (untuk gas monoatomik)
        delta_u = 1.5 * n * R * delta_t
        # Q = W + ΔU
        heat = work + delta_u

        print("\n--- Hasil Perhitungan ---")
        print(f"Usaha (W)                : {work:.4f} J")
        print(f"Perubahan Energi Dalam (ΔU): {delta_u:.4f} J")
        print(f"Kalor (Q)                : {heat:.4f} J")

    except ValueError:
        print("\nError: Masukan tidak valid. Harap masukkan angka.")
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")

def calculate_isochoric():
    """Menghitung proses Isokhorik."""
    print("\n--- Kalkulator Proses Isokhorik (Volume Konstan) ---")
    try:
        n = float(input("Masukkan Jumlah mol (n): "))
        t1 = float(input("Masukkan Suhu Awal (T₁) dalam Kelvin: "))
        t2 = float(input("Masukkan Suhu Akhir (T₂) dalam Kelvin: "))

        delta_t = t2 - t1
        
        # W = 0
        work = 0
        # ΔU = 3/2 * n * R * ΔT (untuk gas monoatomik)
        delta_u = 1.5 * n * R * delta_t
        # Q = ΔU
        heat = delta_u

        print("\n--- Hasil Perhitungan ---")
        print(f"Usaha (W)                : {work:.4f} J")
        print(f"Perubahan Energi Dalam (ΔU): {delta_u:.4f} J")
        print(f"Kalor (Q)                : {heat:.4f} J")

    except ValueError:
        print("\nError: Masukan tidak valid. Harap masukkan angka.")
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")

def calculate_isothermal():
    """Menghitung proses Isotermal."""
    print("\n--- Kalkulator Proses Isotermal (Suhu Konstan) ---")
    try:
        n = float(input("Masukkan Jumlah mol (n): "))
        t = float(input("Masukkan Suhu (T) dalam Kelvin: "))
        v1 = float(input("Masukkan Volume Awal (V₁) dalam m³: "))
        v2 = float(input("Masukkan Volume Akhir (V₂) dalam m³: "))

        if v1 <= 0 or v2 <= 0:
            print("\nError: Volume harus bernilai positif.")
            return
            
        # W = n * R * T * ln(V₂/V₁)
        work = n * R * t * math.log(v2 / v1)
        # ΔU = 0
        delta_u = 0
        # Q = W
        heat = work

        print("\n--- Hasil Perhitungan ---")
        print(f"Usaha (W)                : {work:.4f} J")
        print(f"Perubahan Energi Dalam (ΔU): {delta_u:.4f} J")
        print(f"Kalor (Q)                : {heat:.4f} J")

    except ValueError:
        print("\nError: Masukan tidak valid. Harap masukkan angka.")
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")

# --- FUNGSI KONVERTER SATUAN ---

def convert_temperature():
    """Melakukan konversi antar satuan suhu."""
    print("\n--- Konverter Suhu ---")
    try:
        val = float(input("Masukkan nilai suhu: "))
        unit = input("Masukkan satuan awal (C, F, atau K): ").upper()

        if unit == 'C':
            c = val
            f = (c * 9/5) + 32
            k = c + 273.15
        elif unit == 'F':
            f = val
            c = (f - 32) * 5/9
            k = c + 273.15
        elif unit == 'K':
            k = val
            c = k - 273.15
            f = (c * 9/5) + 32
        else:
            print("Satuan tidak valid. Harap pilih 'C', 'F', atau 'K'.")
            return
            
        print("\n--- Hasil Konversi ---")
        print(f"{c:.2f} °C")
        print(f"{f:.2f} °F")
        print(f"{k:.2f} K")

    except ValueError:
        print("\nError: Masukan tidak valid. Harap masukkan angka.")

def convert_pressure():
    """Melakukan konversi antar satuan tekanan."""
    print("\n--- Konverter Tekanan ---")
    try:
        val = float(input("Masukkan nilai tekanan: "))
        unit = input("Masukkan satuan awal (atm, mmhg, pa): ").lower()

        if unit == 'atm':
            atm = val
            mmhg = atm * 760
            pa = atm * 101325
        elif unit == 'mmhg':
            mmhg = val
            atm = mmhg / 760
            pa = mmhg * 133.322
        elif unit == 'pa':
            pa = val
            atm = pa / 101325
            mmhg = pa / 133.322
        else:
            print("Satuan tidak valid. Harap pilih 'atm', 'mmhg', atau 'pa'.")
            return

        print("\n--- Hasil Konversi ---")
        print(f"{atm:.5f} atm")
        print(f"{mmhg:.2f} mmHg")
        print(f"{pa:.2f} Pa")

    except ValueError:
        print("\nError: Masukan tidak valid. Harap masukkan angka.")

# --- FUNGSI INTERAKSI DENGAN GEMINI AI ---

def ask_gemini_ai():
    """Mengirim prompt ke Gemini API dan menampilkan hasilnya."""
    print("\n--- Tanya Konsep Termodinamika pada AI ---")
    user_prompt = input("Ketik konsep yang ingin ditanyakan: ")
    if not user_prompt:
        print("Pertanyaan tidak boleh kosong.")
        return

    # Anda bisa menyimpan API Key di environment variable untuk keamanan
    # api_key = os.getenv("GEMINI_API_KEY")
    api_key = "" # Kunci API akan ditangani oleh lingkungan saat dijalankan
    
    if not api_key:
        print("Peringatan: API Key tidak ditemukan.")
        # Lanjutkan tanpa API Key, karena lingkungan mungkin akan menyediakannya
        
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    full_prompt = f"Jelaskan konsep termodinamika berikut dalam Bahasa Indonesia dengan sederhana, jelas, dan ringkas untuk pemula: \"{user_prompt}\""
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": full_prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    print("\nMemproses permintaan Anda...")
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Akan error jika status code bukan 2xx
        
        result = response.json()
        
        text = result['candidates'][0]['content']['parts'][0]['text']
        
        print("\n--- Jawaban AI ---")
        print(text)
        
    except requests.exceptions.RequestException as e:
        print(f"\nError: Gagal menghubungi API. Periksa koneksi internet Anda. ({e})")
    except (KeyError, IndexError):
        print("\nError: Respons dari API tidak dalam format yang diharapkan.")
    except Exception as e:
        print(f"\nTerjadi kesalahan tak terduga: {e}")


# --- FUNGSI UTAMA (MAIN MENU) ---

def main_menu():
    """Menampilkan menu utama dan mengarahkan ke fungsi yang sesuai."""
    while True:
        print("\n========================================")
        print("   Utilitas Termodinamika Cerdas (CLI)")
        print("========================================")
        print("1. Kalkulator Proses Termodinamika")
        print("2. Konverter Satuan")
        print("3. Tanya Konsep pada AI")
        print("4. Keluar")
        
        choice = input("Pilih menu (1-4): ")
        
        if choice == '1':
            print("\n--- Pilih Proses ---")
            print("a. Isobarik")
            print("b. Isokhorik")
            print("c. Isotermal")
            proc_choice = input("Pilih proses (a/b/c): ").lower()
            if proc_choice == 'a':
                calculate_isobaric()
            elif proc_choice == 'b':
                calculate_isochoric()
            elif proc_choice == 'c':
                calculate_isothermal()
            else:
                print("Pilihan tidak valid.")
        elif choice == '2':
            print("\n--- Pilih Konversi ---")
            print("a. Suhu")
            print("b. Tekanan")
            conv_choice = input("Pilih konversi (a/b): ").lower()
            if conv_choice == 'a':
                convert_temperature()
            elif conv_choice == 'b':
                convert_pressure()
            else:
                print("Pilihan tidak valid.")
        elif choice == '3':
            ask_gemini_ai()
        elif choice == '4':
            print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Silakan masukkan angka dari 1 sampai 4.")
        
        input("\nTekan Enter untuk kembali ke menu utama...")

if __name__ == "__main__":
    main_menu()

