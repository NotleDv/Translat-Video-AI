import ffmpeg, imageio_ffmpeg
from app.configs import read_json, write_json
import os
from pydub import AudioSegment
import wave 

def leitura_wave (path:str, condicional:bool = False) -> str:
    # O intuito do parâmetro 'condicional' é apenas para retornar o rate
    with wave.open(path, 'rb') as wave_file:
        frames = wave_file.getnframes() # q_frames
        rate = wave_file.getframerate() # taxa de amostragem
        duration = frames / float(rate)    

        if condicional:
            return duration, rate
        
        return duration

def inserte_audio (path_dir_audio: str, path_out_dir: str, path_video:str, name_video:str, audio_f:str, path_instrumental:str) -> str:
    
    #Import dos áudios
    vocal = AudioSegment.from_file(audio_f)
    instrumental = AudioSegment.from_file(path_instrumental)
    vocal_instr = os.path.join(path_dir_audio, "audio_final.wav")
    
    #Criando um áudio com o vocal e instrumental juntos
    output = vocal.overlay(instrumental)
    output.export(vocal_instr, format="wav")
    
    
    #Verando o áudio final
    path_f = os.path.join(path_out_dir, f'(Dublado) {name_video}')

    video = ffmpeg.input(path_video)
    audio = ffmpeg.input(vocal_instr)
    
    
    ffmpeg.output(video.video, audio.audio, path_f, vcodec='copy').run( quiet = True)
    
    return path_f

                
def main(path_log:str, path_video:str, dir_:str):
    log = read_json(path_log)
    
    path_video = path_video
    path_dir_audio = log[0]['path_dir_audio']
    name_video = log[0]['name_video']
    audio_f = log[0]['audio_concatenado']
    #audio = log[0]['path_audio_video']
    #path_audio_dir = log[0]['path_dir_audio']
    
    path_instrumental = log[0]['path_accompaniment']
    
    
    resultado = inserte_audio(path_dir_audio = path_dir_audio,
                                                path_out_dir =dir_,
                                                path_video = path_video,
                                                name_video = name_video, 
                                                audio_f = audio_f, 
                                                path_instrumental = path_instrumental)
    
    return resultado
    
# def inserte_audio (path_dir_audio: str, path_out_dir: str, path_video:str, name_video:str, audio_f:str):
    
#     #Import dos áudios
#     vocal = AudioSegment.from_file(audio_f)
#     vocal_instr = os.path.join(path_dir_audio, "audio_final.wav")
    
#     #Criando um áudio com o vocal e instrumental juntos
#     vocal.export(vocal_instr, format="wav")    
    
#     #Verando o áudio final
#     path_f = os.path.join(path_out_dir, f'(Dublado) {name_video}')

#     video = ffmpeg.input(path_video)
#     audio = ffmpeg.input(vocal_instr)
    
    
#     ffmpeg.output(video.video, audio.audio, path_f, vcodec='copy').run( quiet = True)
    
#     return path_f