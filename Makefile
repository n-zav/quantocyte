PYTHON_BIN := `which python`
MANAGE=django-admin.py

ubuntu.env.init:
	@setcap 'cap_net_bind_service=+ep' ${PYTHON_BIN}

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=quantocyte.settings $(MANAGE) test quantocyte

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=quantocyte.settings $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=quantocyte.settings $(MANAGE) syncdb --noinput

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=quantocyte.settings $(MANAGE) migrate quantocyte
