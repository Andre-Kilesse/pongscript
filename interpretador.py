from pong_game import PongGame
import ast

class PongInterpreter:
    def __init__(self, script_path):
        self.script_path = script_path
        self.commands = []
        self.command_map = {
            'inicializar_jogo': 'init_objects',
            'reposicionar_bola': 'reset_ball',
            'verificar_eventos': 'handle_events',
            'controlar_jogador': 'handle_input',
            'mover_bola': 'update_ball',
            'renderizar_tela': 'draw',
            'rodar_jogo': 'run'
        }
        self.game = None
        self.class_defined = False
        self.allowed_vars = [
            'WIDTH', 'HEIGHT', 'BALL_SPEED', 'PADDLE_SPEED',
            'SPEED_INCREMENT', 'COLOR'
        ]

    def carregar_script(self):
        with open(self.script_path, 'r', encoding='utf-8') as f:
            self.commands = [linha.strip() for linha in f if linha.strip()]

    def analisar_lexica(self, linha):
        return linha.split()

    def analisar_sintatica(self, tokens):
        if tokens[0] == 'classe' and 'PongGame' in tokens[1]:
            self.class_defined = True
            return 'classe PongGame'
        elif tokens[0] == 'met' and len(tokens) == 2:
            metodo = tokens[1].strip()
            if metodo in self.command_map:
                return f'met {metodo}'
        elif tokens[0] == 'var' and '=' in tokens:
            return ' '.join(tokens)
        raise SyntaxError(f"Comando inválido ou mal formatado: {' '.join(tokens)}")

    def analisar_semantica(self, comando):
        if comando == 'classe PongGame':
            self.game = PongGame()
            return None
        elif comando.startswith('met '):
            metodo_chave = comando.replace('met ', '')
            metodo_real = self.command_map.get(metodo_chave)
            if not hasattr(self.game, metodo_real):
                raise AttributeError(f"Método '{metodo_real}' não encontrado no jogo.")
            return metodo_real
        elif comando.startswith('var '):
            nome, valor = comando[4:].split('=', 1)
            nome = nome.strip().upper()
            if nome not in self.allowed_vars:
                raise NameError(f"Variável '{nome}' não é permitida.")
            try:
                valor_avaliado = ast.literal_eval(valor.strip())
            except Exception:
                raise ValueError(f"Valor inválido para a variável '{nome}'.")
            setattr(self.game, nome, valor_avaliado)
            return None

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
