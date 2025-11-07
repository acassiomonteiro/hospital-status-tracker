#!/bin/sh

# Aguarda a confirmação da disponibilidade do banco de dados antes de prosseguir com a inicialização da aplicação.
echo "Aguardando a disponibilidade do banco de dados..."
while ! python -c "import psycopg2; psycopg2.connect(host='${DB_HOST:-db}', port='${DB_PORT:-5432}', user='${DB_USER}', password='${DB_PASSWORD}', dbname='${DB_NAME}')" 2>/dev/null; do
  echo "Banco de dados indisponível - aguardando"
  sleep 1
done

echo "Banco de dados disponível - executando operações subsequentes"

# Gera automaticamente os arquivos de migration para mudanças nos models
echo "Criando migrations..."
python manage.py makemigrations --noinput

# Realiza a aplicação das migrações do banco de dados para garantir a consistência do esquema conforme definido pelos modelos da aplicação.
echo "Aplicando migrations..."
python manage.py migrate --noinput

# Coleta os arquivos estáticos (CSS, JS, imagens) dos apps instalados, incluindo o admin do Django.
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput


# Verifica se as variáveis de superusuário estão definidas antes de tentar criar o superusuário
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Verificando e criando superusuário, se necessário..."
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print(f"Superusuário '$DJANGO_SUPERUSER_USERNAME' criado com sucesso!")
else:
    print(f"Superusuário '$DJANGO_SUPERUSER_USERNAME' já existe.")
EOF
else
  echo "Variáveis de ambiente para superusuário Django não definidas. Pulando criação automática de superusuário."
fi


# Inicia o servidor de desenvolvimento do Django, disponibilizando-o em todos os interfaces de rede do contêiner, na porta 8000.
echo "======================================"
echo "Iniciando servidor Django..."
echo "Acesse: http://localhost:8000"
echo "======================================"
python manage.py runserver 0.0.0.0:8000
