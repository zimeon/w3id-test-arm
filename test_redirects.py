#!/usr/bin/env python
"""Run tests on a selection of https://w3id.org/arm redirects."""

import argparse
import logging
import requests
import unittest
from urllib.parse import urljoin

BASE = 'http://localhost:8080'
W3ID = 'https://w3id.org'
ARM = 'https://art-and-rare-materials-bf-ext.github.io/'


class TestRedirects(unittest.TestCase):

    def req(self, path, accept=None, code=None, redirect=None):
        """Request BASE/path."""
        headers = {}
        if accept is not None:
            headers['accept'] = accept
        uri = urljoin(BASE, path)
        r = requests.head(uri, headers=headers, allow_redirects=False)
        status_code = r.status_code
        if 'location' in r.headers:
            location = r.headers['location']
        else:
            location = None
        logging.info("Request %s --%d--> %s" % (uri, status_code, location))
        if code is not None:
            self.assertEqual(status_code, code)
        if redirect is not None:
            self.assertEqual(location, redirect)

    def test_1_0(self):
        # The 1.0 ARM now has both RDF files and HTML
        # One ontology
        self.req('/arm/core/ontology/',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/ontology/1.0/'))
        self.req('/arm/ontology/1.0/', accept='application/xml+rdf',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v1.0/ontology/arm_1_0.rdf'))
        self.req('/arm/ontology/1.0/', accept='text/html',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v1.0/ontology/arm_1_0.html'))
        self.req('/arm/ontology/1.0/Annotation',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v1.0/ontology/arm_1_0.rdf'))
        self.req('/arm/ontology/1.0/Annotation', accept='application/xml+rdf',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v1.0/ontology/arm_1_0.rdf'))
        self.req('/arm/ontology/1.0/Annotation', accept='text/html',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v1.0/ontology/arm_1_0.html#Annotation'))
        # Six vocabularies
        for vocab in ('note_types', 'origin', 'physical_presentation', 'relator', 'status', 'typeface'):
            self.req('/arm/vocabularies/1.0/' + vocab + '/',
                     code=303,
                     redirect=urljoin(ARM, '/arm/v1.0/vocabularies/' + vocab + '.rdf'))
            self.req('/arm/vocabularies/1.0/' + vocab + '/', accept='text/html',
                     code=303,
                     redirect=urljoin(ARM, '/arm/v1.0/vocabularies/' + vocab + '.html'))
            self.req('/arm/vocabularies/1.0/' + vocab + '/SomeTermHere',
                     code=303,
                     redirect=urljoin(ARM, '/arm/v1.0/vocabularies/' + vocab + '.rdf'))
            self.req('/arm/vocabularies/1.0/' + vocab + '/SomeTermHere', accept='text/html',
                     code=303,
                     redirect=urljoin(ARM, '/arm/v1.0/vocabularies/' + vocab + '.html#SomeTermHere'))

    def test_bad(self):
        self.req('/arm/BAD',
                 code=404)

    def test_generic(self):
        self.req('/arm/',
                 redirect=urljoin(ARM, '/arm/'))

    def test_award(self):
        # Unversioned URIs --> versioned URIs
        self.req('/arm/award/ontology',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/award/ontology/0.1/'))
        self.req('/arm/award/ontology/award.rdf',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/award.html',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/award/ontology/0.1/award.html'))
        # Versioned URIs -> content
        self.req('/arm/award/ontology/0.1/award.rdf',
                 redirect=urljoin(ARM, '/arm/v0.1/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/0.1/award.html',
                 redirect=urljoin(ARM, '/arm/v0.1/award/ontology/0.1/award.html'))
        self.req('/arm/award/ontology/0.1/',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v0.1/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/0.1/', accept='application/xml+rdf',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v0.1/award/ontology/0.1/award.rdf'))
        self.req('/arm/award/ontology/0.1/', accept='text/html',
                 code=303,
                 redirect=urljoin(ARM, '/arm/v0.1/award/ontology/0.1/award.html'))

    def test_core(self):
        # Unversioned
        self.req('/arm/core/ontology',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/ontology/1.0/'))
        self.req('/arm/core/ontology/',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/ontology/1.0/'))

        self.req('/arm/core/ontology/1.0/',
                 code=303,
                 redirect=urljoin(W3ID, 'https://art-and-rare-materials-bf-ext.github.io/arm/v1.0/ontology/arm_1_0.rdf'))
        self.req('/arm/core/ontology/0.1/',
                 code=303,
                 redirect=urljoin(W3ID, 'https://art-and-rare-materials-bf-ext.github.io/arm/v0.1/core/ontology/0.1/core.rdf'))

    def test_activity(self):
        self.req('/arm/activity/ontology',
                 code=302,
                 redirect=urljoin(W3ID, '/arm/activity/ontology/0.1/'))
        self.req('/arm/activity/ontology/0.1/activity.rdf',
                 redirect=urljoin(ARM, '/arm/v0.1/activity/ontology/0.1/activity.rdf'))
        self.req('/arm/activity/ontology/0.1/activity.html',
                 redirect=urljoin(ARM, '/arm/v0.1/activity/ontology/0.1/activity.html'))

    def test_origin(self):
        self.req('/arm/core/vocabularies/origin/0.1/',
                 redirect=urljoin(ARM, '/arm/v0.1/core/vocabularies/origin/0.1/origin.rdf'))


parser = argparse.ArgumentParser(description='Test ARMredirects.')
parser.add_argument('--live', '-l', action='store_true',
                    help='run against live site instead of %s' % BASE)
parser.add_argument('--verbose', '-v', action='store_true',
                    help='show requests and responses')
args = parser.parse_args()
if args.live:
    BASE = W3ID
logging.basicConfig(level=logging.INFO if args.verbose else logging.WARN)
# Avoid using unittest.main() because that messes with argarse
suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestRedirects)
unittest.TextTestRunner(verbosity=2).run(suite)
