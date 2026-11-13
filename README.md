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

## Parte 2 — Threads e Semáforos (Contador Concorrente)

### Tabela de Resultados (T = 8 threads, M = 200.000 incrementos)

| Versão | Execução | Valor Esperado | Valor Obtido | Tempo de Execução (s) |
| :--- | :---: | :---: | :---: | :---: |
| Sem Sincronização | 1 | 1.600.000 | 200.184 | 4,2547 |
| Sem Sincronização | 2 | 1.600.000 | 200.188 | 4,1508 |
| Sem Sincronização | 3 | 1.600.000 | 200.189 | 4,1275 |
| Com Semáforo Binário | 1 | 1.600.000 | 1.600.000 | 17,3611 |
| Com Semáforo Binário | 2 | 1.600.000 | 1.600.000 | 16,3768 |
| Com Semáforo Binário | 3 | 1.600.000 | 1.600.000 | 17,4624 |

### Discussão Técnica
* **Por que a versão sem sincronização perde incrementos:** A operação de incremento (`temp = count` seguida de `count = temp + 1`) não é atômica, sendo composta por leitura, modificação e escrita. Quando o escalonador realiza uma troca de contexto entre essas etapas (forçada aqui pelo `time.sleep(0)` para superar a janela padrão de alternância do GIL em Python), múltiplas threads leem o mesmo valor antigo de `count` antes que ele seja atualizado, sobrescrevendo umas às outras (*lost updates*).
* **Por que a versão com semáforo é correta e garantias de visibilidade/ordenação:** O `threading.Semaphore(1)` atua como um mecanismo de exclusão mútua (mutex), garantindo que apenas uma thread por vez execute a leitura e escrita na seção crítica. Além disso, as chamadas `acquire()` e `release()` atuam como barreiras implícitas de sincronização (equivalente à relação *happens-before*): todas as alterações feitas na memória por uma thread antes de chamar `release()` tornam-se visíveis e ordenadas para a próxima thread que obtiver a permissão via `acquire()`.
* **Trade-off de Throughput:** A versão com semáforo é aproximadamente 4 vezes mais lenta (~17s contra ~4s) porque serializa o acesso à seção crítica e introduz sobrecarga (*overhead*) de gerenciamento de fila e troca de estado das threads bloqueadas/desbloqueadas pelo sistema operacional, sacrificando vazão (*throughput*) em troca de consistência dos dados.

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