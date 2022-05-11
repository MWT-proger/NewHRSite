# Блок продакшн
run_prod:
	docker-compose -f docker-compose.prod.yml up --build
full_upload:
	docker-compose -f docker-compose.prod.yml build --no-cache
	docker-compose -f docker-compose.prod.yml up -d
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Блок разработки
dev_full_upload:
	docker-compose -f docker-compose.yml up -d --build
	docker-compose -f docker-compose.yml exec web_dev python manage.py makemigrations
	docker-compose -f docker-compose.yml exec web_dev python manage.py migrate
	docker-compose -f docker-compose.yml exec web_dev python manage.py collectstatic --noinput
dev_run:
	docker-compose -f docker-compose.yml up --build
dev_create_user:
	docker-compose -f docker-compose.dev.yml exec web_dev python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
