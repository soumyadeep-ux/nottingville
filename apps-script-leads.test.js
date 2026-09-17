// Loads apps-script-leads.js with mocked Apps Script globals and checks which
// requests produce a row. Run before every push: node apps-script-leads.test.js
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

function load() {
  const rows = [];
  const header = [[]];
  const sheet = {
    getRange: () => ({ getValues: () => header, setValues: v => { header[0] = v[0]; },
                       copyFormatToRange: () => {} }),
    appendRow: r => rows.push(r),
  };
  const ctx = {
    SpreadsheetApp: { openById: () => ({ getSheetByName: () => sheet, getSheets: () => [sheet] }) },
    ContentService: {
      MimeType: { JSON: 'json' },
      createTextOutput: s => ({ body: s, setMimeType() { return this; } }),
    },
  };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(__dirname, 'apps-script-leads.js'), 'utf8'), ctx);
  return { ctx, rows };
}

let failed = 0;
function test(name, fn) {
  try { fn(); console.log('PASS', name); } catch (e) { failed++; console.log('FAIL', name, '-', e.message); }
}

test('bare /exec hit (no params) writes no row', () => {
  const { ctx, rows } = load();
  ctx.doGet({ parameter: {} });
  assert.strictEqual(rows.length, 0, 'expected 0 rows, got ' + rows.length + ': ' + JSON.stringify(rows[0]));
});

test('landing-page click is logged with source, cta and page', () => {
  const { ctx, rows } = load();
  ctx.doGet({ parameter: { source: 'lp:phone', cta: 'sticky-call', page: 'pg-city-centre-durgapur',
                           page_url: 'https://nottingville.space/pg-city-centre-durgapur?gclid=x' } });
  assert.strictEqual(rows.length, 1);
  assert.strictEqual(rows[0][8], 'lp:phone');
  assert.strictEqual(rows[0][9], 'https://nottingville.space/pg-city-centre-durgapur?gclid=x');
  assert.strictEqual(rows[0][10], 'sticky-call');
  assert.strictEqual(rows[0][11], 'pg-city-centre-durgapur');
});

test('homepage form submit is logged with the parent details', () => {
  const { ctx, rows } = load();
  ctx.doGet({ parameter: { parent_name: 'Sunita', phone: '9876543210', student_name: 'Priya',
                           source: 'form', page_url: 'https://nottingville.space/' } });
  assert.strictEqual(rows.length, 1);
  assert.strictEqual(rows[0][1], 'Sunita');
  assert.strictEqual(rows[0][2], '9876543210');
  assert.strictEqual(rows[0][8], 'form');
});

test('homepage "skip" is logged', () => {
  const { ctx, rows } = load();
  ctx.doGet({ parameter: { source: 'skip', page_url: 'https://nottingville.space/' } });
  assert.strictEqual(rows.length, 1);
  assert.strictEqual(rows[0][8], 'skip');
});

test('POST without source writes no row', () => {
  const { ctx, rows } = load();
  ctx.doPost({ postData: { contents: '{}' } });
  assert.strictEqual(rows.length, 0);
});

test('a failing header rewrite never blocks lead logging', () => {
  const { ctx, rows } = load();
  // Row 1 edited by hand, and the rewrite throws (e.g. a validation rule on row 1).
  ctx.SpreadsheetApp.openById = () => ({
    getSheetByName: () => ({
      getRange: () => ({ getValues: () => [['edited by hand']],
                         setValues: () => { throw new Error('violates data validation'); },
                         copyFormatToRange: () => {} }),
      appendRow: r => rows.push(r),
    }),
  });
  ctx.doGet({ parameter: { source: 'lp:phone', page: 'pg-durgapur',
                           page_url: 'https://nottingville.space/pg-durgapur' } });
  assert.strictEqual(rows.length, 1, 'lead was lost because ensureHeaders threw');
});

process.exit(failed ? 1 : 0);
