# 🤟 Tradutor de Libras Interativo 

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5%2B-orange)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.9%2B-yellowgreen)](https://mediapipe.dev/)

**Projeto que traduz gestos de Libras para texto e voz em tempo real!**  
*Desenvolvido como projeto acadêmico da FIAP*

---
## 👥 Autores

| Nome                          | RM      | 
|-------------------------------|---------|
| **Fabiano Luiz Santos**       | 96044   | 
| **Luigi de Jesus Felice**     | 94546   | 
| **Pedro de Sousa Dutra**      | 96167   | 
| **Victor Moura Ventura**      | 93509   | 

---

## ✨ Funcionalidades Incríveis

- **Tradução de 13 letras**: A, B, C, D, E, F, G, I, L, M, N, O, P
- **Síntese de voz integrada** com fila de processamento
- **Easter Eggs Especiais**:
  - 🎓 `FIAP` → Mostra logo + voz
  - 🤙 `EAE` → Exibe meme interativo + voz
- **Interface profissional**:
  - ✔️ Preview da câmera em miniatura
  - ✔️ Temporizador para próxima letra
  - ✔️ Feedback visual de limpeza
- **Controle por gestos**:
  - ✋ Uma mão → Formação de letras
  - ✌️ Duas mãos abertas → Limpa frase
  - `Tecla Q`: Encerra o aplicativo

---

## 🛠 Tecnologias Utilizadas

| Tecnologia       | Função                                | 
|------------------|---------------------------------------|
| `MediaPipe`      | Rastreamento preciso de mãos         |
| `OpenCV`         | Processamento de imagem em tempo real|
| `pyttsx3`        | Conversão texto-voz                  |
| `Threading`      | Processamento assíncrono             |

---

## 🗂 Estrutura de Arquivos

```plaintext
📂 projeto/
├── 📁 images/        # Armazena imagens dos easter eggs
│   ├── fiap.png      # Logo da FIAP
│   └── eae.png       # Imagem do meme "EAE"
├── 📁 util/          # Lógica de reconhecimento
│   └── Alfabeto.py   # Detecção de gestos por letra
└── main.py           # Script principal do sistema
```

## 🚀 Execução

1. **Instale as dependências**:
   ```bash
   pip install opencv-python mediapipe pyttsx3 numpy
   ```

2. **Inicie o sistema**:
   ```bash
   python main.py
   ```

## 🧠 Lógica-Chave

**Sistema de Fila para Voz**:
```python
def thread_fala():
    while True:
        texto = fila_fala.get()
        if texto is None: break
        voz.say(texto)
        voz.runAndWait()
```

**Detecção de Letras**:
```python
if alfabeto.letra_A(hand): letra = "A"
elif alfabeto.letra_B(hand): letra = "B"  # ... e assim por diante
```

**Easter Egg 'EAE'**:
```python
if frase == "EAE":
    output[100:300, 220:420] = eae_sem_fundo
    falar("EAE Galera!")
```

## 💡 Dicas de Uso

1. **Iluminação**: Use ambiente bem iluminado
2. **Posicionamento**: Mantenha as mãos na área central da câmera
3. **Timing**: Aguarde 2 segundos entre gestos diferentes
4. **Reset Rápido**: Faça gesto ✌️ com duas mãos para limpar

---
