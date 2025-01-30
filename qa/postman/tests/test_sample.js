const newman = require('newman');

newman.run({
    collection: require('../collections/sample_collection.json'),
    environment: require('../environments/sample_environment.json'),
    reporters: 'cli'
}, function (err) {
    if (err) { throw err; }
    console.log('Collection run complete!');
});