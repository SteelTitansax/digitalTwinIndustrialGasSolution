az webapp up \
  --name dim-sim-industrial-app \
  --resource-group rg-spaincentral-digitaltwin \
  --runtime "PYTHON:3.12" \
  --sku FREE \
  --location "spaincentral"

# Startup command
# gunicorn --workers 3 --bind 0.0.0.0:8000 equipments_sim_app.wsgi:application
# Use this command before deploy for preparing the static data
# python manage.py collectstatic