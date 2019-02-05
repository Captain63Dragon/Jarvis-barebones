var fs = require('fs');

fs.readFile('DoNote - Reminder 8b5f5337-c2e8-436e-9049-4fd9a9e0d47e.png.txt', 'utf8', function (err, data) {

	var i;
	var data2 = "";
	var locBody = data.indexOf("doNoteBody");
	var locBodyEnd = data.indexOf("attachment\":") - 4;
	for (i=0; i < data.length; i ++ ) {
	   if (i >= 0 && i < locBody) {
		   data2 += data[i];
	   } else if (i >= locBody && i < locBodyEnd) {
		   data2 += (data[i] == '\n') ? "~" : data[i];
	   } else {
		   data2 += data[i];
	   }
	}
	console.log(data2);
	var obj = JSON.parse(data2);
	//{date, body, attach, email} = obj;
	console.log(obj);
});

// ********************************************
// const urlRegex = require('url-regex');
// const arrayUniq = require('array-uniq');

// var str = `zaudi.com http://google.com file://oreisit.txt`;
// var urls = str.match(urlRegex({exact: false, strict: false}));

// if (urls) {
	// console.log(urls);
// } else {
	// console.log("That string did not have any urls");
// }

// ********************************************
// const shortcutUrl = require('shortcut-url');
// 
// shortcutUrl('NoFrillsGuideToNodeJS-HowToCreateANodeJSWebAPP').then(url => {
//    console.log(url);
    //=> 'https://google.com'
// }).catch(err => {console.log(err)});
