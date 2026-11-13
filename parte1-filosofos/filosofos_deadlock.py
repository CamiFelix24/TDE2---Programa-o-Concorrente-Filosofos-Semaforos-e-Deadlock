import threading
import time

N = 5
garfos = [threading.Lock() for _ in range(N)]
barreira = threading.Barrier(N)

def filosofo(id_filosofo):
    esq = id_filosofo
    dir_ = (id_filosofo + 1) % N

    print(f"[Filósofo {id_filosofo}] pensando...")
    time.sleep(0.1)

    print(f"[Filósofo {id_filosofo}] com fome! Tentando pegar garfo esquerdo ({esq})...")
    garfos[esq].acquire()
    print(f"[Filósofo {id_filosofo}] pegou o garfo esquerdo ({esq}).")

    barreira.wait()

    print(f"[Filósofo {id_filosofo}] tentando pegar garfo direito ({dir_})...")
    garfos[dir_].acquire()

    print(f"[Filósofo {id_filosofo}] comendo...")
    time.sleep(0.2)
    garfos[dir_].release()
    garfos[esq].release()

if __name__ == "__main__":
    threads = [
        threading.Thread(target=filosofo, args=(i,), name=f"Filosofo-{i}", daemon=True)
        for i in range(N)
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join(timeout=2.0)

    if any(t.is_alive() for t in threads):
        print("\n=== IMPASSE (DEADLOCK) DETECTADO NA MESA ===")
        print("Todos os 5 filósofos seguram o garfo da esquerda e aguardam o da direita:")
        for t in threading.enumerate():
            if t.name.startswith("Filosofo"):
                print(f" - {t.name} bloqueado (viva={t.is_alive()})")