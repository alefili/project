import csv
import os  # Add this import for joining file paths
from django.core.management.base import BaseCommand
from app.models import Aliment, Reteta, RetetaAliment  # Assuming app is your Django app name

class Command(BaseCommand):
    help = 'Import data from CSV files'

    def handle(self, *args, **kwargs):
        # Get the directory path of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_dir = os.path.join(current_dir, 'csv')  # Directory containing CSV files

        # CSV file paths
        aliment_csv_file = os.path.join(csv_dir, 'alimente.csv')
        reteta_csv_file = os.path.join(csv_dir, 'reteta.csv')
        retetaaliment_csv_file = os.path.join(csv_dir, 'retetaaliment.csv')

        # Import data for Aliment model
        with open(aliment_csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                aliment = Aliment.objects.create(
                    titlu=row['titlu'],
                    unitate=row['unitate'],
                    calorii_unitate=row['calorii_unitate']
                )
                aliment.save()

        # Import data for Reteta model
        with open(reteta_csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reteta = Reteta.objects.create(
                    nume=row['nume'],
                    indicatii=row['indicatii']
                )
                reteta.save()

        # Import data for RetetaAliment model
        with open(retetaaliment_csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reteta = Reteta.objects.get(nume=row['reteta'])
                aliment = Aliment.objects.get(titlu=row['aliment'])
                reteta_aliment = RetetaAliment.objects.create(
                    reteta=reteta,
                    aliment=aliment,
                    cantitate_aliment=row['cantitate_aliment']
                )
                reteta_aliment.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))