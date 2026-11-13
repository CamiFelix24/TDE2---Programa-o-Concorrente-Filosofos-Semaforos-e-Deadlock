# TDE — Programação Concorrente

**Vídeo de Apresentação (YouTube):** [INSERIR LINK DO VÍDEO AQUI]

* **Integrante:** Camila P. F. Felix (Trabalho Individual)
* **Linguagem utilizada:** Python 3.10+

---

## Como Executar

Certifique-se de ter o **Python 3.10+** instalado. Não são necessárias bibliotecas externas (apenas a biblioteca padrão `threading` e `time`).

### Parte 1 — Jantar dos Filósofos
```bash
# Versão ingênua (com deadlock)
python parte1-filosofos/filosofos_deadlock.py

# Versão corrigida (hierarquia de recursos)
python parte1-filosofos/filosofos_corrigido.py