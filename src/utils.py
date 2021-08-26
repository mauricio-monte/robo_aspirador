def cima(linha, coluna):
    """Retorna coordenada (l, c) da célula acima"""
    return linha - 1, coluna

def baixo(linha, coluna):
    """Retorna coordenada (l, c) da célula abaixo"""
    return linha + 1, coluna

def direita(linha, coluna):
    """Retorna coordenada (l, c) da célula à direita"""
    return linha, coluna + 1

def esquerda(linha, coluna):
    """Retorna coordenada (l, c) da célula à esquerda"""
    return linha, coluna - 1
