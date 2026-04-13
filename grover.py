from pyqpanda3.core import H, X, CNOT, measure, QProg
from pyqpanda3.qcloud import QCloudService, QCloudOptions

def run_grover(api_key):
    service = QCloudService(api_key)
    backend = service.backend("72")
    
    prog = QProg()
    
    # 1. ИНИЦИАЛИЗАЦИЯ:
    # Переводим 2 кубита в суперпозицию. 
    # Теперь они одновременно содержат 4 возможных состояния: |00>, |01>, |10>, |11>
    # (В десятичной системе это 0, 1, 2, 3). У всех состояний одинаковая вероятность - 25%.
    prog << H(0) << H(1)
    
    # 2. ОРАКУЛ (Oracle):
    # Задача оракула - "узнать" искомый элемент и пометить его отрицательным знаком.
    # Допустим, мы ищем состояние |11> (число 3).
    # Для этого применяем гейт CZ (Controlled-Z), который меняет знак амплитуды только для |11>.
    # (Гейт CZ собирается из H и CNOT).
    # После оракула вероятность всё ещё 25%, но у |11> "отрицательная" амплитуда.
    prog << H(1) << CNOT(0, 1) << H(1)
    
    # 3. ДИФФУЗИЯ ГРОВЕРА (Усиление амплитуды):
    # Эта операция делает "инверсию относительно среднего значения". 
    # Так как амплитуда |11> отрицательная, среднее значение падает.
    # Инверсия относительно этого упавшего среднего "убивает" непомеченные состояния 
    # и "накачивает" вероятность помеченного состояния |11> до 100% (в идеале).
    prog << H(0) << H(1)
    prog << X(0) << X(1)
    prog << H(1) << CNOT(0, 1) << H(1) # CZ внутри диффузии
    prog << X(0) << X(1)
    prog << H(0) << H(1)
    
    # 4. ИЗМЕРЕНИЕ:
    # Считываем результат с обоих кубитов.
    prog << measure(0, 0) << measure(1, 1)
    
    options = QCloudOptions()
    options.set_amend(True)
    options.set_optimization(True)
    
    print("Запуск алгоритма Гровера (поиск элемента '11' среди 4 вариантов)...")
    print("Классическому ПК понадобилось бы в среднем 2-3 попытки. Квантовый находит за 1 шаг!")
    job = backend.run(prog, 1000, options)
    return job.result().get_counts()

if __name__ == "__main__":
    API_KEY = "abfe658c02b929b6958491786a3fbcab8e72c61499c8bf49fab45e72b4b4c3944c63425557666f7650795334315a5478"
    try:
        counts = run_grover(API_KEY)
        print("\n--- Результаты (1000 shots) ---")
        
        sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        
        for bitstring, count in sorted_counts:
            decimal = int(bitstring, 2)
            print(f"Состояние: |{bitstring}> | Число: {decimal} | Выпало раз: {count} ({count/10:.1f}%)")
            
        top_bitstring, _ = sorted_counts[0]
        if top_bitstring == "11":
            print("\nУспех! Гровер 'перекачал' вероятность в правильный ответ |11>.")
        else:
            print("\nШум перевесил. Самый частый ответ не |11>.")
            
    except Exception as e:
        print(f"Ошибка: {e}")
