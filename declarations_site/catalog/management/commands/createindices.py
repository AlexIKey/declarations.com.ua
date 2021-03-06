from django.core.management.base import BaseCommand

from elasticsearch_dsl.connections import connections

from catalog.constants import CATALOG_INDICES, CATALOG_INDEX_SETTINGS
from catalog.elastic_models import Declaration, NACPDeclaration


class Command(BaseCommand):
    help = 'Creates ElasticSearch indices with proper settings'

    def add_arguments(self, parser):
        parser.add_argument('indices', nargs='+', choices=CATALOG_INDICES)

    def handle(self, *args, **options):
        for index in options['indices']:
            if index == 'declarations_v2':
                doc_type = Declaration
            elif index == 'nacp_declarations':
                doc_type = NACPDeclaration

            es = connections.get_connection('default')
            if es.indices.exists(index=index):
                self.stdout.write('Index "{}" already exists, not creating.'.format(index))
                return

            doc_type.init()
            es.indices.put_settings(index=index, body=CATALOG_INDEX_SETTINGS)
            self.stdout.write('Created index "{}".'.format(index))
