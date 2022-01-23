var ques = localStorage.getItem("quesValue");
document.getElementById("qlabel").innerHTML=ques;

/////// append faq data
var faqdata = JSON.parse(localStorage.getItem("faqdata"));

if(faqdata["retrieved_question"] == "NONE" && faqdata["retrieved_answer"] == "NONE"){
  document.getElementById("faqdesc").innerHTML = faqdata["faq"];
}
else{
  document.getElementById("faq_ques").innerHTML = "FAQ: " + faqdata["retrieved_question"];
  document.getElementById("faq_ans").innerHTML = faqdata["retrieved_answer"];
}

//////// append QnA ranking model results
var qnarankingdata = JSON.parse(localStorage.getItem("qnarankingdata"));
document.getElementById("qnarankingsubject").innerHTML = "SUBJECT:  " + qnarankingdata[0];

var i;
for(i = 1; i <= parseInt(localStorage.getItem("qnaindex")); i++){

  var newNode = document.createElement('div');
  newNode.classList.add("serp__result")
  newNode.innerHTML = '<a href="' + qnarankingdata[i] + '" target = "_blank"> <div class="serp__title">' + i + '</div> <div class="serp__url">' + qnarankingdata[i] + '</div> </a>';
  document.getElementById("qnadesc").appendChild(newNode);
}

///////// append pagerank search result
var pr_result_list = JSON.parse(localStorage.getItem("pr_search_result_data"));

for (i = 0; i < pr_result_list["items"].length; i++){
	var newNode = document.createElement('div');
  newNode.classList.add("serp__result")
	newNode.innerHTML = '<a href="' + pr_result_list["items"][i]["link"] + '" target = "_blank"> <div class="serp__title">' + pr_result_list["items"][i]["title"] + '</div> <div class="serp__url">' + pr_result_list["items"][i]["link"] + '</div> </a> <span class="serp__description">' + pr_result_list["items"][i]["snippet"] + "</span>";
	document.getElementById("prdesc").appendChild(newNode);
}


// localStorage.clear();

$(window).unload(function(){
  localStorage.myPageDataArr=undefined;
});
