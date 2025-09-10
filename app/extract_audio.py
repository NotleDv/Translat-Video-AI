import ffmpeg, imageio_ffmpeg
import os
from app.configs import write_json, read_json

def extract_audio (input_:str, output:str) -> str:
    # Definição do path de entrada e saída
    input_ = input_
    output_ = output
    
    # Inicialização da Extração
    path_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    try:
        (
            ffmpeg
            .input(input_)
            .output(output_, vn=None,)
            .run(cmd=path_ffmpeg, overwrite_output=True, quiet=True)
        )
        print(f'Extração de áudio concluída: {output_}')
        return output_
        
    except ffmpeg.Error as erro:
        print(erro)

def main(path_log:str) -> str:
    log = read_json(path_log)
    
    path_video = log[0]['path_video']
    path_output = os.path.join(log[0]['path_dir_audio'], 'audio_completo.wav')
    
    path_out_audio = extract_audio ( input_ = path_video,
                                     output = path_output )

    log[0]['path_audio_video'] = path_out_audio
    
    write_json(path_log, log)
