var http = require('http');
var url = require('url');
var fs = require('fs');
var dt = require('./myfirstmodule');

// http://localhost:8080/lookup?recommends=Phil Windley&recommends=source&recommends=book&recommends=review&links=all
http.createServer(function (req, res) {
	fs.readFile('./paste1.txt', 'utf8', function (err, data) {
		var txt = data;
		var obj = JSON.parse(txt);
		var tempText = "";
		var parsedURL = url.parse(req.url, true);
		var recommendment = parsedURL.query.recommends;
		var links = parsedURL.query.links; 
		var i;
		var len = 0;
		if (recommendment != null) {
			len = recommendment.length;
		}
		for (i = 0; i < len; i++) {
			key = recommendment[i];
			if (key == null) {
				tempText += "Recommend key is missing<br />";
				i = len;
			} else {
				switch(recommendment[i]) {
				case obj.recommends:
					tempText += "Recommended by " + obj.recommends + "<br />";
					break;
				case "source":
					tempText += "Posted on " + obj.source + "<br />";
					break;
				case "book":
					var book = obj.book;
					var title = book.title;
					var author = book.author;
					var avail = book.availableAt.webStore;
					var bookLink = book.availableAt.link;
					tempText += "Book: ";
					tempText += (links == "all" && bookLink != null)  
						? "<a href=\"" + bookLink + "\" target=\"_links\">"  
						: "<u>"; 
					tempText += title; 
					tempText += (links == "all" && bookLink != null) ? "</a>" : "</u>";
					tempText += " by <i>" + author + "</i><br />";
					tempText += "Available at " + avail + "<br />";
					break;
				case "source":
					tempText += "Source of recommendation: " + obj.recommends.source + "<br/>";
					break;
				case "review":
					var review = obj.review;
					var title = review.title;
					var reviewer = review.reviewer;
					var platform = review.platform;
					var revLink = review.link;
					tempText += "Review: ";
					tempText += (links == "all" && revLink != null)  
						? "<a href=\"" + revLink + "\" target=\"_links\">"  
						: "<u>"; 
					tempText += title; 
					tempText += (links == "all" && revLink != null) ? "</a>" : "</u>";
					tempText += " by <i>" + reviewer +"</i><br/>";
					tempText += "Posted on " + platform + "<br />"
					break;
				default:
					tempText += "Recommends key: "+ recommendment[i] + "[" + i + "]<br />";
				}
			}
		}
	//	tempText += obj.source + "<br />Link: ";
	//	tempText += obj.linkArr[0].link + "<br /><br />";
	//	tempText += "Review type: " + obj.type.review + "<br />";
	//	tempText += "Review Title: " + obj.review.title;
	//	tempText += "<br />Appearing on " + obj.review.platform;
	//	tempText += "<br />Written by "+ obj.review.reviewer+"<br />Link: ";
	//	if (req.url == "/twitter") {
	//		tempText += obj.linkArr[0].link;
	//	} else if (req.url == "/nyt") {
	//		tempText += obj.linkArr[1].link;
	//	} else {
	//		tempText += "&lt;link not found&gt;"
	//	}
		
		res.writeHead(200, {'Content-Type': 'text/html'});
		res.write("The date and time are currently: " + dt.myDateTime() + "<br /><hr><br />" + tempText);
		res.end();
	});
}).listen(8080); 

