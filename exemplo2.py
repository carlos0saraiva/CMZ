# robot_aspirador.py
# Agente reativo baseado em modelo: mantém um mapa de células limpas (M)
# g(est_antigo, ação, perceção) -> actualiza estado interno
# f(estado) -> escolhe ação

from enum import Enum

class Action(Enum):
    NORTH = 'N'
    EAST  = 'E'
    SOUTH = 'S'
    WEST  = 'W'
    STAY  = 'STAY'

DIRS = {
    Action.NORTH: (-1, 0),
    Action.EAST:  (0, 1),
    Action.SOUTH: (1, 0),
    Action.WEST:  (0, -1),
}

class RobotVacuum:
    def __init__(self, rows=3, cols=3, start=(1,1), pref_order=None):
        self.rows = rows
        self.cols = cols
        self.pos = start  # (x, y)
        # mapa de cobertura: 1 = limpo, 0 = sujo
        self.M = [[0 for _ in range(cols)] for _ in range(rows)]
        # marcar a posição inicial como limpa (exemplo do PDF)
        x,y = start
        self.M[x][y] = 1
        # ordem de preferência: Norte, Este, Sul, Oeste por defeito
        self.pref_order = pref_order or [Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST]

    def percepcao_paredes(self):
        """Sensores que dizem se há parede em cada direção (True se há parede)."""
        x,y = self.pos
        walls = {}
        for d, (dx,dy) in DIRS.items():
            nx, ny = x+dx, y+dy
            walls[d] = not (0 <= nx < self.rows and 0 <= ny < self.cols)
        return walls

    def g_update_state(self, action, perception):
        """Atualiza o estado interno após executar ação e receber perceção (ex: colisão)."""
        # percepção é um dict 'wall hit' ou similar; assumimos percepcao indica se colisão ocorreu
        if action in DIRS:
            dx,dy = DIRS[action]
            x,y = self.pos
            nx, ny = x+dx, y+dy
            # se não bateu em parede -> move e marca célula como limpa
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                self.pos = (nx, ny)
                self.M[nx][ny] = 1
                return True
            else:
                # colisão: mantém posição
                return False
        return False

    def f_select_action(self):
        """Escolhe ação baseada no estado interno (mapa M) e perceções superficiais."""
        x,y = self.pos
        # Primeiro, preferir mover para células não limpas (M == 0) na ordem de preferência
        for d in self.pref_order:
            dx,dy = DIRS[d]
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                if self.M[nx][ny] == 0:
                    return d
        # Se não encontrou célula não limpa adjacente, tentar mover para qualquer vizinho livre
        for d in self.pref_order:
            dx,dy = DIRS[d]
            nx, ny = x+dx, y+dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols:
                return d
        return Action.STAY

    def all_clean(self):
        return all(self.M[i][j] == 1 for i in range(self.rows) for j in range(self.cols))

    def print_state(self):
        x,y = self.pos
        print("Mapa (1=limpo,0=sujo):")
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                if (i,j) == (x,y):
                    row += f"[R]{self.M[i][j]}"
                else:
                    row += f" {self.M[i][j]} "
            print(row)
        print()

if __name__ == "__main__":
    robot = RobotVacuum(rows=3, cols=3, start=(1,1))
    max_steps = 50
    print("Simulação Robot Aspirador (3x3) — ordem preferida: Norte, Este, Sul, Oeste\n")
    robot.print_state()

    for step in range(max_steps):
        if robot.all_clean():
            print(f"Todas as células limpas após {step} passos.")
            break
        action = robot.f_select_action()
        if action == Action.STAY:
            print("Nenhuma ação possível — parado.")
            break
        # percepcao de paredes (simples) — neste modelo usamos apenas limites da grelha
        walls = robot.percepcao_paredes()
        moved = robot.g_update_state(action, walls)
        print(f"Passo {step+1}: ação escolhida: {action.name} -> moveu? {moved} | posição: {robot.pos}")
        robot.print_state()
    else:
        print("Fim de passos (max_steps). Estado final:")
        robot.print_state()
