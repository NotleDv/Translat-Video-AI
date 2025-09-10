import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


from app.configs import read_json, write_json
from pydub import AudioSegment
from spleeter.separator import Separator
from app.processing_audio import leitura_wave
import torch
separator = Separator('spleeter:2stems')

def split_audio(path_audio, path_dir_audio):
    new_audios_accompaniment = []
    duracao = leitura_wave(path_audio)
    contador = 0
    start = 0
    end = 30
    
    def split (path_in, path_out, start, end, count):
        audio = AudioSegment.from_file(path_in)
        split = audio[ start*1000 : end*1000 ]
        
        new_audio = os.path.join(path_out, f'audio_{count}.wav')
        split.export(new_audio, format='wav')
        new_audios_accompaniment.append({
            "name": f'audio_{count}',
            'path': new_audio
        })
    
    #Criando pasta para guarda os audios que seram usadas para remover o accompaniment
    path_dir_audio = os.path.join(path_dir_audio, 'split_for_accompa')
    if not os.path.exists(path_dir_audio): os.mkdir(path_dir_audio)
    
    if duracao > 30 and (duracao-30) > 1:
        while(True):
            if contador == 0:
                start = 0
                end = 30
                split(path_audio, path_dir_audio, start, end, contador) 
                
            elif (duracao-end) > 30:
                start = end
                end+= 30
                split(path_audio, path_dir_audio, start, end, contador)
            
            else:
                start = end
                end = (duracao)
                split(path_audio, path_dir_audio, start, end, contador)
                break
            contador+=1
    else:
        new_audios_accompaniment.append({
            'name': f'audio_{0}',
            'path': path_audio
        })
    return new_audios_accompaniment       

def model(path_in_element, path_dir_result):
    prediction = separator.separate_to_file(path_in_element, path_dir_result)
    
def split_accompa(path_in, path_dir_audio):
    new_audios_accompaniment = split_audio(path_in, path_dir_audio)
    
    # Criando a pasta para receber as pastas com os resultados (spleeter tem como resultado uma pasta com os arquivos no seu interior)
    path_dir_result = os.path.join(path_dir_audio, 'result_accomp')
    if not os.path.exists(path_dir_result): os.mkdir(path_dir_result)
    
    #Chamada do modelo

    #Percorrendo os aúdios que foram cortados nas funções superiores
    for index, element in enumerate(new_audios_accompaniment):
        path_in_element = element['path']
        model(path_in_element, path_dir_result)
        
        path_result = os.path.join(path_dir_result, element['name'], 'accompaniment.wav')
        new_audios_accompaniment[index]['path_accompaniment'] = path_result
        
        os.remove(element['path'])
    
    return new_audios_accompaniment

def join_accompa (path_in, path_dir_audio):
    path_audios_accompaniment = split_accompa(path_in, path_dir_audio)
    audios = AudioSegment.from_file(path_audios_accompaniment[0]['path_accompaniment'])
    
    for i in path_audios_accompaniment[1:]:
        path = i['path_accompaniment']
        audio = AudioSegment.from_file(path)
        audios = audios.overlay(audio)
    
    result = os.path.join(path_dir_audio, 'accompaniment.wav' )
    audios.export(result, format='wav')
    
    return result
    
def main(path_log:str):
    
    log = read_json(path_log)
    
    audio = log[0]['path_audio_video']
    path_audio_dir = log[0]['path_dir_audio']
    
    path_instrumental = join_accompa(audio, path_audio_dir)
    
    log[0]['path_accompaniment'] = path_instrumental
    
    write_json(path_log, log)    