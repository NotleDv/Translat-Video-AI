from app.configs import torch_config, read_json, write_json
import torch  
from tqdm import tqdm
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import logging

def translat (texts:list) -> str:
    
    device_ = torch_config()
    ling_input = 'en'  # <<--- Para futuras atualizações
    ling_output = 'pt' # <<--- Para futuras atualizações
    
    logger = logging.getLogger('M2M100ForConditionalGeneration') 
    logger = logging.getLogger('M2M100Tokenizer') 
    model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M").to(device_)
    
    tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
    
    tokenizer.src_lang = ling_input # Idioma de origem
    
    text_completo = ''
    
    for text in texts:
        encoded_hi = tokenizer(text, return_tensors="pt").to(model.device)
        generated_tokens = model.generate(**encoded_hi, forced_bos_token_id=tokenizer.get_lang_id(ling_output)) # Idioma Destino
        traducao = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        
        text_completo += traducao[0] + ' '
        
    return text_completo
              
def main(path_log:str):
    log = read_json(path_log)
    
    q = len(log[1])
    #bar = tqdm(total=q, desc="Traduzindo texto...", colour="#2196F3")
    bar_count = 0
    text_temp = ''
    
    for index, texts in tqdm(enumerate(log[1]), total=len(log[1]), desc='Traduzindo textos'):
        
        result = translat(texts['text_origem'])
        log[1][index]['text_destino'] = result

    write_json(path_log, log)
    
    
    
### Isso funciona, mas demanda mais processamento da gpu    

# from transformers import T5ForConditionalGeneration, T5Tokenizer
# from transformers import BitsAndBytesConfig
# def model_(device_):
#     bnb_config = BitsAndBytesConfig( load_in_8bit=True )

#     model_name = 'jbochi/madlad400-3b-mt'
#     model = T5ForConditionalGeneration.from_pretrained(
#         model_name,
#         quantization_config=bnb_config,
#         device_map = device_)
    
#     tokenizer = T5Tokenizer.from_pretrained(model_name)
#     return model, tokenizer

# def translat (text:str):
#     device_ = torch_config()
    
#     model, tokenizer = model_(device_)
    
#     text_ = f"<2pt> {text}"
#     input_ids = tokenizer(text_, return_tensors="pt").input_ids.to(model.device)
#     outputs = model.generate(input_ids=input_ids)

#     translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     return translation