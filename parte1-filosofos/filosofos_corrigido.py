import threading
import time
import random

N = 5
CICLOS_REFEICAO = 3
garfos = [threading.Lock() for _ in range(N)]
print_lock = threading.Lock()

def log(msg):
    with print_lock:
        print(msg)

def filosofo(id_filosofo):
    garfo_esq = id_filosofo
    garfo_dir = (id_filosofo + 1) % N

    primeiro = min(garfo_esq, garfo_dir)
    segundo = max(garfo_esq, garfo_dir)

    for ciclo in range(1, CICLOS_REFEICAO + 1):
        log(f"[Filósofo {id_filosofo}] pensando... (ciclo {ciclo}/{CICLOS_REFEICAO})")
        time.sleep(random.uniform(0.05, 0.15))

        log(f"[Filósofo {id_filosofo}] com fome! Aguardando garfos ({primeiro} e {segundo})...")
        with garfos[primeiro]:
            with garfos[segundo]:
                log(f"[Filósofo {id_filosofo}] comendo (usando garfos {primeiro} e {segundo})...")
                time.sleep(random.uniform(0.05, 0.15))

        log(f"[Filósofo {id_filosofo}] terminou de comer e devolveu os garfos {primeiro} e {segundo}.")

if __name__ == "__main__":
    threads = [
        threading.Thread(target=filosofo, args=(i,), name=f"Filosofo-{i}")
        for i in range(N)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("\n=== TODOS OS FILÓSOFOS CONCLUÍRAM SUAS REFEIÇÕES SEM IMPASSE ===")