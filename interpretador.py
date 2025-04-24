from pong_game import PongGame

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
        self.class_defined = False

    def carregar_script(self):
        with open(self.script_path, 'r', encoding='utf-8') as f:
            self.commands = [linha.strip() for linha in f if linha.strip()]

    def analisar_lexica(self, linha):
        return linha.lower().split()

    def analisar_sintatica(self, tokens):
        if tokens[0] == 'classe' and 'ponggame' in tokens[1]:
            self.class_defined = True
            return 'classe PongGame'
        elif tokens[0] == 'met' and len(tokens) == 2:
            metodo = tokens[1].replace(' ', '_').strip()
            if metodo in self.command_map:
                return f'met {metodo}'
        raise SyntaxError(f"Comando inválido ou mal formatado: {' '.join(tokens)}")

    def analisar_semantica(self, comando):
        if comando == 'classe PongGame':
            self.game = PongGame()
            return None
        metodo_chave = comando.replace('met ', '')
        metodo_real = self.command_map.get(metodo_chave)
        if not hasattr(self.game, metodo_real):
            raise AttributeError(f"Método '{metodo_real}' não encontrado no jogo.")
        return metodo_real

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
