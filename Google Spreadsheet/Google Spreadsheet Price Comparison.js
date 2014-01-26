/**
 * Retrieves all the rows in the active spreadsheet that contain data and logs the
 * values for each row.
 * For more information on using the Spreadsheet API, see
 * https://developers.google.com/apps-script/service_spreadsheet
 */

// Set up categories to delete, because they're not being used for comparison.
var excessCategories = ["", "0", 0, "DC", "GB", "GBA", "GBC", "GC", "GCUBE", "GEN", "N64", "N8", "PC", "PS2", "PS4", "PSX", "SN", "SO-PRO", "WiiU", "XB1", "XBOX"];

var ss = SpreadsheetApp.getActiveSpreadsheet();
//var sheet = SpreadsheetApp.getActiveSheet();
var sheet1 = ss.getSheets()[0];
var sheet2 = ss.getSheets()[1];
var sheet3 = ss.getSheets()[2];
var sheet = sheet1;
var rows = sheet.getDataRange();
var numRows = rows.getNumRows();
var values = rows.getValues();


function deleteExcess() {
  // Set the first sheet as the active sheet.
  sheet = sheet1;
  // Prompt user to make sure they want to delete the excess.
  var result = Browser.msgBox(
    'The excess data in the spreadsheet will be deleted.',
    'Are you sure you want to continue?',
    Browser.Buttons.YES_NO);

  // Process the user's response.
  if (result == 'yes') {
    // User clicked "Yes".    
    
    // Delete all the columns that contain info we don't need
    var firstCellRange = sheet.getRange(1, 1);
    var firstCellValue = firstCellRange.getValue();
    if(firstCellValue == "*******************************************************************************************************************************") {
      sheet.deleteColumns(25, 5);
      sheet.deleteColumns(20, 4);
      sheet.deleteColumns(1, 16);
    }
    
    // ---------------------------------------------------------------------------------------------
    // Delete all the rows that contain items from categories we don't want to parse
    
    var lastRow = sheet.getLastRow();
    // Get values of entire first column (row, column, numRows, numColumns) -1 returns last row or column with data.
    var rangeValues = sheet.getSheetValues(1, 1, lastRow, 1);
    // Logger.log(rangeValues);
    var excessRows = [];
    
    // Append all rows that have a value that matches excessCategories to excessRows from last to first.
    for (var x=0;x <= lastRow - 1;x++){
      for (var y in excessCategories) {
        if (rangeValues[x] == excessCategories[y]) {
          excessRows.push(x + 1);
        }
      }
    }
    
    // Iterate through excessRows to grab chunks of rows at a time and append them to separate lists,
    // so we don't have to delete rows individually.
    excessRows.push("end");
    var chunkedRows = chunk(excessRows);
    var finished = deleteRows(chunkedRows);
    // ------------------------------------------------------------------------------------------------
    
    Browser.msgBox(finished);  
  } else {
    // User clicked "No" or X in the title bar.
    Browser.msgBox('Data Deletion Canceled.');
  }
};

function chunk(array) {
  var R = [];
  while (array[0] != "end") {
    for (var i = array.length - 2; i >= 0; i--) {
      var x = array[i] - 1;
      //Logger.log("i - 1 is: " + array[i - 1] + " and x is: " + x);
      if (x != array[i - 1]) {
       // Logger.log("i and x are not equal. Splicing.");
        R.push(array.splice(i, array.length - 1 - i));
        break;
      }
    }
  }
  //Logger.log(R);
  return R;
};

function deleteRows(array) {
  // Get the active sheet.
  sheet = sheet1;
  for (var i = 0; i < array.length; i++) {
    //Logger.log("Deleting row " + array[i][0] + " and the " + (array[i].length - 1) + " behind it.");
    sheet.deleteRows(array[i][0], array[i].length);
  }
  return 'Excess data has been deleted';
};

/*
function search(items, match) {
  // Set the first sheet as the active sheet.
  sheet = sheet1;
  var lastRowS1 = sheet.getLastRow();
  var rangeS1 = sheet.getRange(1, 1, lastRow);
  var valuesS1 = 
  
  
  
  
  // --------- Fast Binary Search
  var low = 0,
  high = items.length -1;
             
  while (low <= high) {
    mid = parseInt((low + high) / 2);
    
    current = items[mid];
    
    if (current > match) {
      high = mid - 1;
    } else if (current < match) {
      low = mid + 1;
    } else {
      return mid;
    }
  }
  return -1;
  // --------------------------
};

function test() {
  var testArray = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 17, 19, 20, 21, 23, 24, 25, 26, 27, "end"];
  var testChunk = chunk(testArray);
  Logger.log(testChunk);
  deleteRows(testChunk);
};

/**
 * Adds a custom menu to the active spreadsheet, containing a single menu item
 * for invoking the readRows() function specified above.
 * The onOpen() function, when defined, is automatically invoked whenever the
 * spreadsheet is opened.
 * For more information on using the Spreadsheet API, see
 * https://developers.google.com/apps-script/service_spreadsheet
 */
function onOpen() {
  var entries = [{
    name : "Delete Excess Data",
    functionName : "deleteExcess"
  }];
  ss.addMenu("Gamez Unleashed Menu", entries);
};
