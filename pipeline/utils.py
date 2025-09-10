import os
import warnings
import logging


# 1. Configuração crítica do TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Importamos o logging do transformers aqui dentro para não poluir o namespace
# de quem importa este módulo.
try:
    from transformers import logging as hf_logging
    # Se o transformers estiver instalado, já o configuramos.
    hf_logging.set_verbosity_error()
except ImportError:
    # Se não estiver instalado, não fazemos nada. O módulo continua útil.
    pass

def suprimir_avisos_gerais():
    """
    Configura os sistemas de warnings e logging do Python para serem menos verbosos.
    É uma boa prática chamar esta função no início dos scripts principais.
    """
    # 2. Configuração de warnings e logging do Python
    warnings.filterwarnings('ignore')
    logging.basicConfig(level=logging.ERROR)
    logging.getLogger('speechbrain').setLevel(logging.WARNING)
    logging.getLogger('phonemizer').setLevel(logging.ERROR)
    #print("=> Avisos e logs gerais foram suprimidos.")