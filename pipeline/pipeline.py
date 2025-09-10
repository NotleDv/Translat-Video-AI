from tempfile import TemporaryDirectory
import os
import shutil
from pathlib import PureWindowsPath
import subprocess
from tqdm import tqdm
import magic
from pathlib import Path
import mimetypes
mime = magic.Magic(mime=True)
import torch
from app.detect_speech import main
from app.configs import write_json
import time
from pipeline.utils import suprimir_avisos_gerais



def create_dir_auxiliar (path_log:str, dir_:str, path, file) -> str:
    ## -- Create dirs supports
        path_dir_audio = os.path.join(dir_, 'audio')
        path_dir_audio_generator = os.path.join(dir_, 'audio', 'generator')
        path_dir_audio_split = os.path.join(dir_, 'audio', 'split')
        
        os.mkdir(path_dir_audio)
        os.mkdir(path_dir_audio_generator)
        os.mkdir(path_dir_audio_split)
        
        write_json(path_log, [{
            #"path_origem_dir": pasta,
            "path_video": path,
            "name_video": file,
            "path_dir_audio": path_dir_audio,
            "path_dir_audio_generator": path_dir_audio_generator,
            "path_dir_audio_split": path_dir_audio_split
            #"extesion_video": extensao_video
        }])

def manipulation_path(path: str) -> str:
    path_novo = path
    sistem = PureWindowsPath(path).drive

    if ':' in sistem:
        path_novo = subprocess.check_output(
            ["wslpath", path_novo]
        ).decode().strip() 
    

    return path_novo

def pipeline(path_log:str, dir_:str, file:str):
    ## -- Extract Audio
    from app.extract_audio import main as extract_audio
    extract_audio(path_log)
    
    ## -- Detect Speech
    raiz = os.getcwd()
    path_venv = os.path.join(raiz, '.venv_ds/bin/python')
    path_detect = ('app.detect_speech')
    cmd = [str(path_venv), '-m', str(path_detect), str(path_log)]
    subprocess.run(cmd, check=True)


    ## -- Split Áudio
    from app.split_audio import main as split_audio
    split_audio(path_log)

    ## -- Audio to Text
    from app.audio_to_text import main as audio_to_text
    audio_to_text(path_log)
    
    ## -- Translat Text
    from app.translat_text import main as translat_text
    translat_text(path_log)


    # -- Text to Audio
    from app.text_to_audio import main as text_to_audio
    text_to_audio(path_log)
    
    bar = tqdm(total = 100, desc="Finalizando...", colour="#0DD338")
    #breakpoint()
    # -- Slig Accompaniment
    from app.split_accompaniment import main as split_accompaniment
    split_accompaniment(path_log)
    bar.update(60)
    
    # -- Processing Audio
    from app.processing_audio import main as processing_audio
    processing_audio(path_log)
    bar.update(25)
    
    # -- Finish
    from app.finish import main as finish
    path_video_temp = os.path.join(dir_, file)
    bar.update(15)
    
    resultado = finish(path_log, path_video_temp, dir_)
    return resultado 

def extensoes_mime():
    extensoes = {}

    for ext, mime in mimetypes.types_map.items():
        if mime.startswith("video/"):
            if mime not in extensoes:
                extensoes[mime] = []
            extensoes[mime].append(ext)
        extensoes['mkv'] = ['.mkv']
    return extensoes

def validacao_arquivo(files:list, path_dir_origem:str, dir_temp:str) -> list:
    #Movendo os arquivos para a pasta_temp principal
    list_path_videos = []

    for i in tqdm(files, total=len(files), colour="#2196F3"):
        name_file = i
        tqdm.write(f'Movendo: {i}')
        
        i = manipulation_path(i)
        path_temp = os.path.join(path_dir_origem, i)
        
        # Pular se for diretório
        if os.path.isdir(path_temp):
            continue
        
        # Valindo se o path é de um vídeo - por meio da extensão
        extensao_video = mimetypes.guess_extension(mime.from_file(path_temp)) # Gerando a possível extensão do vídeo
        validacao = False
        posiveis_extensoes = extensoes_mime()
        for _, extensao in posiveis_extensoes.items():
            if extensao_video in extensao:
                validacao = True
                break
        
        if validacao:
            shutil.copy(path_temp, dir_temp)        
            list_path_videos.append({'name_file': name_file , 'path_temp': path_temp})
    
    return list_path_videos

def main():
    time_in = time.time()
    with TemporaryDirectory() as dir_:
        pasta = input('Digite o path da pasta: ')
        #print(dir_)
        
        # Criação das pastas auxiliares
        path_log = os.path.join(dir_, 'log.json')
        #create_dir_auxiliar(path_log, dir_)
        
        # Manipulação do path e verificação de itens
        path_dir_origem = manipulation_path(pasta)
        
        path_dir_destino = os.path.join(path_dir_origem, 'traduções')
                
        q_itens = os.listdir(path_dir_origem)
        
        # Verificação Y/n
        while(True):
            condicional = input(f'Traduzir os {len(q_itens)} itens? [Y/n]: ')
            if condicional.lower() == 'y' or condicional.lower() == 'n':
                break
        
        # Codicional para tradução +1 vídeo
        if condicional.lower() == 'y':
            list_path_videos = []
            print("Vídeos a serem traduzidos: ")
            
            #Apenas listando
            for i in q_itens:
                print(i)
            
            list_path_videos = validacao_arquivo(files=q_itens, 
                                                 path_dir_origem=path_dir_origem, 
                                                 dir_temp=dir_)
            
            for i in list_path_videos:
                with TemporaryDirectory() as dir_sub:
                    file = i['name_file']
                    path = i['path_temp']
                       
                    #Iniciando a Tradução   
                    path_log = os.path.join(dir_sub, 'log.json')
                    
                    create_dir_auxiliar(path_log = path_log, 
                                        dir_ = dir_sub, 
                                        path = path,
                                        file = file)
                                        
                    result = pipeline(path_log = path_log,
                                      dir_ = dir_, 
                                      file = file)

                    if not os.path.exists(path_dir_destino): os.mkdir(path_dir_destino)
                    shutil.copy(result, path_dir_destino)
                    print(f'😆 [{file}] traduzido!')
        else:
            # Valindo se o path é de um vídeo - por meio da extensão
            input_ = input("Digite o nome do vídeo juntamente da extensão: ")
            
            name_video = input_
            
            input_ = manipulation_path(input_)
            #path_video = os.path.join(path_dir_destino, input_)
            input_ = [input_]
            
            input_ = validacao_arquivo(files=input_, 
                                       path_dir_origem=path_dir_origem, 
                                       dir_temp=dir_)
           
            create_dir_auxiliar(path_log = path_log, 
                                dir_ = dir_, 
                                path = input_[0]['path_temp'], 
                                file = name_video) 
            #print(dir_)
            
            result = pipeline(path_log = path_log,
                              dir_ = dir_, 
                              file = input_[0]['path_temp'])
            #breakpoint()
            if not os.path.exists(path_dir_destino): os.mkdir(path_dir_destino)
            shutil.copy(result, path_dir_destino)
            print(f'\n\n😆 [{name_video}] traduzido!')
            
    time_end = time.time() 
    
    time_total = (time_end - time_in)/60
    print(f"⌛ Tempo levado: {round(time_total, 2)}min")       
        



if __name__ == "__main__":
    main()

#print(videos)