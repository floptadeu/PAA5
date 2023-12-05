import random
import time
import matplotlib.pyplot as plt
import numpy as np

# Problema da mochila 0-1 (Binaria)
#
# xi ∈ N: quantidade do item i colocada na mochila.
# vi : valor de utilidade do item i.
# pi : peso do item i.
# L: capacidade da mochila.
# m: número de tipos de itens.
# Programaçao dinamica = quebrar o problema em subproblemas (estagios)


#dinamico
def knapsack_0_1(vi, pi, L, m):
    # Inicializando a matriz de programação dinâmica
    K = [[0 for x in range(L + 1)] for x in range(m + 1)]

    # Construindo a matriz em bottom up (de baixo para cima)
    for i in range(m + 1):
        for w in range(L + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif pi[i - 1] <= w:
                # Máximo entre não incluir o item i e incluir o item i
                K[i][w] = max(K[i - 1][w], vi[i - 1] + K[i - 1][w - pi[i - 1]])
            else:
                # Não é possível incluir o item i
                K[i][w] = K[i - 1][w]

    return K[m][L]

# Exemplo de uso
vi = [60, 100, 120] # Valores dos itens
pi = [10, 20, 30]   # Pesos dos itens
L = 30              # Capacidade da mochila
m = len(vi)         # Número de itens

#print("Valor máximo que pode ser obtido: ", knapsack_0_1(vi, pi, L, m))



# A estratégia gulosa é escolher os itens baseando-se na razão 
# entre o valor e o peso (valor por unidade de peso) e pegar primeiro os
#  itens com a maior razão.


def greedy_knapsack(vi, pi, L, m):
    # Criando uma lista de índices dos itens
    indices = list(range(m))
    # Calculando a razão valor-peso e ordenando os itens por essa razão
    ratio = [(vi[i] / pi[i], i) for i in indices]
    ratio.sort(reverse=True)

    total_value = 0
    for r, i in ratio:
        if pi[i] <= L:
            total_value += vi[i]
            L -= pi[i]
        else:
            total_value += r * L
            break

    return total_value

# Exemplo de uso
vi = [60, 100, 120] # Valores dos itens
pi = [10, 20, 30]   # Pesos dos itens
L = 50              # Capacidade da mochila
m = len(vi)         # Número de itens

#print("Valor máximo que pode ser obtido (abordagem gulosa): ", greedy_knapsack(vi, pi, L, m))
# Funções para plotar gráficos individuais

def plot_individual_graph(times, title, color):
    plt.figure(figsize=(10, 6))
    plt.plot(times, color=color)
    plt.xlabel('Test Case Number')
    plt.ylabel('Execution Time (milissegundos)')
    plt.title(title)
    plt.show()

def plot_individual_column_graph(times, title, color):
    n_tests = len(times)  # Número de casos de teste
    indices = np.arange(n_tests)  # Índices para o eixo x

    # Criando o gráfico de barras individual
    plt.figure(figsize=(12, 6))
    plt.bar(indices, times, color=color)

    # Adicionando títulos e labels
    plt.xlabel('Test Case Number')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title(f'Execution Time for {title}')

    # Ajustando as marcações do eixo x para os números dos casos de teste
    # Nota: Removemos os labels do eixo x para evitar a desordem
    plt.xticks(indices, [''] * n_tests)

    # Exibindo o gráfico
    plt.show()
    
def generate_random_input(max_items, max_value, max_weight, make_harder_for_greedy=False):
    m = random.randint(1, max_items)
    vi = [random.randint(1, max_value) for _ in range(m)]
    pi = [random.randint(1, max_weight) for _ in range(m)]

    # Ajustando para tornar mais difícil para o algoritmo guloso
    if make_harder_for_greedy:
        # Tornando as razões valor/peso mais similares
        for i in range(m):
            adjustment = random.uniform(0.8, 1.2)
            vi[i] = int(vi[i] * adjustment)
            pi[i] = max(1, int(pi[i] * adjustment))  # Garantindo que o peso não seja zero

    L = random.randint(1, max_weight)
    return vi, pi, L, m

def test_performance(algorithm, test_cases, max_items, max_value, max_weight, make_harder_for_greedy=False):
    times = []
    for _ in range(test_cases):
        vi, pi, L, m = generate_random_input(max_items, max_value, max_weight, make_harder_for_greedy)
        start_time = time.perf_counter()  # Usando time.perf_counter para maior precisão
        algorithm(vi, pi, L, m)
        end_time = time.perf_counter()
        times.append((end_time - start_time) * 1000)  # Convertendo para milissegundos
    return times


# Parâmetros do teste
test_cases = 50   # Número de casos de teste
max_items = 200    # Número máximo de itens
max_value = 100    # Valor máximo de um item
max_weight = 1000  # Peso máximo de um item


# Executar os testes com os parâmetros ajustados
times_dynamic = test_performance(knapsack_0_1, test_cases, max_items, max_value, max_weight)
times_greedy = test_performance(greedy_knapsack, test_cases, max_items, max_value, max_weight, make_harder_for_greedy=True)

# Plotar os gráficos individuais
plot_individual_graph(times_dynamic, 'Dynamic Programming Performance', 'blue')
plot_individual_graph(times_greedy, 'Greedy Algorithm Performance (Harder Cases)', 'green')

plot_individual_column_graph(times_dynamic, 'Dynamic Programming', 'blue')
plot_individual_column_graph(times_greedy, 'Greedy Algorithm (Harder Cases)', 'green')