import streamlit as st
import math
import requests
import json
import os

# Konstanta gas ideal (J/mol·K)
R = 8.314

# --- FUNGSI KALKULATOR PROSES TERMODINAMIKA (DIADAPTASI UNTUK STREAMLIT) ---

def calculate_isobaric_streamlit():
    st.header("Kalkulator Proses Isobarik (Tekanan Konstan)")

    # Menggunakan widget Streamlit untuk input
    p = st.number_input("Masukkan Tekanan (p) dalam Pascal:", min_value=0.0, format="%.2f")
    v1 = st.number_input("Masukkan Volume Awal (V₁) dalam m³:", min_value=0.0, format="%.2f")
    v2 = st.number_input("Masukkan Volume Akhir (V₂) dalam m³:", min_value=0.0, format="%.2f")
    n = st.number_input("Masukkan Jumlah mol (n):", min_value=0.0, format="%.2f")
    t1 = st.number_input("Masukkan Suhu Awal (T₁) dalam Kelvin:", min_value=0.0, format="%.2f")
    t2 = st.number_input("Masukkan Suhu Akhir (T₂) dalam Kelvin:", min_value=0.0, format="%.2f")

    # Tombol untuk memicu perhitungan
    if st.button("Hitung Isobarik"):
        try:
            if v1 <= 0 or v2 <= 0 or n <= 0 or t1 <= 0 or t2 <= 0:
                st.error("Semua nilai input harus positif. Harap periksa kembali masukan Anda.")
            else:
                delta_v = v2 - v1
                delta_t = t2 - t1
                
                # W = p * ΔV
                work = p * delta_v
                # ΔU = 3/2 * n * R * ΔT (untuk gas monoatomik)
                delta_u = 1.5 * n * R * delta_t
                # Q = W + ΔU
                heat = work + delta_u

                st.subheader("Hasil Perhitungan")
                st.info(f"**Usaha (W)**: {work:.4f} J")
                st.info(f"**Perubahan Energi Dalam (ΔU)**: {delta_u:.4f} J")
                st.info(f"**Kalor (Q)**: {heat:.4f} J")

        except ValueError:
            st.error("Masukan tidak valid. Harap masukkan angka.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

def calculate_isochoric_streamlit():
    st.header("Kalkulator Proses Isokhorik (Volume Konstan)")
    
    n = st.number_input("Masukkan Jumlah mol (n):", min_value=0.0, key="isochoric_n", format="%.2f")
    t1 = st.number_input("Masukkan Suhu Awal (T₁) dalam Kelvin:", min_value=0.0, key="isochoric_t1", format="%.2f")
    t2 = st.number_input("Masukkan Suhu Akhir (T₂) dalam Kelvin:", min_value=0.0, key="isochoric_t2", format="%.2f")

    if st.button("Hitung Isokhorik"):
        try:
            if n <= 0 or t1 <= 0 or t2 <= 0:
                st.error("Semua nilai input harus positif. Harap periksa kembali masukan Anda.")
            else:
                delta_t = t2 - t1
                work = 0 # W = 0 untuk isokhorik
                delta_u = 1.5 * n * R * delta_t
                heat = delta_u

                st.subheader("Hasil Perhitungan")
                st.info(f"**Usaha (W)**: {work:.4f} J")
                st.info(f"**Perubahan Energi Dalam (ΔU)**: {delta_u:.4f} J")
                st.info(f"**Kalor (Q)**: {heat:.4f} J")
        except ValueError:
            st.error("Masukan tidak valid. Harap masukkan angka.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

def calculate_isothermal_streamlit():
    st.header("Kalkulator Proses Isotermal (Suhu Konstan)")
    
    n = st.number_input("Masukkan Jumlah mol (n):", min_value=0.0, key="isothermal_n", format="%.2f")
    t = st.number_input("Masukkan Suhu (T) dalam Kelvin:", min_value=0.0, key="isothermal_t", format="%.2f")
    v1 = st.number_input("Masukkan Volume Awal (V₁) dalam m³:", min_value=0.0, key="isothermal_v1", format="%.2f")
    v2 = st.number_input("Masukkan Volume Akhir (V₂) dalam m³:", min_value=0.0, key="isothermal_v2", format="%.2f")

    if st.button("Hitung Isotermal"):
        try:
            if v1 <= 0 or v2 <= 0 or n <= 0 or t <= 0:
                st.error("Semua nilai input harus positif. Harap periksa kembali masukan Anda.")
            else:
                work = n * R * t * math.log(v2 / v1)
                delta_u = 0 # ΔU = 0 untuk isotermal pada gas ideal
                heat = work

                st.subheader("Hasil Perhitungan")
                st.info(f"**Usaha (W)**: {work:.4f} J")
                st.info(f"**Perubahan Energi Dalam (ΔU)**: {delta_u:.4f} J")
                st.info(f"**Kalor (Q)**: {heat:.4f} J")
        except ValueError:
            st.error("Masukan tidak valid. Harap masukkan angka.")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# --- FUNGSI KONVERTER SATUAN (DIADAPTASI UNTUK STREAMLIT) ---

def convert_temperature_streamlit():
    st.header("Konverter Suhu")
    
    col1, col2 = st.columns(2)
    with col1:
        val = st.number_input("Masukkan nilai suhu:", format="%.2f", key="temp_val")
    with col2:
        unit = st.selectbox("Pilih satuan awal:", ('Celsius', 'Fahrenheit', 'Kelvin'), key="temp_unit")
    
    c, f, k = None, None, None

    if unit == 'Celsius':
        c = val
        f = (c * 9/5) + 32
        k = c + 273.15
    elif unit == 'Fahrenheit':
        f = val
        c = (f - 32) * 5/9
        k = c + 273.15
    elif unit == 'Kelvin':
        k = val
        c = k - 273.15
        f = (c * 9/5) + 32
    
    st.subheader("Hasil Konversi")
    st.write(f"**{c:.2f} °C**")
    st.write(f"**{f:.2f} °F**")
    st.write(f"**{k:.2f} K**")


def convert_pressure_streamlit():
    st.header("Konverter Tekanan")

    col1, col2 = st.columns(2)
    with col1:
        val = st.number_input("Masukkan nilai tekanan:", format="%.2f", key="pressure_val")
    with col2:
        unit = st.selectbox("Pilih satuan awal:", ('atm', 'mmHg', 'Pa'), key="pressure_unit").lower()

    atm, mmhg, pa = None, None, None

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
    
    st.subheader("Hasil Konversi")
    st.write(f"**{atm:.5f} atm**")
    st.write(f"**{mmhg:.2f} mmHg**")
    st.write(f"**{pa:.2f} Pa**")

# --- FUNGSI INTERAKSI DENGAN GEMINI AI (DIADAPTASI UNTUK STREAMLIT) ---

def ask_gemini_ai_streamlit():
    st.header("Tanya Konsep Termodinamika pada AI")
    user_prompt = st.text_area("Ketik konsep yang ingin ditanyakan:", key="ai_prompt")

    if st.button("Tanyakan pada AI"):
        if not user_prompt:
            st.warning("Pertanyaan tidak boleh kosong.")
            return

        # Ambil API Key dari environment variable (lebih aman)
        api_key = os.getenv("GEMINI_API_KEY") # Pastikan Anda telah mengatur ini di lingkungan Anda
        
        if not api_key:
            st.error("Kesalahan: API Key Gemini tidak ditemukan. Harap atur environment variable 'GEMINI_API_KEY'.")
            st.info("Anda bisa mendapatkan API Key dari Google AI Studio: https://aistudio.google.com/")
            return
            
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        full_prompt = f"Jelaskan konsep termodinamika berikut dalam Bahasa Indonesia dengan sederhana, jelas, dan ringkas untuk pemula: \"{user_prompt}\""
        
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": full_prompt}]
            }]
        }
        
        headers = {"Content-Type": "application/json"}
        
        with st.spinner("Memproses permintaan Anda..."):
            try:
                response = requests.post(api_url, headers=headers, data=json.dumps(payload))
                response.raise_for_status() # Akan error jika status code bukan 2xx
                
                result = response.json()
                
                text = result['candidates'][0]['content']['parts'][0]['text']
                
                st.subheader("Jawaban AI")
                st.write(text)
                
            except requests.exceptions.RequestException as e:
                st.error(f"Error: Gagal menghubungi API. Periksa koneksi internet Anda atau status API. ({e})")
            except (KeyError, IndexError):
                st.error("Error: Respons dari API tidak dalam format yang diharapkan.")
            except Exception as e:
                st.error(f"Terjadi kesalahan tak terduga: {e}")


# --- FUNGSI UTAMA UNTUK STREAMLIT ---

def main():
    st.set_page_config(page_title="Utilitas Termodinamika Cerdas", layout="centered")

    st.title("🌡️ Utilitas Termodinamika Cerdas")
    st.markdown("Aplikasi ini membantu Anda melakukan perhitungan termodinamika dasar, konversi satuan, dan bertanya konsep pada AI.")

    # Menggunakan st.sidebar untuk menu navigasi
    st.sidebar.title("Navigasi")
    menu_choice = st.sidebar.radio(
        "Pilih Menu:",
        ("Kalkulator Proses Termodinamika", "Konverter Satuan", "Tanya Konsep pada AI")
    )

    if menu_choice == "Kalkulator Proses Termodinamika":
        st.sidebar.subheader("Pilih Proses")
        process_choice = st.sidebar.radio(
            "Pilih proses:",
            ("Isobarik", "Isokhorik", "Isotermal")
        )
        if process_choice == "Isobarik":
            calculate_isobaric_streamlit()
        elif process_choice == "Isokhorik":
            calculate_isochoric_streamlit()
        elif process_choice == "Isotermal":
            calculate_isothermal_streamlit()

    elif menu_choice == "Konverter Satuan":
        st.sidebar.subheader("Pilih Konversi")
        convert_choice = st.sidebar.radio(
            "Pilih konversi:",
            ("Suhu", "Tekanan")
        )
        if convert_choice == "Suhu":
            convert_temperature_streamlit()
        elif convert_choice == "Tekanan":
            convert_pressure_streamlit()

    elif menu_choice == "Tanya Konsep pada AI":
        ask_gemini_ai_streamlit()

    st.sidebar.markdown("---")
    st.sidebar.info("Dibuat dengan ❤️ untuk memahami Termodinamika AUUUUUAHHH.")
    
if __name__ == "__main__":
    main()
