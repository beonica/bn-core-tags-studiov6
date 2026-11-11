const vm = require('node:vm');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {js, tests} = JSON.parse(fs.readFileSync(0, 'utf8'));
for (const scenario of tests.scenarios) {
  const calls = {};
  const mocks = {};
  const record = (name, args) => (calls[name] ||= []).push(args);
  const context = {
    mock(name, value) { mocks[name] = value; },
    assertApi(name) { return {
      wasCalled() { assert.ok(calls[name]?.length, name); },
      wasNotCalled() { assert.ok(!calls[name]?.length, name); },
      wasCalledWith(...expected) { assert.ok(calls[name]?.some(args => JSON.stringify(args) === JSON.stringify(expected)), name); }
    }; },
    assertThat(actual) { return {
      isEqualTo(expected) { assert.equal(JSON.stringify(actual), JSON.stringify(expected)); },
      isEmpty() { assert.equal(actual.length, 0); },
      hasLength(n) { assert.equal(actual.length, n); }
    }; },
    runCode(input) {
      const data = {...input, gtmOnSuccess: () => record('gtmOnSuccess', []), gtmOnFailure: () => record('gtmOnFailure', [])};
      const requireMock = name => (...args) => { record(name, args); return typeof mocks[name] === 'function' ? mocks[name](...args) : mocks[name]; };
      vm.runInNewContext('(function(data, require) {\n' + js + '\n})', {})(data, requireMock);
    }
  };
  vm.runInNewContext(tests.setup + '\n' + scenario.code, context);
  console.log('OK:', scenario.name);
}
console.log('Mocks locais; não executa sandbox ou permissões nativas do GTM.');
