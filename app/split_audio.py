import ffmpeg, imageio_ffmpeg
import os
from app.configs import write_json, read_json


def extrair_audio_f(path_in:str, path_out:str, log:list) -> list:
    input_ = path_in
    path_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    # --- Extração de áudio  ---
    for index, i in enumerate(log[1]):
        
        path_out_ = os.path.join(path_out, f'{index}.wav')
        
        try:
            (
                ffmpeg
                .input(input_, ss=float(i['start']), to=float(i['end']))
                .output(path_out_)
                .run(cmd=path_ffmpeg, overwrite_output=True, quiet=True)
            )
            #print(f'Extração de áudio concluída: {path_out_}')
            
            log[1][index]['path_audio'] = path_out_
            
        except ffmpeg.Error as e:
            print('Erro no ffmpeg:', e)
    
    return log
            
            
def main(path_log:str):
    log = read_json(path_log)
    
    path_audio = log[0]['path_audio_video']
    path_out = log[0]['path_dir_audio_split']
       
    log_f = extrair_audio_f(path_audio, path_out, log)
    
    write_json(path_log, log_f)
    
    
    