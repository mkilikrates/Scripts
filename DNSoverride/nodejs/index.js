exports.handler = async function(event) {
  var evilDns = require('evil-dns');
  var url = (event.url);
  const https = require('https');
  console.log(`Testing DNS Resolution via specific DNS Server\nEvent: ${JSON.stringify(event)}`);
  evilDns.add(event.name, event.ip);
  const promise = new Promise(function(resolve, reject) {
    https.get(url, (res) => {
        resolve(res.statusCode);
        console.info(`Result: ${JSON.stringify(res.statusCode)}`);
      }).on('error', (e) => {
        reject(Error(e));
        console.error(`Error: ${JSON.stringify(e)}`);
      });
  evilDns.clear();
    });
  return promise;
};

