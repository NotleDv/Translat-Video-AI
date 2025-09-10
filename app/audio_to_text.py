from app.configs import write_json, read_json
import whisper
from app.configs import torch_config, read_json, write_json
import torch
from tqdm import tqdm
import os
import textwrap

def tratamento_text(text:str, max_len:str) -> list:
    list_temp = []
    len_text = len(text)
    
    if text[0] == ' ':
        for i in range(1, len_text):
            if text[i] != ' ':
                text = text[i:]
                break
            
    if text[-1] == ' ':
        for i in range(1,len_text):
            if text[-i] != ' ':
                text = text[:-i]
                break
    
    new_text = text.split('. ')
    new_text = ' '.join(new_text)
    
    list_temp.append(
            textwrap.wrap(new_text, width=max_len, break_long_words=False)
        )
    
    return list_temp[0]

def model_whisper():
    device_ = torch_config()
    model = whisper.load_model("base", device=device_);
    #model.to(torch.device(device_))
    return model

def audio_to_text (path:str) -> str:    
    #Realizando a transcrição
    model = model_whisper()
    result = model.transcribe(path, fp16=True)
    torch.cuda.empty_cache()
    
    if result['text']:
        return result['text']
    else:
        return 'erro'
             
def main(path_log:str):
    log = read_json(path_log)
    
    q = len(log[1]) #Apenas para contagem
    
    bar = tqdm(total=q, desc="Convertendo áudio em texto...", colour="#2196F3")
      
    #Removendo texto do audio
    for index, i in enumerate(log[1]):
        result = audio_to_text(i['path_audio'])
        log[1][index]['text_origem'] = result
        
        bar.update(1)
    
    bar_ = tqdm(total=q, desc="Ajustando texto...", colour="#2196F3")
    #Reduzindo a dimensionalidade dos texto - Para ajudar na tradução
    for index, element in enumerate(log[1]):
        text = (element['text_origem'])
        result = tratamento_text(text, 50)
        
        log[1][index]['text_origem'] = result
        bar_.update(1)
        
        
    print()
    write_json(path_log, log)
