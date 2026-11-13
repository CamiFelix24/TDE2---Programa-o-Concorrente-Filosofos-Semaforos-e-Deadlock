import threading
import time

T = 8
M = 200_000

count = 0

def incrementar():
    global count
    for _ in range(M):
        temp = count
        time.sleep(0)
        count = temp + 1

if __name__ == "__main__":
    threads = [threading.Thread(target=incrementar) for _ in range(T)]

    inicio = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    fim = time.perf_counter()

    esperado = T * M
    print("=== VERSÃO 1: SEM SINCRONIZAÇÃO (CONDIÇÃO DE CORRIDA) ===")
    print(f"Threads (T): {T} | Incrementos por thread (M): {M}")
    print(f"Valor esperado : {esperado}")
    print(f"Valor obtido   : {count}")
    print(f"Perdidos       : {esperado - count}")
    print(f"Tempo execução : {fim - inicio:.4f} s")