const isNumber = require('is-number');
if (!isNumber(42) || isNumber('42')) process.exit(1);
console.log('Basic dependency smoke test passed');
