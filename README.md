# Local Mac OSX Apache setup to test https://w3id.org/arm config

## Ontology locations

  * Version 0.1 was hosted at <https://ld4p.github.io/arm/> based on source <https://github.com/ld4p/arm>
  * Development has since shifted to <https://art-and-rare-materials-bf-ext.github.io/arm/> based on source <https://github.com/Art-and-Rare-Materials-BF-Ext/arm>. The 0.1 files are hosted unchanged at <https://art-and-rare-materials-bf-ext.github.io/arm/v0.1/>

## URI changes from 0.1 to 1.0

### Move of 0.1 hosting

In redirects:
  * Change `https://ld4p.github.io/arm/` to `https://art-and-rare-materials-bf-ext.github.io/arm/v0.1/` everywhere

In new source repository:
  * Fix files in `v0.1` dir to point to new `js` and `css` locations [https://github.com/Art-and-Rare-Materials-BF-Ext/arm/pull/38]

### Addition of 1.0 hosting

Additional URIs:
  * https://w3id.org/arm/core/ontology/ - changed
  * https://w3id.org/arm/ontology/1.0/ --> https://art-and-rare-materials-bf-ext.github.io/arm/v1.0/ontology/arm_1_0.rdf
  * https://w3id.org/arm/vocabularies/1.0/origin/ --> https://art-and-rare-materials-bf-ext.github.io/arm/v1.0/vocabularies/origin.rdf
  * etc.

### Update of unversioned URIs with addition of 1.0

The are very significant changes to the ontology and vocabulary layouts associated with the move from 0.1 to 1.0.

All ontologies have been combined into one and thus, for ontologies:
  * Change `/arm/core/ontology` to point instead to the one new ontology `/arm/ontology/1.0/` per declaration in <https://github.com/Art-and-Rare-Materials-BF-Ext/arm/blob/main/v1.0/ontology/arm_1_0.rdf?
  * All other unversioned ontology redirects stay the same, pointing to appropriate 0.1 ontologies

The vocabularies all used to have URIs with prefixes `/arm/core/vocabularies/` and now the prefix is `/arm/v1.0/vocabularies/`. There are various changes:

  * `arrangement` has been renamed `physical_presentation`
  * `origin`, `status`, `typeface` have some name
  * `note_types` and `relator` are new vocabularies
  * `handwriting_type` is deprecated so no change of redirect

## Testing on local version of w3id.org htaccess

  * Assumes checked out copy of config in `~/src/w3id.org/`
  * Creates Apache root in `/tmp/w3id-test-arm` (zaps anything with that name)

Can set up test server with:

```
killall -9 httpd; ./run_test_apache_mac.sh
```

Can then run tests against this server with:

```
./test_redirects.py
```

(add `-v` to see the redirects).

## Testing on live w3id.org server

```
./test_redirects.py --live
```
