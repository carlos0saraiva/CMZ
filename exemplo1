# termostato.py
# Agente reativo simples: f(perceção) -> ação
# Ação: "Ligar Aquecedor", "Desligar Aquecedor", "Manter Estado"

class ThermostatAgent:
    def __init__(self, desired_temp=20.0, delta=1.0):
        self.desired = desired_temp
        self.delta = delta
        self.heater_on = False  # estado atual do atuador

    def f(self, temp_atual):
        """Função de decisão do agente reativo."""
        lower = self.desired - self.delta
        upper = self.desired + self.delta
        if temp_atual < lower:
            return "Ligar Aquecedor"
        elif temp_atual > upper:
            return "Desligar Aquecedor"
        else:
            return "Manter Estado"

    def step(self, temp_atual):
        action = self.f(temp_atual)
        if action == "Ligar Aquecedor":
            self.heater_on = True
        elif action == "Desligar Aquecedor":
            self.heater_on = False
        # Manter Estado -> não altera heater_on
        return action

if __name__ == "__main__":
    # Simulação simples com leituras de temperatura
    agent = ThermostatAgent(desired_temp=20.0, delta=1.0)
    readings = [18.5, 19.0, 20.0, 21.5, 20.2, 19.3, 18.9]

    print("Simulação Termóstato")
    for t in readings:
        action = agent.step(t)
        print(f"Temp: {t:0.1f} °C -> Ação: {action} | Aquecedor ligado? {agent.heater_on}")
