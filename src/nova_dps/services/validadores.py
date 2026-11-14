import re

def validar_cpf(cpf: str) -> bool:
    """Valida o algoritmo oficial do CPF brasileiro."""
    numeros = [int(digito) for digito in re.sub(r'\D', '', cpf)]
    if len(numeros) != 11:
        return False
    # Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if len(set(numeros)) == 1:
        return False
    # Primeiro dígito verificador
    soma = sum(a * b for a, b in zip(numeros[:9], range(10, 1, -1)))
    digito_1 = (soma * 10 % 11) % 10
    if digito_1 != numeros[9]:
        return False
    # Segundo dígito verificador
    soma = sum(a * b for a, b in zip(numeros[:10], range(11, 1, -1)))
    digito_2 = (soma * 10 % 11) % 10
    return digito_2 == numeros[10]

def validar_telefone(telefone: str) -> bool:
    """Valida telefone/celular com DDD (10 ou 11 dígitos numéricos)."""
    digitos = re.sub(r'\D', '', telefone)
    return len(digitos) in (10, 11)

def validar_email(email: str) -> bool:
    """Valida formato de e-mail padrão."""
    if not email:
        return True # Campo opcional
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(padrao, email.strip()))
