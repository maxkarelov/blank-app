import streamlit as st
import subprocess
import tempfile
import os

st.title("Видео-конвертер с использованием ffmpeg")

# Выбор файла и параметров
input_file = st.file_uploader("Загрузите видео для конвертации", type=["mp4", "mov", "avi"])
output_format = st.selectbox("Выберите выходной формат", ["mp4", "avi", "mov"])
bitrate = st.slider("Выберите битрейт (кбит/с)", 500, 5000, 1500)
width = st.number_input("Ширина кадра", min_value=100, max_value=1920, value=1280)
height = st.number_input("Высота кадра", min_value=100, max_value=1080, value=720)

# Кнопка для запуска конвертации
if st.button("Конвертировать"):
    if input_file:
        with tempfile.NamedTemporaryFile(delete=False) as temp_input:
            temp_input.write(input_file.read())
            temp_input_path = temp_input.name

        output_file = f"output.{output_format}"
        output_path = os.path.join(tempfile.gettempdir(), output_file)

        with st.spinner("Конвертация..."):
            command = [
                "ffmpeg", "-i", temp_input_path, "-vf", f"scale={width}:{height}",
                "-b:v", f"{bitrate}k", output_path
            ]
            process = subprocess.run(command, capture_output=True, text=True)

            if process.returncode == 0:
                st.success("Видео успешно конвертировано!")
                with open(output_path, "rb") as file:
                    st.download_button("Скачать результат", file, output_file)
            else:
                st.error("Произошла ошибка при конвертации видео.")
                st.text(process.stderr)

        # Удаление временного входного файла
        os.remove(temp_input_path)
    else:
        st.error("Пожалуйста, загрузите файл для конвертации.")
