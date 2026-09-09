"""Resource integrity tests, using temporary files rather than the real academic record."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from content_model import ContentError, load_content, validate


class ResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('papers', 'appendices', 'data'):
            (self.root / 'public' / folder).mkdir(parents=True)
        (self.root / 'public/papers/example.pdf').write_bytes(b'%PDF-1.4\n')
        (self.root / 'public/appendices/example.pdf').write_bytes(b'%PDF-1.4\n')
        (self.root / 'public/data/example.csv').write_text('date,value\n2026,1\n')
        self.data = {
            'publications': [{'id': 'example-paper', 'type': 'published', 'title': 'Example',
                              'url': 'https://doi.org/10.example/paper', 'pdf': '/papers/example.pdf',
                              'appendix': '/appendices/example.pdf'}],
            'other_publications': [],
            'presentations': [{'paper_id': 'example-paper'}],
            'datasets': [{'id': 'example-data', 'paper_id': 'example-paper', 'title': 'Example data',
                          'description': 'Annual observations.',
                          'files': [{'label': 'Data (CSV)', 'url': '/data/example.csv'}],
                          'replication_url': 'https://example.org/replication'}]
        }

    def test_local_resources_preserve_publisher_link(self):
        result = validate(deepcopy(self.data), self.root)
        self.assertEqual(result['publications'][0]['url'], self.data['publications'][0]['url'])
        self.assertEqual(len(result['datasets']), 1)

    def test_bad_paths_fail_before_build(self):
        for path in ('/papers/missing.pdf', '/papers/Example.pdf', '/papers/../example.pdf',
                     '/papers/%2e%2e/example.pdf', '//example.org/a.pdf', r'E:\papers\a.pdf',
                     'javascript:alert(1)', '/data/example.csv'):
            with self.subTest(path=path):
                record = deepcopy(self.data)
                record['publications'][0]['pdf'] = path
                with self.assertRaises(ContentError):
                    validate(record, self.root)

    def test_empty_data_and_replication_only(self):
        record = deepcopy(self.data)
        record['datasets'][0].pop('files')
        validate(record, self.root)
        record['datasets'] = []
        validate(record, self.root)

    def test_unknown_references_and_drafts_rejected(self):
        for key in ('presentations', 'datasets'):
            record = deepcopy(self.data)
            record[key][0]['paper_id'] = 'typo'
            with self.assertRaises(ContentError):
                validate(record, self.root)
        record = deepcopy(self.data)
        record['datasets'][0].pop('files')
        record['datasets'][0].pop('replication_url')
        with self.assertRaises(ContentError):
            validate(record, self.root)

    def test_duplicate_yaml_and_biography(self):
        source = self.root / 'academic.md'
        source.write_text('---\npublications: []\nother_publications: []\n---\nMy revised biography.\n', encoding='utf-8')
        self.assertEqual(load_content(source, self.root)['biography'], 'My revised biography.')
        source.write_text('---\npublications: []\npublications: []\n---\nBio\n', encoding='utf-8')
        with self.assertRaisesRegex(ContentError, 'Duplicate'):
            load_content(source, self.root)

    def test_homepage_selection_follows_paper_category(self):
        record = deepcopy(self.data)
        record['homepage'] = {'publications': ['example-paper'], 'working_papers': []}
        validate(record, self.root)
        record['publications'][0]['type'] = 'working'
        with self.assertRaisesRegex(ContentError, 'homepage.publications'):
            validate(record, self.root)
        record['homepage'] = {'publications': [], 'working_papers': ['example-paper']}
        validate(record, self.root)
        record['homepage']['working_papers'].append('example-paper')
        with self.assertRaisesRegex(ContentError, 'different papers'):
            validate(record, self.root)


if __name__ == '__main__':
    unittest.main()
