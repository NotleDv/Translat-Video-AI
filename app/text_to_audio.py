from IPython.display import Audio
import soundfile as sf
import numpy as np
from app.configs import read_json, write_json
import os
from tqdm import tqdm
from kokoro import KPipeline

    

def gerar_audio (texto, path_destino, index):
    contador = 0
    
    pipeline = KPipeline(lang_code='p')
    generator = pipeline(
        texto, voice='af_heart', # <= change voice here
        speed=1, split_pattern=r'\n+'
        )
    
    path_audios_gerados = []
    
    for i, (gs, ps, audio) in enumerate(generator):
        # print(i)  # i => index
        # print(gs) # gs => graphemes/text
        # print(ps) # ps => phonemes
        # #display(Audio(data=audio, rate=24000, autoplay=i==0))
        Audio(data=audio, rate=24000)
        
        samplerate = 24000
        
        
        if contador == 0:
            name_audio = os.path.join(path_destino, f'audio{index}.wav')
            
            path_audios_gerados.append({f'audio_{index}': name_audio})
            
            audio_np = np.array(audio, dtype=np.float32)
            sf.write(name_audio, audio_np, samplerate)
            
        else:
            name_audio = os.path.join(path_destino, f'audio{index} ({contador}).wav')
            
            path_audios_gerados.append({f'audio_{index}': name_audio})
            
            audio_np = np.array(audio, dtype=np.float32)
            sf.write(name_audio, audio_np, samplerate)
            
        contador+=1
        
    return path_audios_gerados
         
def main(path_log:str):
    log = read_json(path_log)
    
    output = log[0]['path_dir_audio_generator']
    
    q = len(log[1])
    bar = tqdm(total=q, desc="Gerando áudios...", colour="#2196F3")
    bar_count = 0
    
    for index, i in enumerate(log[1]):
        bar.update(bar_count)
        
        log[1][index]['path_audios_gerados'] = gerar_audio(i['text_destino'], output, index)

        bar_count+=1
    
    print()
    write_json(path_log, log)
    
    
    