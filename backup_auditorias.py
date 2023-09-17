import os
import shutil
import os
import glob
import hashlib
import csv


def calculate_file_hash(path):
    list_of_files = glob.glob(os.path.join(path, "*"))

    # Verifica se o arquivo mais recente existe
    if os.path.exists(path):
        # Inicializa o objeto hash
        hasher = hashlib.sha256()
        
        # Lê o arquivo em blocos para evitar carregá-lo inteiramente na memória
        with open(path, "rb") as file:
            while True:
                # Lê um bloco de dados do arquivo
                data = file.read(65536)  # 64 KB
                if not data:
                    break
                # Atualiza o objeto hash com os dados lidos
                hasher.update(data)
        
        # Retorna o hash em hexadecimal
        return hasher.hexdigest()
    else:
        return None




# Lista de strings que você deseja salvar no arquivo CSV
lista_de_strings = []
lista_de_hash = []
lista_de_arquivos_duplicados=[]
hash_lista_de_arquivos_duplicados=[]


# Nome do arquivo CSV onde você deseja salvar as strings
nome_arquivo = "arquivo_nao_copiado.csv"

def tamanhoArquivo (caminho_do_arquivo):

    # Verifica se o arquivo existe
    if os.path.exists(caminho_do_arquivo):
        tamanho_do_arquivo = os.path.getsize(caminho_do_arquivo)
        tamanho_do_arquivo_mb = tamanho_do_arquivo / (1024 * 1024)  # Converte de bytes para megabytes
        tamanho_do_arquivo_str = str(tamanho_do_arquivo_mb)
        return tamanho_do_arquivo_str
    else:
        print('O arquivo não existe.')


def contar_arquivos_diretorio(directory):
    #return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]) #conta apenas arquivos do diretorio, sem incluir subdiretorios
    return sum([len(files) for r, d, files in os.walk(directory)])




def percorrerArquivosECompararHahs(pathParaHash):
    arquivoHash = []
    # Percorra todos os arquivos no diretório
    quantidadeArquivoExistente=0
    for raiz, subdiretorios, arquivos in os.walk(os.path.dirname(pathParaHash)):     #aponta apenas o PATH para fazer a varredura desde a origem até a última pasta
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            try:
                if os.path.isfile(caminho_completo):

                    arquivoComparar=str(calculate_file_hash(caminho_completo))
                    arquivoHash.append(arquivoComparar)

                   
                else:
                    print("Erro: Nenhum arquivo encontrado na pasta especificada.")
            except:
                pass
    
    return arquivoHash

def retornar_lista_nome_arquivos(pathParaHash):
    listagem_arquivos = []
    # Percorra todos os arquivos no diretório
    quantidadeArquivoExistente=0
    for raiz, subdiretorios, arquivos in os.walk(os.path.dirname(pathParaHash)):     #aponta apenas o PATH para fazer a varredura desde a origem até a última pasta
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(raiz, nome_arquivo)
            try:
                if os.path.isfile(caminho_completo):

                     listagem_arquivos.append(caminho_completo)

                   
                else:
                    print("Erro: Nenhum arquivo encontrado na pasta especificada.")
            except:
                pass
    
    return listagem_arquivos


def copiar_diretorio(src, dst,apenas_auditoria):

    print("Totalizando arquivos em cada diretório. Aguarde...")
    
    hashArquivosOrigem= percorrerArquivosECompararHahs(src)
    caminho_arquivos_da_origem= retornar_lista_nome_arquivos(src)

    hashArquivosDestino= percorrerArquivosECompararHahs(dst)

    arquivosCopiados=[]
    
    for arquivo_duplicado, arquivo_origem in zip(hashArquivosOrigem,caminho_arquivos_da_origem):
        if(hashArquivosOrigem.count(arquivo_duplicado)>1):
            if not arquivo_origem in lista_de_arquivos_duplicados:
                lista_de_arquivos_duplicados.append(arquivo_origem)
                hash_lista_de_arquivos_duplicados.append(arquivo_duplicado)

    qtdArquivosNaOrigem = contar_arquivos_diretorio(src)
    contadorArquivosCopiados=0

    hashArquivoAtualOrigem=""

    print("O diretório: " + src +" Possui: " + str(qtdArquivosNaOrigem) + " arquivos.")

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)

        if os.path.isdir(s):
            if not os.path.exists(d):
                os.makedirs(d)
            copiar_diretorio(s, d,apenas_auditoria)
        else:                              #sem o else, cria-se apenas os diretórios, deixando intactos arquivos já copiados/criados
            hashArquivoAtualOrigem= str(calculate_file_hash(s))

            if(hashArquivoAtualOrigem in arquivosCopiados):
                continue
            else:
                if(hashArquivoAtualOrigem in hashArquivosDestino):
                    continue
                else:
                    arquivosCopiados.append(hashArquivoAtualOrigem)
                    if not apenas_auditoria:    #apenas copia se auditoria estiver desativada
                        shutil.copy2(s, d)
                        contadorArquivosCopiados=contadorArquivosCopiados+1
                        print("Progresso: " + str((contadorArquivosCopiados/qtdArquivosNaOrigem)*100) + "%")








apenas_auditoria=True       # True = apenas irá verificar e salvar em arquivo CSV os arquivos duplicados na origem ou já salvos no destino

# Caminho do diretório original
diretorio_original = 'D:\\Documentos\\Leandro\\Fotos e Videos\\'

# Caminho onde o novo diretório será criado
novo_diretorio = 'D:\\Users\\'






# Verifica se o diretório original existe
if os.path.exists(diretorio_original):
    # Cria o diretório destino se não existir
    if not os.path.exists(novo_diretorio):
        os.makedirs(novo_diretorio)
    
    # Copia o conteúdo
    copiar_diretorio(diretorio_original, novo_diretorio,apenas_auditoria)
else:
    print(f'O diretório {diretorio_original} não existe.')
# Abrir o arquivo CSV em modo de escrita
with open(nome_arquivo, mode="w", newline="",encoding='utf-8') as arquivo_csv:
    # Crie um objeto escritor CSV
    escritor_csv = csv.writer(arquivo_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # Escreva as strings no arquivo CSV
    contadorAuxiliar=1
    for arquivo_nao_copiado,hash_arquivo_nao_copiado in zip(lista_de_arquivos_duplicados,hash_lista_de_arquivos_duplicados):
        #print(hash_lista_de_arquivos_duplicados)
        escritor_csv.writerow([arquivo_nao_copiado,hash_arquivo_nao_copiado])
        contadorAuxiliar=contadorAuxiliar+1
