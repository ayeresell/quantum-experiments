import time
from pyqpanda3.core import H, X, CNOT, measure, QProg
from pyqpanda3.qcloud import QCloudService, QCloudOptions

API_KEY = "abfe658c02b929b6958491786a3fbcab8e72c61499c8bf49fab45e72b4b4c3944c63425557666f7650795334315a5478"

# 8-битный секретный ключ
SECRET = [1, 0, 1, 1, 0, 1, 0, 1]
N = len(SECRET)

# --- Классическое решение ---
# Представим, что проверка одного бита (или одного варианта) занимает время, 
# так как функция (оракул) очень сложная (например, криптографическая).
def classical_oracle(bit_index):
    # Симуляция сложных классических вычислений (0.5 сек на бит)
    time.sleep(0.5) 
    return SECRET[bit_index]

def solve_classical():
    print(f"\n[Классический ПК] Начинаем поиск {N}-битного ключа...")
    start_time = time.time()
    
    found_secret = []
    for i in range(N):
        print(f"  Классический процессор вычисляет бит {i}...")
        bit = classical_oracle(i)
        found_secret.append(str(bit))
        
    end_time = time.time()
    classic_time = end_time - start_time
    result_str = "".join(found_secret)
    print(f"[Классический ПК] Ключ найден: {result_str}")
    print(f"[Классический ПК] Потрачено времени: {classic_time:.2f} сек. (сделано {N} запросов к оракулу)")
    return classic_time

# --- Квантовое решение (Алгоритм Бернштейна-Вазирани) ---
def solve_quantum():
    print(f"\n[Квантовый ПК] Начинаем поиск {N}-битного ключа с помощью чипа Wukong...")
    print("  Используем алгоритм Бернштейна-Вазирани, который решает задачу за 1 запрос!")
    start_time = time.time()
    
    service = QCloudService(API_KEY)
    backend = service.backend("72")
    
    prog = QProg()
    
    # 1. Инициализация (N кубитов в суперпозиции, 1 вспомогательный в состоянии |->)
    for i in range(N):
        prog << H(i)
    
    prog << X(N) << H(N) # Вспомогательный кубит
    
    # 2. Квантовый оракул (вычисляется 1 раз для всех возможных состояний одновременно!)
    for i in range(N):
        if SECRET[i] == 1:
            prog << CNOT(i, N)
            
    # 3. Финальная интерференция
    for i in range(N):
        prog << H(i)
        
    # 4. Измерение
    for i in range(N):
        prog << measure(i, i)
        
    options = QCloudOptions()
    options.set_amend(True)
    options.set_optimization(True)
    
    print("  Отправка квантовой схемы на реальный 72-кубитный чип...")
    job = backend.run(prog, 1000, options)
    counts = job.result().get_counts()
    
    end_time = time.time()
    quantum_time = end_time - start_time
    
    # Сортируем результаты по частоте
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    top_bitstring, top_count = sorted_counts[0]
    
    print(f"[Квантовый ПК] Самый частый ответ (из 1000 шотов): {top_bitstring} (уверенность {top_count/1000:.1%})")
    print(f"[Квантовый ПК] Ключ найден всего за 1 квантовый шаг!")
    print(f"[Квантовый ПК] Потрачено времени: {quantum_time:.2f} сек. (включая сетевую задержку до Китая и обратно)")
    
    return quantum_time, top_bitstring

if __name__ == "__main__":
    print("=== Демонстрация Квантового Превосходства (Алгоритм Бернштейна-Вазирани) ===")
    print("Задача: Разгадать сложный секретный ключ. Доступ к 'черному ящику' (оракулу) требует больших вычислительных затрат.")
    
    t_classic = solve_classical()
    t_quantum, q_res = solve_quantum()
    
    print("\n=== ИТОГОВОЕ СРАВНЕНИЕ ===")
    expected_str = "".join(map(str, SECRET))
    if q_res == expected_str:
        print("✅ Квантовый алгоритм выдал абсолютно точный ответ.")
    else:
        print(f"⚠️ Квантовый алгоритм выдал '{q_res}', а ожидалось '{expected_str}'. (Влияние квантового шума)")
        
    print(f"Классическое время: {t_classic:.2f} сек ({N} шагов)")
    print(f"Квантовое время:    {t_quantum:.2f} сек (1 шаг)")
    
    if t_quantum < t_classic:
        print(f"🚀 Квантовый компьютер оказался быстрее в {t_classic/t_quantum:.1f} раз!")
    else:
        print(f"ℹ️ Квантовый ПК выполнил алгоритм за 1 шаг, но сетевая задержка сделала общее время больше.")
