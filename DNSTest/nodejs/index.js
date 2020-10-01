global.response = {};
exports.handler = async (event) => {
    //console.log("ENVIRONMENT VARIABLES\n" + JSON.stringify(process.env, null, 2));
    console.info("EVENT\n" + JSON.stringify(event, null, 2));
    console.log(`Testing DNS Resolution via specific DNS Server\nEvent: ${JSON.stringify(event)}`);
    const { Resolver } = require('dns');
    const resolver = new Resolver();
    if (event.ns) {
        resolver.setServers(event.ns);
    }
    resolver.resolve4(event.name, (err, addresses) => {
        if (err) console.log(err, err.stack);
        console.log(`addresses: ${JSON.stringify(addresses)}`);
        global.response['statusCode'] = 200;
        global.response['body'] = addresses;
            });
    return global.response;
};
