#!/usr/bin/env python
"""Make .htaccess file for w3id.org/arm.

Follows patterns laid out in
https://github.com/LD4P/arm/issues/58
"""

import logging
import requests
import sys

ONTOLOGIES = [
  ('core', ['0.1']),
  ('activity', ['0.1']),
  ('award', ['0.1']),
  ('custodial_history', ['0.1']),
  ('measurement', ['0.1'])
]

VOCABS = [
  ('arrangement', ['0.1']),
  ('handwriting_type', ['0.1']),
  ('origin', ['0.1']),
  ('status', ['0.1']),
  ('typeface', ['0.1'])
]

def check_exists_200(uri):
    r = requests.head(uri)
    if r.status_code != 200:
        logging.error("Got status code %d from %s" % (r.status_code, uri))
        #sys.exit(1)

def add_redirect(path, uri, flags='[R=302,L]'):
    print("RewriteRule %s %s %s" % (path, uri, flags))

def add_conneg(path, rdf, html):
    """Add content negotiation confirguration from path -> rdf or html.
    
    See semweb best practices: http://www.w3.org/TR/swbp-vocab-pub/#recipe4
    """
    print("""
# Rewrite rule to serve HTML content from the vocabulary URI if requested
RewriteCond %{HTTP_ACCEPT} !application/rdf\+xml.*(text/html|application/xhtml\+xml)
RewriteCond %{HTTP_ACCEPT} text/html [OR]
RewriteCond %{HTTP_ACCEPT} application/xhtml\+xml [OR]
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/.*""")
    print("RewriteRule %s/?$ %s [R=303]" % (path, html))
    print("""
# Rewrite rule to serve directed HTML content from class/prop URIs
RewriteCond %{HTTP_ACCEPT} !application/rdf\+xml.*(text/html|application/xhtml\+xml)
RewriteCond %{HTTP_ACCEPT} text/html [OR]
RewriteCond %{HTTP_ACCEPT} application/xhtml\+xml [OR]
RewriteCond %{HTTP_USER_AGENT} ^Mozilla/.*""")
    print("RewriteRule %s/?([^/]+) %s#$1 [R=303,NE]" % (path, html))
    print("""
# Rewrite rule to serve RDF/XML content if request is not HTML
#any non-HTML gives RDF so omit this: RewriteCond %{HTTP_ACCEPT} application/rdf\+xml""")
    print("RewriteRule %s/?([^/]*) %s [R=303]" % (path, rdf))

def write_rules(w3id_path, ld4p_base, name):
    """Write rules for one ontology or vocabulary."""
    w3id_base = 'https://w3id.org/arm/' + w3id_path
    print("\n### Setup for %s" % (w3id_base))
    # Setup for specific versions
    for version in sorted(versions):
        print("\n# Version %s" % (version))
        # rdf and html specific URIs
        rdf = '%s/%s/%s.rdf' % (ld4p_base, version, name)
        logging.info("%s %s -> %s" % (name, version, rdf))
        check_exists_200(rdf)
        html = '%s/%s/doc/lode/%s.html' % (ld4p_base, version, name)
        # FIXME not yet present: check_exists_200(html)
        add_redirect('^%s/%s/%s.rdf' % (w3id_path, version, name), rdf)
        add_redirect('^%s/%s/%s.html' % (w3id_path, version, name), html)
        # conneg
        add_conneg('^%s/%s' % (w3id_path, version), rdf, html)
    # Redirects for the lastest version
    print("\n# Unversioned -> latest version")
    add_redirect('^%s/?$' % (w3id_path),
                 '%s/%s/' % (w3id_base, version))
    add_redirect('^%s/%s.rdf$' % (w3id_path, name),
                 '%s/%s/%s.rdf' % (w3id_base, version, name))
    add_redirect('^%s/%s.html$' % (w3id_path, name),
                 '%s/%s/%s.html' % (w3id_base, version, name))


# Preamble...
print("""# LD4P Art and Rare Materials Ontology Extensions
# https://w3id.org/arm/...
Options +FollowSymLinks -MultiViews
RewriteEngine on

AddType application/rdf+xml .rdf .owl

#### Direct just to raw github on develop branch until we publish HTML+onto with conneg, at
#### least this will allow everyone to work with the real w3id ontology URIs

# Base
RewriteRule ^$ https://ld4p.github.io/arm/ [R=302,L]""")

# Ontologies
for name, versions in ONTOLOGIES:
    w3id_path = '%s/ontology' % (name)
    ld4p_base = 'https://ld4p.github.io/arm/%s/ontology' % (name)
    if name == 'activity':
        # This ontology is the odd-one out for naming
        w3id_path = 'core/activity'
        ld4p_base = 'https://ld4p.github.io/arm/core/ontology'
    write_rules(w3id_path, ld4p_base, name)

# Vocabularies
for name, versions in VOCABS:
    w3id_path = 'core/vocabularies/%s' % (name)
    ld4p_base = 'https://ld4p.github.io/arm/core/vocabularies/%s' % (name)
    write_rules(w3id_path, ld4p_base, name)
