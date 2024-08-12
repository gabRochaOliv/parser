import csv

class LL1Parser:
    def __init__(self, table_file):
        self.table = self.read_ll1_table(table_file)
        self.non_terminals = self.table[0][1:]
        self.terminals = [row[0] for row in self.table[1:]]
        self.table_dict = self.create_table_dict()

    def read_ll1_table(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            table = []
            for row in reader:
                table.append([cell.strip() for cell in row])  # Remove espaços em branco
            return table

    def create_table_dict(self):
        table_dict = {}
        for i, non_terminal in enumerate(self.non_terminals):
            table_dict[non_terminal] = {}
            for j, terminal in enumerate(self.terminals):
                production = self.table[j + 1][i + 1]
                if production:  # Verifica se a célula não está vazia
                    parts = production.split(" -> ")
                    if len(parts) == 2:
                        rhs = parts[1].split() if parts[1] != 'empty' else []  # Trata "empty" como lista vazia
                        table_dict[non_terminal][terminal] = rhs
                        print(f"Adicionado: {non_terminal} -> {rhs} para terminal {terminal}")
                    else:
                        print(f"Erro ao processar a produção: '{production}' na linha {j+2}, coluna {i+2}")
        return table_dict

    def parse(self, input_string):
        input_tokens = input_string.split() + ['$']
        stack = ['$', 'E']  # Supondo que 'E' é o símbolo inicial

        print("Parsing started:")
        while stack:
            top = stack.pop()
            current_input = input_tokens[0]
            print(f"Top of stack: {top}, Current input: {current_input}")

            if top in self.non_terminals:
                if current_input in self.table_dict[top]:
                    production = self.table_dict[top][current_input]
                    print(f"Produção encontrada para {top} com {current_input}: {production}")
                    if production:
                        stack.extend(reversed(production))
                    else:
                        print(f"Erro de sintaxe: não há produção para '{top}' com o terminal '{current_input}'")
                        return False
                else:
                    print(f"Erro de sintaxe: não há entrada na tabela para '{top}' com o terminal '{current_input}'")
                    return False
            elif top == current_input:
                print(f"Match: {top}")
                input_tokens.pop(0)
            else:
                print(f"Erro de sintaxe: esperado '{top}' mas encontrado '{current_input}'")
                return False
        
        if input_tokens == ['$']:
            print("Entrada aceita com sucesso.")
            return True
        else:
            print("Erro de sintaxe: entrada não consumida completamente.")
            return False

if __name__ == "__main__":
    parser = LL1Parser('ll1_table.csv')
    
    with open('input.txt', 'r') as file:
        input_string = file.read().strip()
    
    parser.parse(input_string)
