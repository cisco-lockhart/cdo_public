const pug = require('pug');
const _ = require('lodash');
const fs = require('fs');
var exec = require('child_process').exec;
const jsonDir = process.argv[2];
const TEMPLATE_PATH = `${__dirname}/template.pug`;
const STYLESHEET = fs.readFileSync(`${__dirname}/static/report.css`, 'utf8');
const ANGULAR = fs.readFileSync(`${__dirname}/static/angular.min.js`, 'utf8');
const ANGULAR_TEMPLATE = fs.readFileSync(`${__dirname}/static/app.html`, 'utf8');
const APP_SCRIPT = fs.readFileSync(`${__dirname}/static/app.js`, 'utf8');

// import json files from a path passed into the script
if(!jsonDir) {
  console.error('ERROR: JSON file directory must be specified as the first parameter');
  process.exit(1);
}
const jsonFiles = _(fs.readdirSync(jsonDir))
  .filter((filename) => {
    return _.endsWith(filename, '.json');
  })
  .map((filename) => {
    return `${jsonDir}/${filename}`;
  })
  .map((path) => {
    return _.merge({}, require(path), {path: path});
  })
  .value();
const filesToParse = jsonFiles;

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
// - The generated HTML in BDB omits "ok" severity and only shows "info", "warning", and "notice"

function parseSingleJson(obj) {
  const alertsList = _(_.get(obj, 'data.variables.json_output', []))
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

  return {
    resultTypeAgg,
    issueList,
    path: obj.path
  }
}

function countSeveritiesInParsedJson(obj, severityLevel) {
  return _.filter(obj.issueList, (result) => {
    return result.severity === severityLevel;
  }).length;
}

function compileHtml(bindings) {
  return pug.compileFile(TEMPLATE_PATH)(_.merge({}, bindings, {
    stylesheet: STYLESHEET,
    preScript: `var bindings = ${JSON.stringify(bindings)};`,
    angular: ANGULAR,
    angularTemplate: ANGULAR_TEMPLATE,
    postScript: APP_SCRIPT
  }));
}

/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////

const results = _.map(filesToParse, parseSingleJson);

fs.writeFileSync('report.html', compileHtml({
  results: _.map(results, (result) => {
    return {
      path: result.path,
      agg: _.map(result.resultTypeAgg, (value, key) => {
        return {
          type: key,
          count: value
        }
      })
    };
  }),
  statistics: {
    issueCounts: {
      info: _.sum(_.map(results, (result) => {return countSeveritiesInParsedJson(result, SEVERITY.info)})),
      notice: _.sum(_.map(results, (result) => {return countSeveritiesInParsedJson(result, SEVERITY.notice)})),
      warning: _.sum(_.map(results, (result) => {return countSeveritiesInParsedJson(result, SEVERITY.warning)}))
    }
  }
}));

exec('open ./report.html');
