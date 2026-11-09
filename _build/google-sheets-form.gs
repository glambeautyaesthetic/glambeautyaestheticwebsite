/**
 * Glam Beauty Aesthetics: website enquiries → Google Sheet (+ email alert)
 *
 * Setup (about 10 minutes):
 *  1. Create a new Google Sheet (e.g. "Website enquiries") in the clinic's Google account.
 *  2. Extensions → Apps Script. Delete what's there, paste this whole file, click Save.
 *  3. Deploy → New deployment → gear icon → Web app.
 *       Execute as: Me
 *       Who has access: Anyone
 *     Click Deploy, then Authorise access and allow the permissions.
 *  4. Copy the "Web app URL" (it ends in /exec) and send it to your web developer.
 *
 * Every enquiry is added as a row on the "Enquiries" tab, newest at the bottom.
 * Set NOTIFY_EMAIL to '' to turn off the email alerts.
 */
const SHEET_NAME = 'Enquiries';
const NOTIFY_EMAIL = 'shania0712@googlemail.com';

// [column heading, form field]
const FIELDS = [
  ['Received', null],
  ['Name', 'name'],
  ['Phone', 'phone'],
  ['Email', 'email'],
  ['Treatment', 'treatment'],
  ['Contact by', 'contact_method'],
  ['Message', 'message'],
  ['Consent to contact', 'consent'],
  ['Sent from', 'page'],
];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p._gotcha) return json({ ok: true });                       // hidden spam trap was filled in
  if (!p.name || !(p.phone || p.email)) return json({ ok: false, error: 'missing details' });

  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const row = FIELDS.map(([, key]) => {
      if (!key) return new Date();
      if (key === 'phone') return "'" + clean(p.phone).replace(/^'/, '');  // keep the leading 0
      if (key === 'consent') return p.consent ? 'Yes' : 'No';
      return clean(p[key]);
    });
    getSheet().appendRow(row);
  } finally {
    lock.releaseLock();
  }

  if (NOTIFY_EMAIL) {
    const body = FIELDS.filter(([, key]) => key)
      .map(([label, key]) => label + ': ' + (key === 'consent' ? (p.consent ? 'Yes' : 'No') : (p[key] || '-')))
      .join('\n');
    const options = {
      to: NOTIFY_EMAIL,
      subject: 'New website enquiry: ' + (p.treatment || 'General') + ' (' + (p.name || '') + ')',
      body: body + '\n\nAll enquiries: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl(),
    };
    if (isEmail(p.email)) options.replyTo = p.email;
    MailApp.sendEmail(options);
  }
  return json({ ok: true });
}

// Opening the Web app URL in a browser shows this, which confirms it's live.
function doGet() {
  return ContentService.createTextOutput('Glam Beauty Aesthetics enquiry form is connected.');
}

function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(FIELDS.map(([label]) => label));
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, FIELDS.length).setFontWeight('bold').setBackground('#F1E6E2');
    sheet.setColumnWidth(7, 360);
  }
  return sheet;
}

// Trim long text and stop anything that looks like a spreadsheet formula from running.
function clean(value) {
  const v = String(value || '').slice(0, 2000);
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function isEmail(v) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(v || ''));
}

function json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
