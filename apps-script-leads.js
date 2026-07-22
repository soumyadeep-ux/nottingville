/**
 * Nottingville Lead Capture — Google Apps Script
 *
 * Setup:
 * 1. Create a Google Sheet named "Nottingville Leads"
 * 2. Add headers in Row 1: Timestamp | Parent Name | Phone | Student Name | Class | Exam | Coaching | Move-in | Source | Page URL
 * 3. Go to Extensions → Apps Script
 * 4. Paste this code, save
 * 5. Deploy → New deployment → Web app → Execute as: Me, Access: Anyone
 * 6. Copy the web app URL and set it in index.html as window.__SHEETS_ENDPOINT
 */

var SHEET_ID = '1dtCbSjtWOk5kW02XS7SshApDiE6tSM9dJb4zHoH0WcI';

function doGet(e) {
  return handleRequest(e.parameter);
}

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    return handleRequest(data);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function handleRequest(data) {
  try {
    var ss = SpreadsheetApp.openById(SHEET_ID);
    var sheet = ss.getSheetByName('Leads');
    if (!sheet) {
      sheet = ss.getSheets()[0];
    }

    sheet.appendRow([
      new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' }),
      data.parent_name || '',
      data.phone || '',
      data.student_name || '',
      data.student_class || '',
      data.exam || '',
      data.coaching || '',
      data.move_in || '',
      data.source || 'form',
      data.page_url || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
