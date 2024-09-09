class SemanticAnalyzer:
    def __init__(self, tokens, symbol_table):
        self.tokens = tokens
        self.symbol_table = symbol_table
        self.errors = []
        self.current_token_index = 0

    def analyze(self):

        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.check_token(token)
            self.current_token_index += 1

        if self.errors:
            print("Erros Semânticos:")
            for error in self.errors:
                print(error)
        else:
            print("Análise Semântica concluída sem erros.")

    def check_token(self, token):

        if token.token_type in ["INT", "BOOL", "VOID"]:
            self.declare_variables(token)

        elif token.token_type == "ID":
            symbol = self.symbol_table.get_symbol(token.value)
            if symbol is None:
                self.errors.append(f"Erro: A variável ou função '{token.value}' foi usada antes de ser declarada na linha {token.line}.")
            elif symbol.get("type") == "undefined":
                self.errors.append(f"Erro: A variável ou função '{token.value}' foi usada sem um tipo definido na linha {token.line}.")

        elif token.token_type == "ASSIGN":
            self.check_assignment(token)

    def declare_variables(self, type_token):

        self.current_token_index += 1 
        while self.current_token().token_type == "ID":
            var_token = self.current_token()
            name = var_token.value
            print(f"Declarando variável '{name}' com tipo '{type_token.token_type.lower()}'")

            if self.current_token_index + 1 < len(self.tokens):
                next_token = self.tokens[self.current_token_index + 1]
                if next_token.token_type == "LPAREN":
                    self.declare_function(type_token, var_token)
                    break

            if name in self.symbol_table.symbols:
                self.symbol_table.symbols[name]['type'] = type_token.token_type.lower()
            else:
                self.symbol_table.symbols[name] = {
                    "type": type_token.token_type.lower(),
                    "value": None,
                    "scope": "global",
                    "line": var_token.line,
                    "column": var_token.column
                }

            self.current_token_index += 1  
            if self.current_token().token_type == "SEMICOLON":
                break
            elif self.current_token().token_type == "COMMA":
                self.current_token_index += 1  

    def declare_function(self, type_token, function_token):

        print(f"Declarando função '{function_token.value}' com tipo '{type_token.token_type.lower()}'")
        self.symbol_table.symbols[function_token.value] = {
            "type": type_token.token_type.lower(),
            "parameters": []
        }

        self.current_token_index += 2  

        while self.current_token().token_type != "RPAREN":
            param_type = self.current_token()
            self.current_token_index += 1  
            param_name = self.current_token()

            print(f"Registrando parâmetro '{param_name.value}' com tipo '{param_type.token_type.lower()}' para a função '{function_token.value}'")
            self.symbol_table.symbols[function_token.value]["parameters"].append({
                "name": param_name.value,
                "type": param_type.token_type.lower()
            })

            if param_name.value in self.symbol_table.symbols:
                self.symbol_table.symbols[param_name.value]['type'] = param_type.token_type.lower()
            else:
                self.symbol_table.symbols[param_name.value] = {
                    "type": param_type.token_type.lower(),
                    "value": None,
                    "scope": "local",
                    "line": param_name.line,
                    "column": param_name.column
                }

            self.current_token_index += 1  
            if self.current_token().token_type == "COMMA":
                self.current_token_index += 1  

    def check_assignment(self, token):

        var_name_token = self.tokens[self.current_token_index - 1]
        if var_name_token.token_type == "ID":
            var_symbol = self.symbol_table.get_symbol(var_name_token.value)
            if var_symbol:
                assigned_value_token = self.tokens[self.current_token_index + 1]

                if assigned_value_token.token_type == "FUN":
                    function_token = self.tokens[self.current_token_index + 2]
                    self.check_function_call(var_name_token, function_token)

                elif assigned_value_token.token_type == "ID":
                    assigned_symbol = self.symbol_table.get_symbol(assigned_value_token.value)
                    if assigned_symbol and var_symbol["type"] != assigned_symbol["type"]:
                        self.errors.append(f"Erro: Atribuição inválida entre tipos '{var_symbol['type']}' e '{assigned_symbol['type']}' na linha {token.line}.")
                elif var_symbol["type"] == "int" and assigned_value_token.token_type != "NUMBER":
                    self.errors.append(f"Erro: Atribuição inválida para a variável '{var_name_token.value}' do tipo 'int' na linha {token.line}.")
                elif var_symbol["type"] == "bool" and assigned_value_token.token_type not in ["TRUE", "FALSE"]:
                    self.errors.append(f"Erro: Atribuição inválida para a variável '{var_name_token.value}' do tipo 'bool' na linha {token.line}.")
        else:
            raise RuntimeError(f"Atribuição inesperada na linha {token.line}")

    def check_function_call(self, var_name_token, fun_token):

        function_symbol = self.symbol_table.get_symbol(fun_token.value)  # Verifica o nome real da função
        if not function_symbol:
            self.errors.append(f"Erro: Função '{fun_token.value}' chamada na linha {fun_token.line} não foi declarada.")
            return

        if function_symbol["type"] != self.symbol_table.get_symbol(var_name_token.value)["type"]:
            self.errors.append(f"Erro: O tipo de retorno da função '{fun_token.value}' é incompatível com o tipo da variável '{var_name_token.value}' na linha {fun_token.line}.")

        self.current_token_index += 3  

        params_passed = []
        while self.current_token().token_type != "RPAREN":  
            if self.current_token().token_type not in ["COMMA", "LPAREN", "RPAREN"]:
                params_passed.append(self.current_token())
            self.current_token_index += 1

        expected_params = function_symbol.get("parameters", [])
        if len(params_passed) != len(expected_params):
            self.errors.append(f"Erro: Número de parâmetros incorreto para a função '{fun_token.value}' na linha {fun_token.line}. Esperado {len(expected_params)}, mas recebido {len(params_passed)}.")
        else:
            for param, passed_param in zip(expected_params, params_passed):
                passed_param_type = "undefined"
                if passed_param.token_type == "NUMBER":
                    passed_param_type = "int"
                elif passed_param.token_type == "ID":
                    param_symbol = self.symbol_table.get_symbol(passed_param.value)
                    if param_symbol:
                        passed_param_type = param_symbol["type"]

                if passed_param_type != param["type"]:
                    self.errors.append(f"Erro: Tipo incompatível para o parâmetro '{param['name']}' da função '{fun_token.value}' na linha {fun_token.line}. Esperado '{param['type']}', mas recebido '{passed_param_type}'.")

    def current_token(self):
        return self.tokens[self.current_token_index]
