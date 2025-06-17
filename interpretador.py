from pong_game import PongGame
import ast

class PongInterpreter:
    def __init__(self, script_path):
        self.script_path = script_path
        self.commands = []
        self.command_map = {
            'iniciar_objetos': 'init_objects',
            'reiniciar_bola': 'reset_ball',
            'lidar_eventos': 'handle_events',
            'lidar_entrada': 'handle_input',
            'atualizar_bola': 'update_ball',
            'desenhar': 'draw',
            'executar': 'run'
        }
        self.game = None
        self.allowed_vars = [
            'WIDTH', 'HEIGHT', 'BALL_SPEED', 'PADDLE_SPEED', 'SPEED_INCREMENT',
            'COLOR', 'BACKGROUND', 'FPS'
        ]

    def carregar_script(self):
        with open(self.script_path, 'r', encoding='utf-8') as f:
            self.commands = [linha.strip() for linha in f if linha.strip() and not linha.strip().startswith('#')]

    def analisar_lexica(self, linha):
        return linha.split()

    def analisar_sintatica(self, tokens):
        if tokens[0] == 'classe' and 'PongGame' in tokens[1]:
            return {'tipo': 'classe', 'nome': 'PongGame'}
        elif tokens[0] == 'met' and len(tokens) == 2:
            metodo = tokens[1].strip()
            if metodo in self.command_map:
                return {'tipo': 'metodo', 'nome': metodo}
            else:
                raise SyntaxError(f"Método '{tokens[1]}' não reconhecido.")
        elif tokens[0] == 'var' and '=' in tokens:
            resto = ' '.join(tokens[1:])
            nome, valor = resto.split('=', 1)
            return {'tipo': 'variavel', 'nome': nome.strip().upper(), 'valor': valor.strip()}
        elif tokens[0] == 'imprimir':
            valor = ' '.join(tokens[1:])
            return {'tipo': 'imprimir', 'mensagem': valor}
        else:
            raise SyntaxError(f"Comando inválido ou mal formatado: {' '.join(tokens)}")

    def analisar_semantica(self, comando):
        if comando['tipo'] == 'classe':
            self.game = PongGame()
        elif comando['tipo'] == 'metodo':
            metodo_real = self.command_map.get(comando['nome'])
            if not hasattr(self.game, metodo_real):
                raise AttributeError(f"Método '{metodo_real}' não encontrado no jogo.")
            return metodo_real
        elif comando['tipo'] == 'variavel':
            nome = comando['nome']
            if nome not in self.allowed_vars:
                raise NameError(f"Variável '{nome}' não é permitida.")
            try:
                valor_avaliado = ast.literal_eval(comando['valor'])
            except Exception:
                raise ValueError(f"Valor inválido para a variável '{nome}'.")
            setattr(self.game, nome, valor_avaliado)
        elif comando['tipo'] == 'imprimir':
            msg = comando['mensagem']
            try:
                if msg.upper() in self.allowed_vars:
                    print(getattr(self.game, msg.upper()))
                else:
                    print(ast.literal_eval(msg))
            except:
                print(msg.strip('"'))

    def executar(self):
        self.carregar_script()
        for linha in self.commands:
            tokens = self.analisar_lexica(linha)
            comando = self.analisar_sintatica(tokens)
            metodo = self.analisar_semantica(comando)
            if metodo:
                getattr(self.game, metodo)()

if __name__ == "__main__":
    interpretador = PongInterpreter("script.pgs")
    interpretador.executar()