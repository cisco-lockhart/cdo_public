const pug = require('pug');
const _ = require('lodash');
const fs = require('fs');
const sampleData = require('./example-response.json');

const compileHtml = pug.compileFile('template.pug');

const KNOWN_TYPES = ['ok', 'issue'];
const SEVERITY = {
  ok: 0,
  info: 1,
  notice: 2,
  warning: 3
};

// data.variables.json_output (array of "check" objects)
// result_type (string)
// severity (string)
// - The generated HTML in BDB emits "ok" severity and only shows "info", "warning", and "notice"

const alertsList = _(_.get(sampleData, 'data.variables.json_output', []))
  .filter((alert) => {
    return _.includes(KNOWN_TYPES, alert.result_type);
  })
  .map((alert) => {
    return {
      severity: SEVERITY[alert.severity],
      type: alert.result_type,
      title: alert.title,
      text: alert.text
    }
  })
  .value();
const resultTypeAgg = _.reduce(alertsList, (result, alert) => {
  result[alert.type] ? result[alert.type] += 1 : result[alert.type] = 1;
  return result;
}, {});

const issueList = _.filter(alertsList, (alert) => {
  return alert.severity >= SEVERITY.info;
});

console.log(JSON.stringify(resultTypeAgg, null, 2));
console.log(JSON.stringify(issueList, null, 2));

fs.writeFile('report.html', compileHtml({
  agg: _.map(resultTypeAgg, (value, key) => {
    return {
      type: key,
      count: value
    }
  })
}));
