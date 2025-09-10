import json

def torch_config ():
    import torch
    n_devices = torch.cuda.device_count()

    device_ = "cpu" if not n_devices else "cuda"
    
    return device_

def read_json (path):
    log = ''
    with open(path, 'r', encoding='utf-8') as file:
        log = json.load(file)
    
    return log

def write_json (path, dados):        
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(dados, ensure_ascii=False, indent=2))
    except:
        print('erro ao salvar o json')


    
      