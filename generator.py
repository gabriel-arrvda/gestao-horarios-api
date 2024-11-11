from ortools.linear_solver import pywraplp
import argparse
import json
def parse_arguments():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Process turn scheduling data.")

    # Define arguments expected to be passed by Express
    parser.add_argument('qtd_total_disponivel_clinico', type=int, help='Quantidade total disponível de clínicos')
    parser.add_argument('qtd_total_disponivel_especialista', type=int, help='Quantidade total disponível de especialistas')
    parser.add_argument('qtd_necessaria_clinico_1_turno', type=int, help='Quantidade necessária de clínicos para o 1º turno')
    parser.add_argument('qtd_necessaria_clinico_2_turno', type=int, help='Quantidade necessária de clínicos para o 2º turno')
    parser.add_argument('qtd_necessaria_clinico_3_turno', type=int, help='Quantidade necessária de clínicos para o 3º turno')
    parser.add_argument('qtd_necessaria_especialista_1_turno', type=int, help='Quantidade necessária de especialistas para o 1º turno')
    parser.add_argument('qtd_necessaria_especialista_2_turno', type=int, help='Quantidade necessária de especialistas para o 2º turno')
    parser.add_argument('qtd_necessaria_especialista_3_turno', type=int, help='Quantidade necessária de especialistas para o 3º turno')

    # Parse the arguments
    args = parser.parse_args()

    return args

# Parse command-line arguments
args = parse_arguments()

# Access the arguments
qtd_total_disponivel_clinico = args.qtd_total_disponivel_clinico
qtd_total_disponivel_especialista = args.qtd_total_disponivel_especialista
qtd_necessaria_clinico_1_turno = args.qtd_necessaria_clinico_1_turno
qtd_necessaria_clinico_2_turno = args.qtd_necessaria_clinico_2_turno
qtd_necessaria_clinico_3_turno = args.qtd_necessaria_clinico_3_turno
qtd_necessaria_especialista_1_turno = args.qtd_necessaria_especialista_1_turno
qtd_necessaria_especialista_2_turno = args.qtd_necessaria_especialista_2_turno
qtd_necessaria_especialista_3_turno = args.qtd_necessaria_especialista_3_turno

qtd_necessaria_clinico_diario = qtd_necessaria_clinico_1_turno + qtd_necessaria_clinico_2_turno + qtd_necessaria_clinico_3_turno
qtd_necessaria_especialista_diario = qtd_necessaria_especialista_1_turno + qtd_necessaria_especialista_2_turno + qtd_necessaria_especialista_3_turno

def minimizar_turnos():
    # Cria o solver do tipo CLP (Linear Programming)
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Erro ao criar o solver.")
        return

    # Definir as variáveis de decisão: Xij
    # X = Quantidade
    # i = tipo de medico
      # 1 = clinico
      # 2 = especialista
    # j = tipo de turno
      # 1 = turno 1
      # 2 = turno 2
      # 3 = turno 3

    X11 = solver.IntVar(0, solver.infinity(), 'X11')
    X12 = solver.IntVar(0, solver.infinity(), 'X12')
    X13 = solver.IntVar(0, solver.infinity(), 'X13')
    X21 = solver.IntVar(0, solver.infinity(), 'X21')
    X22 = solver.IntVar(0, solver.infinity(), 'X22')
    X23 = solver.IntVar(0, solver.infinity(), 'X23')

    # Definir a função objetivo Z = 450*X11 + 900*X21 + 500*X12 + 1100*X22 + 550*X13 + 1200*X23
    solver.Minimize(450 * X11 + 900 * X21 + 500 * X12 + 1100 * X22 + 550 * X13 + 1200 * X23)

    # Definir as restrições
    solver.Add(X11 >= qtd_necessaria_clinico_1_turno)  # X11 >= 6
    solver.Add(X12 >= qtd_necessaria_clinico_2_turno)  # X12 >= 8
    solver.Add(X13 >= qtd_necessaria_clinico_3_turno)  # X13 >= 8
    solver.Add(X21 >= qtd_necessaria_especialista_1_turno)  # X21 >= 3
    solver.Add(X22 >= qtd_necessaria_especialista_2_turno)  # X22 >= 6
    solver.Add(X23 >= qtd_necessaria_especialista_3_turno)  # X23 >= 5

    # Adicionar as restrições de disponibilidade de médicos
    solver.Add(X11 + X12 + X13 == qtd_total_disponivel_clinico)  # Todos os clínicos gerais disponíveis devem ser alocados
    solver.Add(X21 + X22 + X23 == qtd_total_disponivel_especialista)  # Todos os especialistas disponíveis devem ser alocados

    # Restrição de mínimo diário
    solver.Add(X11 + X12 + X13 >= qtd_necessaria_clinico_diario) # Total de clinicos necessarios diarios
    solver.Add(X21 + X22 + X23 >= qtd_necessaria_especialista_diario) # Total de especialistas necessarios diarios

    # Resolver o problema
    status = solver.Solve()

    # Verificar se uma solução foi encontrada
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        result['status'] = 'OPTIMAL'
        result['X11'] = X11.solution_value()
        result['X12'] = X12.solution_value()
        result['X13'] = X13.solution_value()
        result['X21'] = X21.solution_value()
        result['X22'] = X22.solution_value()
        result['X23'] = X23.solution_value()
        result['Z'] = solver.Objective().Value()
    else:
        result['status'] = 'NOT_OPTIMAL'
        result['message'] = 'Não foi possível encontrar uma solução ótima.'

    return json.dumps(result)

# Chamar a função para resolver o problema
print(minimizar_turnos())
