# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
import json
from cordis_fact_sheet.items import CordisFactSheetItem
from scrapy.exporters import CsvItemExporter, JsonItemExporter
import csv


class CordisFactSheetPipeline:
    def open_spider(self, spider):
        self.id_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.id_to_exporter.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item):
        id = item['project_id']
        if id not in self.id_to_exporter:
            f = open('{}_fact_sheet.json'.format(id), 'wb')
            exporter = JsonItemExporter(f,ensure_ascii=False)
            exporter.start_exporting()
            self.id_to_exporter[id] = exporter
        return self.id_to_exporter[id]

    def process_item(self, item, spider):
        exporter = self._exporter_for_item(item)
        exporter.export_item(item)
        return item
