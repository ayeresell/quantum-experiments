from pyqpanda3.core import H, X, CNOT, measure, QProg
from pyqpanda3.qcloud import QCloudService, QCloudOptions

def find_secret_with_wukong(api_key):
    service = QCloudService(api_key)
    backend = service.backend("72")
    
    # Секретное число: 13 (в двоичной 1101)
    # Порядок битов: q0=1, q1=0, q2=1, q3=1
    secret = [1, 0, 1, 1] 
    
    prog = QProg()
    
    # 1. Подготовка: кубиты 0-3 в суперпозицию, кубит 4 в состояние |->
    for i in range(4):
        prog << H(i)
    
    prog << X(4) << H(4) # Вспомогательный кубит для фазового сдвига
    
    # 2. ОРАКУЛ: "Зашиваем" секрет в схему
    # Если в секрете 1, ставим связь CNOT между кубитом и анциллой
    for i in range(4):
        if secret[i] == 1:
            prog << CNOT(i, 4)
            
    # 3. Финальная интерференция
    for i in range(4):
        prog << H(i)
        
    # 4. Измерение только основных кубитов
    for i in range(4):
        prog << measure(i, i)
        
    options = QCloudOptions()
    options.set_amend(True) # Включаем подавление ошибок (error mitigation)
    options.set_optimization(True)
    
    print("Отправка задачи... Wukong ищет секрет 1101 (13) за один проход!")
    job = backend.run(prog, 1000, options) # Увеличиваем количество shots до 1000
    return job.result().get_counts()

# --- Запуск ---
API_KEY = "abfe658c02b929b6958491786a3fbcab8e72c61499c8bf49fab45e72b4b4c3944c63425557666f7650795334315a5478"
try:
    counts = find_secret_with_wukong(API_KEY)
    print("\n--- Результат квантового поиска (1000 shots) ---")
    
    # Сортируем результаты по частоте выпадения (от большего к меньшему)
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    
    for bitstring, count in sorted_counts:
        # Читаем биты напрямую, так как pyqpanda возвращает их в правильном порядке (q3 q2 q1 q0)
        decimal = int(bitstring, 2) 
        print(f"Битстрока: {bitstring} | Число: {decimal:2d} | Выпало раз: {count}")
        
    # Выводим самый частый результат
    top_bitstring, top_count = sorted_counts[0]
    top_decimal = int(top_bitstring, 2)
    print(f"\nСамый частый результат: {top_bitstring} (Число {top_decimal}), вероятность {top_count/1000:.1%}")
    if top_decimal == 13:
        print("Успех! Квантовый алгоритм нашел правильный секрет!")
    else:
        print("Шум помешал найти правильный секрет на первом месте.")
        
except Exception as e:
    print(f"Ошибка: {e}")
