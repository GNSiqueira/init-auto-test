palavras = ["abacate", "abismo", "abdutor", "formabila", "paralelepido"]
palavras_com_ab = [] # Cria uma lista vazia para guardar os resultados

for palavra in palavras:
  if "ab" in palavra:
    palavras_com_ab.append(palavra) # Adiciona a palavra na nova lista

print(f"As palavras que contêm 'ab' são: {palavras_com_ab}")
# Saída: As palavras que contêm 'ab' são: ['abacate', 'abismo', 'abdutor', 'formabila']