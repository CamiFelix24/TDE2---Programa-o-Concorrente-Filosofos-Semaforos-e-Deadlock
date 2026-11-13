# TDE — Programação Concorrente

**Vídeo de Apresentação (YouTube):** [INSERIR LINK DO VÍDEO AQUI]

* **Integrante:** Camila P. F. Felix (Trabalho Individual)
* **Linguagem utilizada:** Python 3.10+

---

## Como Executar

Para o trabalho será usado o **Python 3.10+** instalado. Não são necessárias bibliotecas externas (apenas a biblioteca padrão `threading` e `time`).

### Parte 1 — Jantar dos Filósofos
```bash
# Versão ingênua (com deadlock)
python parte1-filosofos/filosofos_deadlock.py

# Versão corrigida (hierarquia de recursos)
python parte1-filosofos/filosofos_corrigido.py
```

## Parte 3 — Deadlock

### Evidência do Travamento
```text
[T1] Adquiriu LOCK_A.
[T2] Tentando adquirir LOCK_B...
[T2] Adquiriu LOCK_B.
[T2] Tentando adquirir LOCK_A...
[T1] Tentando adquirir LOCK_B...

=== DEADLOCK DETECTADO ===
As threads ficaram bloqueadas aguardando recursos entre si.
Threads ativas no momento (threading.enumerate):
 - MainThread (viva=True)
 - Thread-1 (viva=True)
 - Thread-2 (viva=True)