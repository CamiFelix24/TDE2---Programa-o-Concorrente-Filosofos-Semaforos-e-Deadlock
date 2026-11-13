import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

def tarefa_segura(nome):
    print(f"[{nome}] Tentando adquirir LOCK_A...")
    with LOCK_A:
        print(f"[{nome}] Adquiriu LOCK_A.")
        time.sleep(0.2)
        
        print(f"[{nome}] Tentando adquirir LOCK_B...")
        with LOCK_B:
            print(f"[{nome}] Adquiriu LOCK_B. Executando seção crítica...")
            time.sleep(0.1)
            print(f"[{nome}] Liberando LOCK_B e LOCK_A.")
            
    print(f"[{nome}] Concluiu com sucesso!")

if __name__ == "__main__":
    t1 = threading.Thread(target=tarefa_segura, args=("Thread-1",))
    t2 = threading.Thread(target=tarefa_segura, args=("Thread-2",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("\n=== EXECUÇÃO FINALIZADA SEM DEADLOCK ===")