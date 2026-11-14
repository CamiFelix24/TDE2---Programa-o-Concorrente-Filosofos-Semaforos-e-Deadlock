# TDE — Programação Concorrente

**Vídeo de Apresentação (YouTube):** https://youtu.be/Kl0A0woB-Zs?si=I2EYWcqKw38lDXKf

* **Integrante:** Camila P. F. Felix (Trabalho Individual)
* **Linguagem utilizada:** Python 3.10+

---

## Como Executar

Para o trabalho será usado o **Python 3.10+** instalado. Não são necessárias bibliotecas externas (apenas a biblioteca padrão `threading` e `time`).

## Parte 1 — Jantar dos Filósofos

### Dinâmica do Problema e Causa do Impasse
Cinco filósofos alternam entre os estados **pensando**, **com fome** e **comendo**, compartilhando 5 garfos dispostos entre eles (`garfo i` entre o filósofo `i` e `(i + 1) mod 5`). Na versão ingênua, todos os filósofos pegam primeiro o garfo à sua esquerda e, em seguida, tentam pegar o garfo à sua direita. Quando os cinco ficam com fome simultaneamente e adquirem o garfo esquerdo, nenhum garfo direito resta disponível, fazendo com que todas as threads fiquem bloqueadas indefinidamente em um **deadlock**.

### Protocolo de Solução e Condição de Coffman Negada
* **Estratégia escolhida:** **Hierarquia de recursos** (ordenação global). Os garfos são numerados de `0` a `4`, e cada filósofo é obrigado a adquirir sempre o garfo de **menor índice** primeiro (`min(esq, dir)`) e depois o de **maior índice** (`max(esq, dir)`).
* **Condição de Coffman negada:** **Espera circular**. Como todos adquirem recursos em ordem estritamente crescente, torna-se matematicamente impossível formar um ciclo fechado de dependência (o Filósofo 4 tenta pegar o garfo `0` antes do `4`, cedendo passagem ao Filósofo 0).
* **Progresso e Justiça (Ausência de Inanição):** Como nenhum filósofo retém garfos indefinidamente (o tempo de refeição é finito e os locks são liberados logo após comer) e a ordem parcial impede bloqueios mútuos, o sistema garante progresso contínuo. Além disso, o escalonamento de locks do sistema operacional alterna o acesso entre vizinhos conforme os garfos são liberados, evitando que um único filósofo monopolize os recursos.

### Pseudocódigo do Protocolo (Hierarquia de Recursos)
```text
Dados: N = 5 filósofos, Garfos 0..N-1

Para cada filósofo p:
  primeiro = min(garfo_esquerda(p), garfo_direita(p))
  segundo  = max(garfo_esquerda(p), garfo_direita(p))

  Loop:
    pensar()
    estado[p] <- "com fome"
    adquirir(primeiro)
    adquirir(segundo)
    estado[p] <- "comendo"
    comer()
    liberar(segundo)
    liberar(primeiro)
    estado[p] <- "pensando"
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
```