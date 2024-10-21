class BaseConhecimento:
    navs_normal = {
        'Chrome': ('V', 'F', 'F', 4, 1, ('linux', 'macos', 'windows', 'ios', 'android')),
        'Ungoogled Chromium': ('F', 'F', 'V', 5, 5, ('linux', 'macos', 'windows')),
        'Edge': ('V', 'F', 'F', 2, 2, ('linux', 'macos', 'windows', 'ios', 'android')),
        'Firefox': ('V', 'V', 'V', 5, 4, ('linux', 'macos', 'windows', 'ios', 'android')),
        'Mullvad': ('F', 'V', 'V', 5, 5, ('linux', 'macos', 'windows')),
        'Librewolf': ('F', 'V', 'V', 5, 5, ('linux', 'macos', 'windows')),
        'Opera': ('V', 'V', 'V', 3, 3, ('linux', 'macos', 'windows')),
        'Safari': ('V', 'F', 'F', 2, 1, ('ios', 'macos')),
        'Brave': ('V', 'F', 'V', 5, 5, ('linux', 'macos', 'windows', 'ios', 'android')),
        'Bromite': ('F', 'V', 'V', 4, 4, ('android')),
        'Cromite': ('F', 'V', 'V', 4, 5, ('windows', 'linux', 'android')),
        'Firefox Focus': ('V', 'V', 'V', 5, 5, ('android', 'ios')),
    }

    navs_leve = {
        'Pale Moon': ('V', 'V', ('linux', 'macos', 'windows')),
        'Falkon': ('V', 'V', ('linux')),
        'qutebrowser': ('F', 'V', ('linux', 'macos', 'windows')),
        'surf': ('F', 'V', ('linux')),
        'browsh': ('F', 'V', ('linux', 'macos')),
        'Emacs Web Wowser (ewww)': ('F', 'F', ('linux')),
        'ELinks': ('F', 'F', ('linux', 'dos', 'windows')),
    }

class EngineRegras:

    # Faz um matching baseado nas respostas qualitativas
    def equiparar_qualitativos_normal(self, respostas):
        candidatos = []
        for chave, valor in BaseConhecimento.navs_normal.items():
            if (
                respostas['nerdice'] == valor[0].lower() and
                respostas['anuncios'] == valor[1].lower() and
                respostas['open_source'] == valor[2].lower() and
                respostas['so'] in valor[5]
            ):
                candidatos.append(chave)
        return candidatos
            
    def equiparar_qualitativos_leve(self, respostas):
        candidatos = []
        for chave, valor in BaseConhecimento.navs_leve.items():
            if (
                respostas['usar_mouse'] == valor[0].lower() and
                respostas['renderizar_css_js'] == valor[1].lower() and
                respostas['so'] in valor[2]
            ):
                candidatos.append(chave)
        return candidatos

    # Calcula a confianca ponderada para navegadores normais
    def calcular_confianca_normal(self, respostas, navegador_info):
        peso_extensoes = abs(respostas['extensoes'] - navegador_info[3]) / 5
        peso_privacidade = abs(respostas['privacidade'] - navegador_info[4]) / 5
        confianca = (1 - (peso_extensoes + peso_privacidade) / 2) * 100
        return confianca

    def calcular_confianca_leve(self):
        return 100  # Para navegadores leves, não temos fatores quantitativos, então é fixo no 100%
    
    def achar_maior_confianca(self, candidatos_qualitativos, respostas, leve):
        melhores_navegadores = []
        maior_confianca = 0
        navegadores = BaseConhecimento.navs_leve if leve else BaseConhecimento.navs_normal
        
        for nome in candidatos_qualitativos:
            info = navegadores[nome]
            confianca = self.calcular_confianca_leve() if leve else self.calcular_confianca_normal(respostas, info)
            if confianca > maior_confianca:
                melhores_navegadores = [nome]  # Novo melhor, limpa a lista
                maior_confianca = confianca
            elif confianca == maior_confianca:
                melhores_navegadores.append(nome)  # Empate na confianca, adiciona à lista

        return melhores_navegadores, maior_confianca

def diagnosticar():
    engine = EngineRegras()
    print("Olá! Eu serei o seu recomendador de navegadores. Responda as perguntas seguintes de acordo com a especificação: ")

    # Perguntas e respostas
    minimalista = input("Eu quero um navegador mais leve/minimalista que o normal (V/F): ").strip().lower() == 'v'

    if minimalista:
        usar_mouse = input("Eu quero usar um mouse para navegar (V/F): ").strip().lower()
        renderizar_css_js = input("É importante que meu navegador consiga renderizar CSS e JavaScript (V/F): ").strip().lower()
        sistema_operacional = input("O sistema operacional que estou usando é: ").strip().lower()

        respostas = {
            'usar_mouse': usar_mouse,
            'renderizar_css_js': renderizar_css_js,
            'so': sistema_operacional
        }

        leve = True

    else:
        nerdice = input("Eu não quero parecer um nerd/quero usar esse navegador no notebook da firma (V/F): ").strip().lower()
        anuncios = input("É importante que meu navegador consiga filtrar o máximo de anúncios, agora e no futuro (V/F): ").strip().lower()
        open_source = input("É importante que meu navegador seja open-source (V/F): ").strip().lower()
        extensoes = int(input("Eu me importo com o suporte para extensões no meu navegador (de 0 a 5): ").strip())
        privacidade = int(input("Eu me importo com a privacidade dos meus dados (de 0 a 5): ").strip())
        sistema_operacional = input("O sistema operacional que estou usando é: ").strip().lower()

        respostas = {
            'nerdice': nerdice,
            'anuncios': anuncios,
            'open_source': open_source,
            'extensoes': extensoes,
            'privacidade': privacidade,
            'so': sistema_operacional
        }

        leve = False

    candidatos_qualitativos = (
        engine.equiparar_qualitativos_leve(respostas) 
        if leve 
        else engine.equiparar_qualitativos_normal(respostas)
    )
    
    navegadores_recomendados, confianca = engine.achar_maior_confianca(candidatos_qualitativos, respostas, leve)
    
    if navegadores_recomendados:
        recomendacoes = " OU ".join(navegadores_recomendados)
        print(f"Recomendamos os navegadores: {recomendacoes} com uma confiança de {confianca:.2f}%.")
    else:
        print("Não foi possível encontrar um navegador adequado com base nas suas preferências.")

if __name__ == "__main__":
    diagnosticar()
