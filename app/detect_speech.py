import torch
import math
from app.configs import torch_config, read_json, write_json
import os
import sys 

def model(token:str) -> list:
    from pyannote.audio import Pipeline
    device_ = torch_config()
    
    model = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=token)
    
    model.to(torch.device(device_))
    
    return model

def aproximacao (lista:list) -> list:
    ## -- Redução de Dimensionalidade
    list_time_speaker_reduzido = []
    i = 0

    while i < len(lista):
        start = lista[i]['start']
        end = lista[i]['end']
        a = i

        while a + 1 < len(lista) and math.isclose(end, lista[a+1]['start'], abs_tol=1.2):
            end = lista[a+1]['end']  # atualiza o fim
            a += 1  # avança para o próximo

        # Adiciona o intervalo unido
        list_time_speaker_reduzido.append({'start':start, 'end': end})
        i = a + 1  # pula para o próximo intervalo que não foi unido
    
    return list_time_speaker_reduzido

## Mudeii
def timer_speaks (model, path:str) -> list:
    list_time_speaker = []
    
    result = model(path)
    
    ## -- Tratamento dos dados brutos no modelo
    for speaker, _, id_speaker in result.itertracks(yield_label=True):
        list_time_speaker.append({
            'start': round(speaker.start, 2),
            'end': round(speaker.end, 2) })
        
    list_time_speaker_reduzido = aproximacao(list_time_speaker)
        
    return list_time_speaker

def main(path_log:str) -> str:
    ## Import do Token
    log_config = os.path.join(os.getcwd(), 'config.json')
    log_config = read_json(log_config)
    token = log_config['token']
    
    
    log = read_json(path_log)
    
    ## -- Importando o modelo
    model_ = model(token)
    
    ## -- Aplicando o modelo
    result = timer_speaks(model_, log[0]['path_audio_video'])
    log.append(result) 
    
    write_json(path_log, log)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python -m app.detect_speech path_log.json")
        sys.exit(1)

    path_log = sys.argv[1]
    main(path_log)
    

## Função aproximação funciona, mas precisa ser melhorada ainda, no futuro ela será aplicada