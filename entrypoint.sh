#!/bin/sh

# Aguarda a confirmação da disponibilidade do banco de dados antes de prosseguir com a inicialização da aplicação.
echo "Aguardando a disponibilidade do banco de dados..."
while ! python -c "import psycopg2; psycopg2.connect(host='${DB_HOST:-db}', port='${DB_PORT:-5432}', user='${DB_USER}', password='${DB_PASSWORD}', dbname='${DB_NAME}')" 2>/dev/null; do
  echo "Banco de dados indisponível - aguardando"
  sleep 1
done

echo "Banco de dados disponível - executando operações subsequentes"

# Realiza a aplicação das migrações do banco de dados para garantir a consistência do esquema conforme definido pelos modelos da aplicação.
python manage.py migrate

# Coleta os arquivos estáticos (CSS, JS, imagens) dos apps instalados, incluindo o admin do Django.
python manage.py collectstatic --noinput

# Inicia o servidor de desenvolvimento do Django, disponibilizando-o em todos os interfaces de rede do contêiner, na porta 8000.
python manage.py runserver 0.0.0.0:8000
