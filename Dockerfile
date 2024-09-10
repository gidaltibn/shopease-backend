# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Definir a variável de ambiente para desativar o modo de depuração (produção)
ENV FLASK_ENV=production

# Expor a porta 5000 para o Flask
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["flask", "run", "--host=0.0.0.0"]
