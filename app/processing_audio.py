from app.configs import read_json, write_json
import os
from pydub import AudioSegment, effects
import wave
import librosa
import pyrubberband as pyrb

import soundfile as sf

def leitura_wave (path:str, condicional:bool = False) -> str:
    # O intuito do parâmetro 'condicional' é apenas para retornar o rate
    with wave.open(path, 'rb') as wave_file:
        frames = wave_file.getnframes() # q_frames
        rate = wave_file.getframerate() # taxa de amostragem
        duration = frames / float(rate)    

        if condicional:
            return duration, rate
        
        return duration

def duracao_origem_X_gerado(log:list) -> list:
    #Capturando a duração do áudio original e do áudio gerado
    for index, i in enumerate(log[1]):
        duracao_audios = 0
        
        for path in i['path_audios_gerados']:
            for key, item in path.items():
                duracao_audios += leitura_wave(item)

        log[1][index]['duracao_audio_gerado'] = round(float(duracao_audios), 2)
        log[1][index]['duracao_audio_original'] = round(float(i['end'] - i['start']), 2)
        
    return log

def concatenacao_audios (log:list) -> list:
    path_dir_audios_gerados = log[0]['path_dir_audio_generator']
    
    #Concatenação dos textos que tem mais de um áudio gerado
    for index, i in enumerate(log[1]):
        q_audios = len(i['path_audios_gerados'])
        
        if q_audios > 1:
            name = []
            concatenacao_audios = AudioSegment.empty()
            
            #Create Audio_Segments dinâmico
            for _, k in enumerate(i['path_audios_gerados']):
                
                name.append(list(k.keys()))
                path_audio_atual = list(k.items())[0]
                
                concatenacao_audios += AudioSegment.from_file(path_audio_atual[1])
                os.remove(path_audio_atual[1])
                
            path_f = os.path.join(path_dir_audios_gerados, 'audio'+ name[0][0][6:] + '.wav')
            concatenacao_audios.export(path_f, format='wav')
            
            
            log[1][index]['path_audios_gerados'] = [{name[0][0]: path_f}]
    
    return log

def concatenacao_final (log:list) -> list:
    path_dir_audios = log[0]['path_dir_audio']
    
    #Calculando duração total do áudio
    duracao_total_audio = ((log[1][-1]['end'] - log[1][-1]['start']) - log[1][-1]['duracao_audio_gerado']) + log[1][-1]['end']
    
    #Inicializando 
    audio = AudioSegment.empty()
    base = AudioSegment.silent(duration= int(duracao_total_audio * 1000))
    
    result = ''
    
    #Concatenando todos os áudios para gerar o áudio final
    for index, lista in enumerate(log[1]):
        time_start = int(lista['start'] * 1000)
        time_end = int(lista['end'] * 1000)
        
        duracao_audio_original = time_end - time_start
        
        
        for _, item in enumerate(lista['path_audios_gerados']):
            path_audio_gerado = list(item.items())[0][1]
            duracao_audio_gerado, rate_audio_gerado = leitura_wave(path_audio_gerado, True)
            duracao_audio_gerado = duracao_audio_gerado * 1000
            
            fator_velocidade = ( duracao_audio_gerado/ duracao_audio_original)
            #new_frame_rate = int(rate_audio_gerado * fator_velocidade)
            if fator_velocidade > 2:
                fator_velocidade = 2
            if fator_velocidade < 1:
                fator_velocidade = 1
                
            #Import audio + Config new_frame_rate
            audio_load, sr = librosa.load(path_audio_gerado)
            audio_fast = pyrb.time_stretch(audio_load, sr, rate= fator_velocidade)
            #audio_fast = pyrb.time_stretch(audio_load, sr, rate=1)
            sf.write(path_audio_gerado, audio_fast, sr)
            
            
            audio = audio.from_file(path_audio_gerado)
            audio = effects.normalize(audio)
            #audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
            #audio = audio.set_frame_rate(new_frame_rate)
            
            if index == 0:
                result = base.overlay(audio, position=time_start)
            
            result = result.overlay(audio, position=time_start)
            
        

        path_f = os.path.join(path_dir_audios, 'resultado.wav')
        result.export(path_f, format='wav')
        
        log[0]['audio_concatenado'] = path_f
    return log

def main(path_log:str):
    log = read_json(path_log)
    
    
    result = concatenacao_audios(log)
    
    result = duracao_origem_X_gerado(log)
    
    result = concatenacao_final(log)
    
    
    write_json(path_log, result)
    
    