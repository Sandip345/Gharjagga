from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='Import products in gharjagga'

    def handle(self,*args,**options):
        self.stdout.write("Importing Products")
