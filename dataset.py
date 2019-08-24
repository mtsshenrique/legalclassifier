







txt = "blabla"
categoria = 0
#categorias
#1 - publicação de falência
#2 - publicação de convolação em falencia
#3 - publicação de extensão dos efeitos de falencia
#4 - publicação de insolvencia civil
#5 - publicacao de recuperacao extrajudicial
#6 - publicação de recuperação judicial

if 'falencia' in txt or 'falida' in txt or 'falido' in txt:
    if 'decretado' in txt or 'extinto' in txt or 'encerramento' in txt or 'decretacao' in txt or 'decretad' in txt:
        categoria = 1
    if 'convolacao' in txt or 'convolo' in txt or 'relacao de credores' in txt or 'relacao nominal de credores' in txt or 'recuperacao judicial' in txt:
        categoria = 2
    if 'extensao dos efeitos' in txt or 'estendo os efeitos' in txt:
        categoria = 3

if 'insolvencia' in txt:
    if 'declaro' in txt or 'civil' in txt or 'convocacao dos credores' in txt:
        categoria = 4

if 'recuperacao extrajudicial' in txt or 'liquidacao extrajudicial' in txt:
    if 'decretada' in txt or 'processamento' in txt or 'decretado' in txt:
        categoria = 5

if 'recuperacao judicial' in txt:
    if 'defiro' in txt or 'deferida' in txt or 'processamento da' in txt or 'concedido' in txt or 'plano de' in txt or 'nomeio' in txt:
        categoria = 6