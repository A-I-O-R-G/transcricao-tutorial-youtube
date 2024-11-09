import os
import whisper
import requests
from pytube import YouTube
from pydub import AudioSegment
from fpdf import FPDF

class PDFGenerator:
    def __init__(self, title):
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Arial", style='B', size=16)
        self.pdf.cell(0, 10, title, ln=True, align='C')
        self.pdf.set_font("Arial", size=12)

    def add_text(self, text):
        self.pdf.multi_cell(0, 10, txt=text)

    def save(self, filename):
        self.pdf.output(filename)


def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file_path = audio_stream.download(filename_prefix='audio_', output_path='.')
    return audio_file_path


def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # Use the model you need (base, small, medium or large)
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)  # Prepare the audio for the model
    result = model.transcribe(audio)
    return result['text']


def main():
    youtube_url = input("Digite a URL do vídeo do YouTube: ")  # Solicita ao usuário a URL do vídeo
    pdf_title = "Transcrição do Tutorial do YouTube"
    pdf_filename = "Transcricao_Tutorial_YouTube.pdf"

    # Passo 1: Baixar o áudio do vídeo
    audio_path = download_audio(youtube_url)
    
    # Passo 2: Transcrever o áudio
    transcription = transcribe_audio(audio_path)
    
    # Passo 3: Criar o PDF
    pdf = PDFGenerator(title=pdf_title)
    pdf.add_text(transcription)
    
    # Passo 4: Salvar o PDF
    pdf.save(pdf_filename)
    
    # Remover o arquivo de áudio após a transcrição
    os.remove(audio_path)
    
    print(f"PDF '{pdf_filename}' gerado com sucesso!")


if __name__ == '__main__':
    main()