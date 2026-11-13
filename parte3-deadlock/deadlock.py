import threading
import time

LOCK_A = threading.Lock()
LOCK_B = threading.Lock()

def thread_1():
    print("[T1] Tentando adquirir LOCK_A...")
    LOCK_A.acquire()
    print("[T1] Adquiriu LOCK_A.")
    
    time.sleep(0.2)
    
    print("[T1] Tentando adquirir LOCK_B...")
    LOCK_B.acquire()
    print("[T1] Adquiriu LOCK_B. Concluiu trabalho!")
    
    LOCK_B.release()
    LOCK_A.release()

def thread_2():
    print("[T2] Tentando adquirir LOCK_B...")
    LOCK_B.acquire()
    print("[T2] Adquiriu LOCK_B.")
    
    time.sleep(0.2)
    
    print("[T2] Tentando adquirir LOCK_A...")
    LOCK_A.acquire()
    print("[T2] Adquiriu LOCK_A. Concluiu trabalho!")
    
    LOCK_A.release()
    LOCK_B.release()

if __name__ == "__main__":
    t1 = threading.Thread(target=thread_1, name="Thread-1", daemon=True)
    t2 = threading.Thread(target=thread_2, name="Thread-2", daemon=True)

    t1.start()
    t2.start()

    t1.join(timeout=2.0)
    t2.join(timeout=2.0)

    if t1.is_alive() or t2.is_alive():
        print("\n=== DEADLOCK DETECTADO ===")
        print("As threads ficaram bloqueadas aguardando recursos entre si.")
        print("Threads ativas no momento (threading.enumerate):")
        for t in threading.enumerate():
            print(f" - {t.name} (viva={t.is_alive()})")