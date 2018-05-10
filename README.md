# Local Mac OSX Apache setup to test https://w3id.org/arm config

  * Assumes checked out copy of config in `~/src/w3id.org/`
  * Creates Apache root in `/tmp/w3id-test-arm` (zaps anything with that name)

Run with:

```
./make_htaccess.py > htaccess; killall -9 httpd; ./run_test_apache_mac.sh
```

Can then run tests against this server with: 

```
./test_redirects.py
```

(add `-v` to see the redirects).
