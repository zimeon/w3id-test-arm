#!/bin/bash

# Cleanup
killall -9 httpd
rm -rf /tmp/w3id-test-arm

# Setup
mkdir /tmp/w3id-test-arm
mkdir /tmp/w3id-test-arm/logs
mkdir /tmp/w3id-test-arm/htdocs
cp ~/src/w3id.org/.htaccess /tmp/w3id-test-arm/htdocs
cp -r ~/src/w3id.org/arm /tmp/w3id-test-arm/htdocs

# Run
echo "Running under on http://localhost:8080/arm/"
httpd -d . -f apache.conf
sleep 1
pid=`cat /tmp/w3id-test-arm/logs/httpd.pid`
echo "Running with PID $pid"
echo "Tailing error and access logs... (^C to exit,  kill -TERM $pid   to clean up)"
echo "Try: http://localhost:8080/arm/BAD"
echo "Try: http://localhost:8080/arm"
echo "Try: http://localhost:8080/arm/"
echo "Try: http://localhost:8080/arm/core/ontology/"
echo "Try: http://localhost:8080/arm/core/ontology/0.1/"
echo "Try rdf: curl http://localhost:8080/arm/core/ontology/0.1/Arrangement"
echo "Try html: curl -H 'Accept: text/html' http://localhost:8080/arm/core/ontology/0.1/Arrangement"
tail -qf /tmp/w3id-test-arm/logs/error_log /tmp/w3id-test-arm/logs/access_log

