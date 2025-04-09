import mediapipe as mp
mp_hands = mp.solutions.hands


def map_pontos_referencia(ponto_referencia):
    return {
        "WRIST": ponto_referencia.landmark[0],

        "THUMB_CMC": ponto_referencia.landmark[1],
        "THUMB_MCP": ponto_referencia.landmark[2],
        "THUMB_IP":  ponto_referencia.landmark[3],
        "THUMB_TIP": ponto_referencia.landmark[4],

        "INDEX_MCP": ponto_referencia.landmark[5],
        "INDEX_PIP": ponto_referencia.landmark[6],
        "INDEX_DIP": ponto_referencia.landmark[7],
        "INDEX_TIP": ponto_referencia.landmark[8],

        "MIDDLE_MCP": ponto_referencia.landmark[9],
        "MIDDLE_PIP": ponto_referencia.landmark[10],
        "MIDDLE_DIP": ponto_referencia.landmark[11],
        "MIDDLE_TIP": ponto_referencia.landmark[12],

        "RING_MCP": ponto_referencia.landmark[13],
        "RING_PIP": ponto_referencia.landmark[14],
        "RING_DIP": ponto_referencia.landmark[15],
        "RING_TIP": ponto_referencia.landmark[16],

        "PINKY_MCP": ponto_referencia.landmark[17],
        "PINKY_PIP": ponto_referencia.landmark[18],
        "PINKY_DIP": ponto_referencia.landmark[19],
        "PINKY_TIP": ponto_referencia.landmark[20],
    }

class Alfabeto:
    def letra_A(self, ponto):
        ponto = map_pontos_referencia(ponto)
        return (
            ponto["THUMB_TIP"].y < ponto["INDEX_TIP"].y and
            ponto["THUMB_TIP"].y < ponto["MIDDLE_TIP"].y and
            abs(ponto["THUMB_TIP"].x - ponto["WRIST"].x) > abs(ponto["INDEX_TIP"].x - ponto["WRIST"].x)
        )

    def letra_B(self, ponto):
        ponto = map_pontos_referencia(ponto)
        dedos_esticados = (
            ponto["INDEX_TIP"].y < ponto["INDEX_PIP"].y and
            ponto["MIDDLE_TIP"].y < ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y < ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y < ponto["PINKY_PIP"].y
        )
        polegar_cruzado = (
            min(ponto["INDEX_TIP"].x, ponto["RING_TIP"].x) < ponto["THUMB_TIP"].x < max(ponto["INDEX_TIP"].x, ponto["RING_TIP"].x)
        )
        return dedos_esticados and polegar_cruzado

    def letra_C(self, ponto):
        ponto = map_pontos_referencia(ponto)
        dedos_curvados = (
            ponto["INDEX_TIP"].y > ponto["INDEX_DIP"].y and
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_DIP"].y and
            ponto["RING_TIP"].y > ponto["RING_DIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_DIP"].y
        )
        abertura_minima = abs(ponto["THUMB_TIP"].x - ponto["INDEX_TIP"].x) >= 0.02
        polegar_lateral = (
            ponto["THUMB_TIP"].y >= ponto["INDEX_TIP"].y and
            ponto["THUMB_TIP"].y >= ponto["MIDDLE_TIP"].y and
            ponto["THUMB_TIP"].y >= ponto["RING_TIP"].y and
            ponto["THUMB_TIP"].y >= ponto["PINKY_TIP"].y
        )
        return dedos_curvados and abertura_minima and polegar_lateral

    def letra_D(self, ponto):
        ponto = map_pontos_referencia(ponto)
        indicador_esticado = ponto["INDEX_TIP"].y < ponto["INDEX_PIP"].y
        distancia_thumb_middle_mcp = ((ponto["THUMB_TIP"].x - ponto["MIDDLE_MCP"].x)**2 + (ponto["THUMB_TIP"].y - ponto["MIDDLE_MCP"].y)**2)**0.5
        polegar_proximo = distancia_thumb_middle_mcp < 0.06
        dedos_dobrados = (
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y > ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        )
        return indicador_esticado and polegar_proximo and dedos_dobrados

    def letra_E(self, ponto):
        ponto = map_pontos_referencia(ponto)
        dedos_fechados = (
            ponto["INDEX_TIP"].y > ponto["INDEX_PIP"].y and
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y > ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        )
        polegar_sobre_dedos = (
            ponto["THUMB_TIP"].y < ponto["INDEX_TIP"].y and
            ponto["THUMB_TIP"].y < ponto["MIDDLE_TIP"].y and
            ponto["THUMB_TIP"].y < ponto["RING_TIP"].y and
            ponto["THUMB_TIP"].y < ponto["PINKY_TIP"].y and
            abs(ponto["THUMB_TIP"].x - ponto["WRIST"].x) < 0.1
        )
        return dedos_fechados and polegar_sobre_dedos

    def letra_F(self, ponto):
        ponto = map_pontos_referencia(ponto)
        medio_esticado = ponto["MIDDLE_TIP"].y < ponto["MIDDLE_PIP"].y
        anelar_esticado = ponto["RING_TIP"].y < ponto["RING_PIP"].y
        mindinho_esticado = ponto["PINKY_TIP"].y < ponto["PINKY_PIP"].y
        distancia_thumb_index_mcp = ((ponto["THUMB_TIP"].x - ponto["INDEX_MCP"].x)**2 + (ponto["THUMB_TIP"].y - ponto["INDEX_MCP"].y)**2)**0.5
        polegar_proximo = distancia_thumb_index_mcp < 0.1
        return medio_esticado and anelar_esticado and mindinho_esticado and polegar_proximo

    def letra_G(self, ponto):
        ponto = map_pontos_referencia(ponto)
        indicador_esticado = ponto["INDEX_TIP"].y < ponto["INDEX_PIP"].y
        polegar_esticado = ponto["THUMB_TIP"].y < ponto["THUMB_IP"].y
        dedos_dobrados = (
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y > ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        )
        return indicador_esticado and polegar_esticado and dedos_dobrados

    def letra_H(self, ponto):
        ponto = map_pontos_referencia(ponto)
        indicador_esticado = ponto["INDEX_TIP"].y < ponto["INDEX_PIP"].y
        medio_esticado = ponto["MIDDLE_TIP"].y < ponto["MIDDLE_PIP"].y
        anelar_dobrado = ponto["RING_TIP"].y > ponto["RING_PIP"].y
        mindinho_dobrado = ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        polegar_dobrado = ponto["THUMB_TIP"].y > ponto["THUMB_IP"].y
        return indicador_esticado and medio_esticado and anelar_dobrado and mindinho_dobrado and polegar_dobrado

    def letra_I(self, ponto):
        ponto = map_pontos_referencia(ponto)
        return ponto["PINKY_TIP"].y < ponto["PINKY_PIP"].y

    def letra_J(self, ponto):
        ponto = map_pontos_referencia(ponto)
        return ponto["PINKY_TIP"].y < ponto["PINKY_PIP"].y and ponto["THUMB_TIP"].x < ponto["THUMB_CMC"].x

    def letra_K(self, ponto):
        ponto = map_pontos_referencia(ponto)
        indicador_esticado = ponto["INDEX_TIP"].y < ponto["INDEX_PIP"].y
        medio_esticado = ponto["MIDDLE_TIP"].y < ponto["MIDDLE_PIP"].y
        polegar_posicionado = ponto["THUMB_TIP"].x > ponto["INDEX_TIP"].x
        return indicador_esticado and medio_esticado and polegar_posicionado

    def letra_L(self, ponto):
        ponto = map_pontos_referencia(ponto)
        indicador_esticado = ponto["INDEX_TIP"].y < ponto["INDEX_PIP"].y
        distancia_lateral = abs(ponto["THUMB_TIP"].x - ponto["INDEX_TIP"].x) > 0.1
        dedos_dobrados = (
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y > ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        )
        return indicador_esticado and distancia_lateral and dedos_dobrados

    def letra_M(self, ponto):
        ponto = map_pontos_referencia(ponto)
        dedos_dobrados = (
            ponto["INDEX_TIP"].y > ponto["INDEX_PIP"].y and
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y > ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        )
        polegar_sob_dedos = (
            ponto["THUMB_TIP"].y > ponto["INDEX_PIP"].y and
            ponto["THUMB_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["THUMB_TIP"].y > ponto["RING_PIP"].y
        )
        return dedos_dobrados and polegar_sob_dedos

    def letra_N(self, ponto):
        ponto = map_pontos_referencia(ponto)
        dedos_dobrados = (
            ponto["INDEX_TIP"].y > ponto["INDEX_PIP"].y and
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_PIP"].y and
            ponto["RING_TIP"].y > ponto["RING_PIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_PIP"].y
        )
        margem = 0.02
        polegar_posicionado = (
            ponto["THUMB_TIP"].y > (ponto["INDEX_PIP"].y - margem) and
            ponto["THUMB_TIP"].y > (ponto["MIDDLE_PIP"].y - margem) and
            ponto["THUMB_TIP"].y < (ponto["RING_PIP"].y + margem)
        )
        return dedos_dobrados and polegar_posicionado

    def letra_O(self, ponto):
        ponto = map_pontos_referencia(ponto)
        dedos_curvados = (
            ponto["INDEX_TIP"].y > ponto["INDEX_DIP"].y and
            ponto["MIDDLE_TIP"].y > ponto["MIDDLE_DIP"].y and
            ponto["RING_TIP"].y > ponto["RING_DIP"].y and
            ponto["PINKY_TIP"].y > ponto["PINKY_DIP"].y
        )
        circulo_fechado = (
            abs(ponto["THUMB_TIP"].x - ponto["INDEX_TIP"].x) < 0.05 and
            abs(ponto["THUMB_TIP"].y - ponto["INDEX_TIP"].y) < 0.05
        )
        dedos_juntos = (
            abs(ponto["INDEX_TIP"].x - ponto["MIDDLE_TIP"].x) < 0.05 and
            abs(ponto["MIDDLE_TIP"].x - ponto["RING_TIP"].x) < 0.05 and
            abs(ponto["RING_TIP"].x - ponto["PINKY_TIP"].x) < 0.05
        )
        return dedos_curvados and circulo_fechado and dedos_juntos

    def letra_P(self, ponto):
        ponto = map_pontos_referencia(ponto)
        index_extended = abs(ponto["INDEX_TIP"].y - ponto["WRIST"].y) > abs(ponto["INDEX_MCP"].y - ponto["WRIST"].y)
        middle_extended = abs(ponto["MIDDLE_TIP"].y - ponto["WRIST"].y) > abs(ponto["MIDDLE_MCP"].y - ponto["WRIST"].y)
        index_middle_extended = index_extended and middle_extended
        dedos_lado = abs(ponto["INDEX_TIP"].x - ponto["MIDDLE_TIP"].x) > 0.05
        thumb_curvado = ponto["THUMB_TIP"].y > ponto["THUMB_IP"].y
        ring_curvado = ponto["RING_TIP"].y > ponto["RING_DIP"].y
        pinky_curvado = ponto["PINKY_TIP"].y > ponto["PINKY_DIP"].y
        outros_fechados = thumb_curvado and ring_curvado and pinky_curvado
        return index_middle_extended and dedos_lado and outros_fechados
