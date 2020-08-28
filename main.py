import re

class Symbol:
    def __init__(self):
        self.tokens = {}
        self.total = 0

class Error:
    def __init__(self, idx, text):
        self.idx = idx
        self.text = text

KEYWORDS = {"int", "double", "float", "real", "break", "case", "char", "const", "continue"}
symbols = Symbol()
errors = []

def output_file_reference():
    return open("output.txt", "w")

def load_input_file():
    """
    @Description
    Função responsável por efetuar a leitura do arquivo de entrada e retornar
    seu conteúdo.
    O arquivo de entrada deve estar localizado na mesma pasta desse programa,
    também deve ter a extensão .txt
    
    @Return
    Retorna cada linha do arquivo em um array
    """
    
    file = open("input.txt", "r")
    return file.read().splitlines()

def isKeyword(text):
    """
    @Description
    Identifica se o argumento text está no set KEYWORDS
    
    @Return
    False se não esta em KEYWORDS, do contrário, retorna True
    """
    
    return text in KEYWORDS

def isComment(text):
    """
    @Description
    Identifica se o argumento text é um comentário
    
    @Return
    False se não é um comentario, do contrário, retorna True
    """
    
    return len(text) >= 2 and text[0] == '/' and text[1] == '/'

def tokenize(text, idx):
    """
    @Description
    Identifica se o argumento text é um token válido

    @Return
    1. Se text é identificado como um token válido, é retornada uma tupla de 2
    2 valores, onde o primeiro valor será a string SUCCESS e o segundo
    valor será uma descrição do token identificado.
    ("SUCCESS", "EXEMPLO DE DESCRIÇÃO")

    2. Se text não é identificado como um token, uma segunda validação
    verifica se text é um comentário, se sim,
    retorna uma tupla de 2 valores onde o primeiro valor será a string
    COMMENT e o segundo valor será a linha do comentário.
    ("COMMENT", idx) -> sendo idx um inteiro representando a linha.

    3. Caso text não se encaixe nos itens 1 e 2, significa que temos um token
    inválido, portanto, é retornada uma tupla de 2 valores contendo no
    primeiro valor a string ERROR e no segundo valor a linha do erro.
    ("ERROR", idx) -> sendo idx um inteiro representando a linha.
    """
    
    maybeError = True

    # ^[0-9]{1,2}\.[0-9]{1,2}$ -> verifica se text e' um double
    # contendo no máximo a dezena e com no máximo duas casas decimais
    # exemplos: 99.99, 9.9, 9.98
    isAMatch = re.search("^[0-9]{1,2}\.[0-9]{1,2}$", text)
    if isAMatch:
        maybeError = False
        if not text in symbols.tokens:
            symbols.total += 1
            symbols.tokens[text] = symbols.total
        return ("SUCCESS", 'NÚMERO REAL {}'.format(symbols.tokens[text]))

    # ^[0-9]{0,2}$ -> verifica se text e' um inteiro
    # com valor maximo de 99
    isAMatch = re.search("^[0-9]{0,2}$", text)
    if isAMatch:
        maybeError = False
        if not text in symbols.tokens:
            symbols.total += 1
            symbols.tokens[text] = symbols.total
        return ("SUCCESS", 'NUMERO INTEIRO {}'.format(symbols.tokens[text]))

    # ^[a-zA-Z]{1}\d*\w* -> verifica se text e' um identificador
    # seguindo a seguinte regra: iniciado por uma letra, podendo possuir na sequência números e/ou letras;
    isAMatch = re.search("^[a-zA-Z]{1}\d*\w*$", text)
    if isAMatch and maybeError:
        maybeError = False
        if not text in symbols.tokens:
            symbols.total += 1
            symbols.tokens[text] = symbols.total
        return ("SUCCESS", 'IDENTIFICADOR {}'.format(symbols.tokens[text]))

    # verifica se e' um comentario ou um erro
    if maybeError:
        if isComment(text):
            return ("COMMENT", idx)
        else:
            errors.append(Error(idx, text))
            return ("ERROR", idx)

def application():
    content = load_input_file()
    output_file = output_file_reference()
    log = ""
    for idx in range(len(content)):
        if isKeyword(content[idx]):
            log = '[{}] {}'.format((idx + 1), content[idx].upper())
            print(log)
            output_file.write(log+ "\n")
        else:
            tokenized = tokenize(content[idx], idx)
            if tokenized[0] == 'SUCCESS':
                log = '[{}] {}'.format((idx + 1), tokenized[1])
                print(log)
                output_file.write(log + "\n")
            elif tokenized[0] == 'COMMENT':
                log = '[{}] COMENTÁRIO'.format(idx + 1)
                print(log)
                output_file.write(log + "\n")
    if symbols.total > 0:
        log = "\nTabela de Símbolos:"
        print(log)
        output_file.write(log + "\n")
        for key in symbols.tokens:
            log = '{} - {}'.format(symbols.tokens[key], key)
            print(log)
            output_file.write(log + "\n")
    if len(errors) > 0:
        log =  "\nErros nas linhas: "
        print(log)
        output_file.write(log + "\n")
        for error in errors:
            log = '{} ({})'.format((error.idx + 1), error.text)
            print(log)
            output_file.write(log + "\n")
    output_file.close()
            
if __name__ == '__main__':
    application()  # inicia o fluxo do programa
