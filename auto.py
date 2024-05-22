import subprocess

caminho = r'C:\Users\T-GAMER\Desktop\ProjetoWhatsHype'

try:
    # executar o script youtubePesquisaID.py
    processo_pesquisa_id = subprocess.Popen(['python', caminho + '\\youtubePesquisaID.py'])
    # esperar até que o processo do youtubePesquisaID.py seja encerrado
    processo_pesquisa_id.wait()
    print("Script youtubePesquisaID.py executado com sucesso!")

    # Executar o script youtubePopular.py
    processo_popular = subprocess.Popen(['python', caminho + '\\youtubePopular.py'])
    print("Script youtubePopular.py executado com sucesso!")
    input("Pressione Enter para fechar esta janela...")
    
except Exception as e:
    print("Ocorreu um erro durante a execução dos scripts:")
    print(e)
    input("Pressione Enter para fechar esta janela...")