OBSTACULO = 1

# Funções de Formatação
def gerar_titulo(titulo, colunas, decoracao="-"):
    return titulo.center((colunas + 1)* 3, decoracao)# + "\n"


def gerar_cabecalho_matriz(titulo, largura_matriz):
    titulo = gerar_titulo(titulo, largura_matriz)
    primeira_linha = "".join([f" {i} " for i in range(largura_matriz)]) + " "    
    cabecalho = f"{titulo}\n  {Formatacao.underline}{primeira_linha}{Formatacao.reset}\n"
    return cabecalho


def concatenar_representacoes(r1, r2):
    linhas_r1 = r1.split("\n")
    linhas_r2 = r2.split("\n")

    nova_representacao = ""
    for lr1, lr2 in zip(linhas_r1, linhas_r2):
        nova_representacao += lr1 + " " * 3 + lr2 + "\n"
    
    return nova_representacao


def colorir_celula(linha, coluna, valor_celula,
                   posicao_aspirador, posicao_carregador, hotspots,
                   coordenadas_percepcao):
    cor = ""

    if [linha, coluna] in hotspots:
        cor += Cores.bgRed
    if [linha, coluna] == posicao_aspirador:
        cor += Cores.bgGreen
    if [linha, coluna] == posicao_carregador:
        cor += Cores.bgMagenta
    if valor_celula in {OBSTACULO, str(OBSTACULO)}:
        cor += Formatacao.reversed
    if valor_celula == "?":
        cor += Cores.fgCyan
    if [linha, coluna] in coordenadas_percepcao:
        cor += Cores.fgGreen

    return cor + " " + str(valor_celula) + " " + Cores.reset


# Constantes de Formatação
class Cores:
    reset = "\033[0m"

    # Black
    fgBlack = "\033[30m"
    fgBrightBlack = "\033[30;1m"
    bgBlack = "\033[40m"
    bgBrightBlack = "\033[40;1m"

    # Red
    fgRed = "\033[31m"
    fgBrightRed = "\033[31;1m"
    bgRed = "\033[41m"
    bgBrightRed = "\033[41;1m"

    # Green
    fgGreen = "\033[32m"
    fgBrightGreen = "\033[32;1m"
    bgGreen = "\033[42m"
    bgBrightGreen = "\033[42;1m"

    # Yellow
    fgYellow = "\033[33m"
    fgBrightYellow = "\033[33;1m"
    bgYellow = "\033[43m"
    bgBrightYellow = "\033[43;1m"

    # Blue
    fgBlue = "\033[34m"
    fgBrightBlue = "\033[34;1m"
    bgBlue = "\033[44m"
    bgBrightBlue = "\033[44;1m"

    # Magenta
    fgMagenta = "\033[35m"
    fgBrightMagenta = "\033[35;1m"
    bgMagenta = "\033[45m"
    bgBrightMagenta = "\033[45;1m"

    # Cyan
    fgCyan = "\033[36m"
    fgBrightCyan = "\033[36;1m"
    bgCyan = "\033[46m"
    bgBrightCyan = "\033[46;1m"

    # White
    fgWhite = "\033[37m"
    fgBrightWhite = "\033[37;1m"
    bgWhite = "\033[47m"
    bgBrightWhite = "\033[47;1m"



class Formatacao: 
    underline = "\033[4m"
    reversed = "\u001b[7m"
    reset = "\033[0m"
    Bold = "\u001b[1m"
