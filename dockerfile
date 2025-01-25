# Usa uma imagem oficial do Python como base
FROM python:3.12

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app/

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Django
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
